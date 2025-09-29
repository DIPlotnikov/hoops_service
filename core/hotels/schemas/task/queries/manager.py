from datetime import timedelta

import graphene
from django.db.models import Q
from graphene_django.fields import DjangoConnectionField

from ....models import ExecuterState, Task
from ...input import InputDateTime
from ...schema_handler import is_manager
from ..input import inputForGetMyTasks, inputId
from ..type import ExecuterStateType, TaskType


class QueryTaskManager(graphene.ObjectType):
    manager_get_my_task = DjangoConnectionField(TaskType, required=True, input=inputForGetMyTasks())
    manager_get_all_task_for_admin = DjangoConnectionField(TaskType, required=True, input=inputForGetMyTasks())
    manager_get_executers_by_taskId = graphene.List(
        graphene.NonNull(ExecuterStateType), required=True, input=inputId(required=True)
    )
    manager_get_task_by_id = graphene.Field(TaskType, required=True, input=inputId(required=True))
    manager_get_tasks_by_month = graphene.List(
        graphene.NonNull(TaskType), required=True, input=InputDateTime(required=True)
    )
    manager_get_tasks_by_date = graphene.List(
        graphene.NonNull(TaskType), required=True, input=InputDateTime(required=True)
    )

    def resolve_manager_get_my_task(self, info, input, **kwargs):
        manager = is_manager(info=info)
        filters = [manager.filter_for_query_task("TASK")]

        if input.id:
            filters.append(Q(id=input.id))
        if input.id_profession:
            filters.append(Q(profession__id=input.id_profession))
        if input.is_approved is not None:
            filters.append(Q(is_approved=input.is_approved))
        if input.date:
            filters.append(Q(start_at__gte=input.date, start_at__lte=input.date + timedelta(hours=24)))
        if input.from_archive is not None:
            filters.append(Q(is_archived=input.from_archive))

        return (
            Task.objects.select_related("profession", "manager", "personal_profession")
            .prefetch_related("executers")
            .filter(*filters)
            .exclude(status="DELETED")
            .order_by("start_at", "id")
            .distinct()
        )

    def resolve_manager_get_all_task_for_admin(self, info, input, **kwargs):
        manager = is_manager(info=info, permission=["TASK"])
        query_set = (
            Task.objects.select_related("profession", "manager", "personal_profession")
            .prefetch_related("executers")
            .filter(manager__hotel=manager.hotel)
            .exclude(status="DELETED")
            .order_by("start_at")
        )
        if input.id_profession:
            query_set = query_set.filter(profession__id=input.id_profession)
        if input.is_approved is not None:
            query_set = query_set.filter(is_approved=input.is_approved)
        if input.id:
            query_set = query_set.filter(id=input.id)
        if input.date:
            query_set = query_set.filter(start_at__date=input.date.date())
        if input.from_archive is not None:
            query_set = query_set.filter(is_archived=input.from_archive)
        return query_set.distinct()

    def resolve_manager_get_task_by_id(self, info, input):
        manager = is_manager(info=info)
        filters = [Q(id=input.id), manager.filter_for_query_task("TASK")]

        task = (
            Task.objects.select_related("profession", "manager", "personal_profession")
            .prefetch_related("executers")
            .filter(*filters)
            .exclude(status="DELETED")
            .first()
        )
        assert task, "Такой заявки нет..."
        return task

    def resolve_manager_get_executers_by_taskId(self, info, input):
        manager = is_manager(info=info)
        return ExecuterState.objects.filter(task__id=input.id, task__manager_id=manager.id).exclude(
            task__status="DELETED"
        )

    def resolve_manager_get_tasks_by_month(self, info, input):
        manager = is_manager(info=info)
        filters = [
            Q(start_at__month=input.datetime.month),
            Q(start_at__year=input.datetime.year),
            Q(is_approved=True),
            manager.filter_for_query_task("TASK"),
        ]
        query_set = (
            Task.objects.select_related("profession", "manager", "personal_profession")
            .prefetch_related("executers")
            .filter(*filters)
            .exclude(status="DELETED")
            .order_by("start_at")
        )
        return query_set

    def resolve_manager_get_tasks_by_date(self, info, input):
        manager = is_manager(info=info)
        filters = [Q(start_at__date=input.datetime.date()), Q(is_approved=True), manager.filter_for_query_task("TASK")]
        query_set = (
            Task.objects.select_related("profession", "manager", "personal_profession")
            .prefetch_related("executers")
            .filter(*filters)
            .exclude(status="DELETED")
            .order_by("start_at")
        )
        return query_set
