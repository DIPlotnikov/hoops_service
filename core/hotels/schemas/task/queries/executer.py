from datetime import timedelta

import graphene
from django.db.models import Count, F, Q
from django.utils import timezone
from graphene_django.fields import DjangoConnectionField

from manager.models import BlackList
from ..input import inputForGetTasks
from ..type import ExecuterStateIDAndTAskStartAt, ExecuterStateTypeForExecuter, ExecuterTaskType, TaskType
from ...input import InputIDs
from ...schema_handler import getIDRole, isAuth, isExecuter
from ....models import Executer, ExecuterState, Profession, Task
from ....scripts import exception_handler as EH


class QueryTaskExecuter(graphene.ObjectType):
    executer_all_tasks = DjangoConnectionField(TaskType, required=True, input=inputForGetTasks(required=True))
    executer_task = graphene.NonNull(TaskType, id=graphene.ID(required=True))
    executer_my_tasks = graphene.List(
        graphene.NonNull(ExecuterTaskType),
        input=graphene.DateTime(required=False, description="Из даты берется месяц"),
        required=True,
    )
    executer_get_task_at_the_moment = graphene.Field(TaskType)
    executer_get_task_by_id = graphene.NonNull(TaskType, id=graphene.ID(required=True))
    executer_my_status_of_tasks = graphene.List(
        graphene.NonNull(ExecuterStateTypeForExecuter),
        input=graphene.DateTime(required=True, description="Из даты берется месяц"),
        required=True,
        description="Получение статуса откликов",
    )
    executer_get_count_all_tasks = graphene.Int(
        required=True, description="Общее число заявок конкретного пользователя"
    )
    executer_get_id_and_date_all_executer_states_by_month = graphene.List(
        graphene.NonNull(ExecuterStateIDAndTAskStartAt),
        input=graphene.DateTime(required=True, description="Из даты берется месяц"),
        required=True,
        description="Получение статуса откликов",
    )
    executer_get_executer_state_by_id = graphene.List(
        graphene.NonNull(ExecuterStateTypeForExecuter),
        input=InputIDs(required=True),
        required=True,
        description="Получение статуса отклика по его id",
    )

    def resolve_executer_all_tasks(self, info, input, **kwargs):

        id_o = isExecuter(isAuth(info))
        if input.id is not None:
            professions = Profession.objects.filter(id=input.id, executer__id=id_o)
        else:
            professions = Profession.objects.filter(executer__id=id_o)
        assert len(professions) > 0, "Нет подписки на выбранную профессию"

        filters = [
            Q(start_at__gte=timezone.now()),
            Q(is_approved=True),
            Q(profession__in=professions),
            Q(min_rating__lte=Executer.objects.get(id=id_o).rating),
        ]
        if input.id_hotel is not None:
            filters.append(Q(manager__hotel__id=input.id_hotel))

        exclude_managers = BlackList.objects.filter(executor_id=id_o).values_list("manager__id", flat=True)

        tasks = (
            Task.objects.prefetch_related("executers", "manager__favourite_executers")
            .filter(*filters)
            .order_by("start_at")
            .exclude(status="DELETED")
            .exclude(executers__executer__id__in=[id_o])
            .exclude(manager__id__in=exclude_managers)
            .annotate(num_executers=Count("executers"))
        )

        tasks = tasks.filter(count_executers__gt=F("num_executers"))

        tasks = tasks.exclude(
            ~Q(manager__favourite_executers__id=id_o),
            for_favorite=True,
            created_at__gte=(timezone.now() - timedelta(minutes=240)),
        )
        if input.sort == "DESC":
            tasks = tasks.reverse()
        return tasks.order_by(input.fields)

    def resolve_executer_task(self, info, id, **kwargs):
        id_o, role = getIDRole(isAuth(info))
        if str(role) not in ["2"]:
            raise EH.customError("Ошибка", "нет прав доступа")

        task = (
            Task.objects.filter(id=id, profession__executer__id=id_o, is_approved=True)
            .exclude(status="DELETED")
            .first()
        )
        assert BlackList.objects.filter(executor_id=id_o, manager=task.manager).exists() is False, "Заявка не доступна"
        if task is None:
            raise EH.customError("Ошибка", "нет такой задачи или подписки на профессию")
        return task

    def resolve_executer_my_tasks(self, info, input=None):
        id_o = isExecuter(isAuth(info))
        query_set = (
            Task.objects.prefetch_related("feedbackexecuter_set", "executers")
            .filter(executers__executer__id=id_o, is_approved=True)
            .exclude(status="DELETED")
            .order_by("start_at")
        )
        if input:
            query_set = query_set.filter(
                start_at__month=input.month,
                start_at__year=input.year,
            )
        query_set_res = []
        for task in query_set:
            obj = ExecuterTaskType()
            obj.feedback = task.feedbackexecuter_set.filter(executer_id=id_o).first()
            obj.task = task
            obj.id = task.executers.filter(executer__id=id_o).first().id
            obj.status = task.executers.filter(executer__id=id_o).first()
            query_set_res.append(obj)
        return query_set_res

    def resolve_executer_get_task_at_the_moment(self, info):
        id_o, role = getIDRole(isAuth(info))
        if str(role) not in ["2"]:
            raise EH.customError("Ошибка", "нет прав доступа")
        tasks = Task.objects.filter(executers__executer__id=id_o, is_approved=True).exclude(status="DELETED")
        task = tasks.filter(start_at__date=timezone.now().date()).first()
        if task is None:
            return None
        if (task.start_at + timedelta(hours=task.duration)) < timezone.now():
            return None
        executer_state = task.executers.all().filter(executer__id=id_o).first()
        if executer_state is None or executer_state.status == "STOP":
            return None
        return task

    def resolve_executer_get_task_by_id(self, info, id):
        id_o, role = getIDRole(isAuth(info))
        assert role not in ["2"], "Нет прав доступа"
        task = (
            Task.objects.filter(executers__executer__id=id_o, is_approved=True, id=id)
            .exclude(status="DELETED")
            .first()
        )
        assert task is not None, "Заявка не найдена"
        return task

    def resolve_executer_my_status_of_tasks(self, info, input):
        id_executer = isExecuter(isAuth(info))
        res = (
            ExecuterState.objects.prefetch_related("task_set")
            .select_related("executer")
            .filter(
                executer__id=id_executer,
                task__is_approved=True,
                start_at__month=input.month,
                start_at__year=input.year,
            )
            .exclude(task__status="DELETED")
        )

        return res

    def resolve_executer_get_count_all_tasks(self, info, **kwargs):
        id_executer = isExecuter(isAuth(info))
        res = (
            ExecuterState.objects.filter(executer__id=id_executer, task__is_approved=True).exclude(
                task__status="DELETED"
            )
        ).count()

        return res

    def resolve_executer_get_id_and_date_all_executer_states_by_month(self, info, input):
        id_executer = isExecuter(isAuth(info))
        period = [input - timedelta(days=45), input + timedelta(days=45)]

        res = (
            ExecuterState.objects.prefetch_related("task_set")
            .filter(executer__id=id_executer, task__is_approved=True, task__start_at__range=period)
            .exclude(task__status="DELETED")
            .order_by("id")
        )
        return res

    def resolve_executer_get_executer_state_by_id(self, info, input):
        id_executer = isExecuter(isAuth(info))
        res = (
            ExecuterState.objects.prefetch_related("task_set")
            .filter(executer__id=id_executer, id__in=input.ids)
            .exclude(task__status="DELETED")
        )
        assert res is not None, "Отклик не найден"
        return res
