from datetime import datetime, timedelta

from django.utils import timezone
from graphene import ID, Mutation, NonNull, ObjectType

from manager.models import BlackList
from ..input import inputId
from ..type import Task, TaskType
from ...schema_handler import getIDRole, isAuth, isExecuter
from ....models import Executer, ExecuterState, Notification
from ....scripts import exception_handler as EH


class requestTask(Mutation):
    """
    Мутация отклика на Заявку
    """

    class Arguments:
        input = inputId(required=True)

    task = NonNull(TaskType)

    @staticmethod
    def mutate(root, info, input):
        executer_id = isExecuter(isAuth(info))
        # поиск заявки и сразу отсеивание по Исполнителю
        task = (
            Task.objects.prefetch_related("executers", "manager__favourite_executers")
            .select_related("profession", "manager")
            .filter(id=input.id)
            .exclude(executers__executer__id__in=[executer_id])
            .first()
        )
        assert task is not None, "Вы ранее уже откликались на данную заявку"
        assert task.is_closed is False, "Нельзя откликнуться на эту заявку, она закрыта"

        assert (
            BlackList.objects.filter(executor_id=executer_id, manager=task.manager).exists() is False
        ), "Заявка не доступна"
        assert task.is_approved is True, "Заявка не подтверждена"

        # проверка заявки на "для избранных"
        if task.for_favorite:
            if (task.created_at + timedelta(minutes=120)) > timezone.now():
                if not task.manager.favourite_executers.filter(id=executer_id).first():
                    raise ValueError("Нельзя откликнуться")

        # проверка рядом стоящих принятых заявок
        other_tasks = Task.objects.filter(
            start_at__range=(
                task.start_at - timedelta(hours=26),
                (task.start_at + timedelta(hours=(task.duration + 3))),
            ),
            executers__executer__id=executer_id,
        ).exclude(status="DELETED")
        for other_task in other_tasks:
            if (
                (other_task.start_at - timedelta(hours=3)).timestamp()
                < task.start_at.timestamp()
                < (other_task.start_at + timedelta(hours=(other_task.duration + 3))).timestamp()
            ):
                raise EH.customError("Ошибка", f"Данная дата занята заявкой # {other_task.id}")
            # # до начала заявки должно быть 3 часа от окончания другой
            if (
                (other_task.start_at - timedelta(hours=3)).timestamp()
                < (task.start_at + timedelta(hours=task.duration)).timestamp()
                < (other_task.start_at + timedelta(hours=(other_task.duration + 3))).timestamp()
            ):
                raise EH.customError("Ошибка", f"Данная дата занята заявкой # {other_task.id}")
        # окончание проверки рядом стоящих заявок

        executer = Executer.objects.filter(professions=task.profession, id=executer_id).first()
        assert executer is not None, "Перечень Ваших профеccий не позволяет бронировать заявку"
        executer.can_work
        assert task.min_rating < executer.rating, "Данная заявка не доступна Вам из-за рейтинга :("

        executer_state = ExecuterState(executer=executer)
        executer_state.save()
        task.executers.add(executer_state)
        task.save()

        notify = Notification(
            type=Notification.TypeNotification.TASK,
            id_instance=task.manager.pk,
            role="manager",
            read=False,
            text=f"На Вашу заявку #{task.id} появился отклик!",
        )
        notify.save(task_id=task.pk)

        return requestTask(task=task)


class deleteRequestTask(Mutation):
    class Arguments:
        task = ID(required=True, description="ID заявки")

    task = NonNull(TaskType)

    @staticmethod
    def mutate(root, info, task):
        id_o, role = getIDRole(isAuth(info))
        if str(role) not in ["2"]:
            raise EH.customError("Ошибка", "нет прав на отмену отклика")
        task = Task.objects.filter(executers__executer__id=id_o, id=task).exclude(status="DELETED").first()
        if task is None:
            raise EH.customError("Ошибка", "отсутствует заявка для отмены")
        if (datetime.now() + timedelta(hours=8)).timestamp() > task.start_at.timestamp():
            raise EH.customError("Ошибка", "нельзя отказаться менее чем за 8 часов")
        executer_state = ExecuterState.objects.filter(executer__id=id_o, task__id=task.pk).first()
        if executer_state.status in ["START"]:
            raise ValueError("Нельзя отказаться - Вы приступили к работе")
        if executer_state.status in ["START", "STOP"]:
            raise ValueError("Нельзя отказаться - Вы закончили работу")
        executer_state.delete()
        notify = Notification(
            type=Notification.TypeNotification.TASK,
            id_instance=task.manager.pk,
            role="manager",
            read=False,
            text=f"Один из исполнителей отказался от заявки #{task.id}",
        )
        notify.save()
        return requestTask(task=task)


class MutationTaskForExecuter(ObjectType):
    """
    Мутации Заявок Исполнителя
    """

    executer_task_request = requestTask.Field(required=True)
    executer_request_task_delete = deleteRequestTask.Field(required=True)
