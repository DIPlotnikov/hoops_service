from datetime import datetime, timedelta

from django.db.models import Q

from ..models import ExecuterState, Manager, Task


def get_normal_period_datetime(start_date: datetime, end_date: datetime):
    if start_date > end_date:
        raise ValueError("Начальная дата не верная!")
    end_date = end_date + timedelta(hours=23, minutes=59, seconds=59, microseconds=59)
    return start_date, end_date


def get_tasks_by_period(start_date: datetime, end_date: datetime):
    tasks = (
        Task.objects.prefetch_related("executers", "executers__executer")
        .select_related("personal_profession", "profession", "manager", "manager__admin", "manager__hotel")
        .filter(start_at__range=get_normal_period_datetime(start_date, end_date))
        .exclude(status="DELETED")
        .order_by("start_at")
    )
    assert tasks.count() > 0, "Заявок не найдено"
    return tasks


def get_tasks_by_hotel_id_and_period(id_hotel: int, start_date: datetime, end_date: datetime):
    tasks = (
        Task.objects.prefetch_related("executers", "executers__executer")
        .select_related("personal_profession", "profession", "manager", "manager__hotel")
        .filter(manager__hotel__id=id_hotel, start_at__range=get_normal_period_datetime(start_date, end_date))
        .exclude(status="DELETED")
        .order_by("start_at")
    )
    assert tasks.count() > 0, "Заявок не найдено"
    return tasks


def get_tasks_by_current_manager_by_period(manager: Manager, start_date: datetime, end_date: datetime):
    tasks = (
        Task.objects.prefetch_related("executers", "executers__executer")
        .select_related("personal_profession", "profession", "manager", "manager__hotel", "additional")
        .filter(
            manager.filter_for_query_task("TASK"), start_at__range=get_normal_period_datetime(start_date, end_date)
        )
        .exclude(status="DELETED")
        .order_by("start_at")
    )
    assert tasks.count() > 0, "Заявок не найдено"
    return tasks


def get_executer_by_hotel_id_and_period(
    id_hotel: int, start_date: datetime, end_date: datetime, type: str = "primary"
):
    tasks = get_tasks_by_hotel_id_and_period(id_hotel, start_date, end_date)
    executors = (
        ExecuterState.objects.filter(task__in=tasks)
        .select_related("executer")
        .prefetch_related("task_set", "task_set__manager", "task_set__profession", "task_set__personal_profession")
        .filter(Q(stop_at__isnull=False) | Q(volume_of_the_work__isnull=False))
        .exclude(task__status="DELETED")
    )
    if type == "correction":
        executors = executors.filter(payment_status=None)
    assert executors.count() > 0, "Не найдено Исполнителей для оплаты"
    return executors, tasks


def get_executer_by_period(
    start_date: datetime, end_date: datetime, payment_status: str = "primary", hotel_id: int = None, manager=None
):
    """
    Получение списка состояний Исполнителей по периоду
    :param start_date: начальная дата
    :param end_date: конечная дата
    :param payment_status: тип запроса оплаты
    :param hotel_id: фильтр на гостиницу
    :param manager: фильтр на менеджера
    :return: список Состояний Исполнителей по периоду
    """
    filters = [
        Q(task__start_at__range=get_normal_period_datetime(start_date, end_date)),
    ]
    if hotel_id:
        filters.append(Q(task__manager__hotel__id=hotel_id))
    if manager:
        filters.append(manager.filter_for_query_executor_states("TASK"))
    if payment_status == "correction":
        filters.append(Q(payment_status=None))
    executors = (
        ExecuterState.objects.select_related("executer")
        .prefetch_related("task_set")
        .filter(*filters)
        .exclude(task__status="DELETED")
    )
    assert executors.count() > 0, "Исполнителей за указанный период не найдено"
    return executors
