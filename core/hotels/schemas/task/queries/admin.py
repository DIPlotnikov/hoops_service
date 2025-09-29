import graphene
from django.db.models import Q
from graphene_django.fields import DjangoConnectionField

from ....models import RoleAdmin, Task
from ....utils.date_time import date_normalize
from ...schema_handler import is_admin
from ..input import InputForAllTaskForAdmin, inputId
from ..type import TaskForAdminType


class QueryTaskAdmin(graphene.ObjectType):
    admin_get_tasks_by_hotel_id = DjangoConnectionField(TaskForAdminType, required=True, input=inputId(required=True))
    admin_get_task_by_id = graphene.Field(TaskForAdminType, required=True, input=inputId(required=True))

    admin_all_task = DjangoConnectionField(
        TaskForAdminType, required=True, input=InputForAllTaskForAdmin(required=True)
    )

    def resolve_admin_get_tasks_by_hotel_id(self, info, input, **kwargs):
        is_admin(info=info, permission=RoleAdmin.Roles.TASK.value)
        return Task.objects.filter(manager__hotel__id=input.id)

    def resolve_admin_get_task_by_id(self, info, input, **kwargs):
        is_admin(info=info, permission=RoleAdmin.Roles.TASK.value)
        task = Task.objects.filter(id=input.id).first()
        assert task is not None, "Заявка не найдена"
        return task

    def resolve_admin_all_task(self, info, input, **kwargs):
        is_admin(info=info, permission=RoleAdmin.Roles.TASK.value)
        filters = []
        if input.task_id:
            filters.append(Q(id=input.task_id))
        if input.start_at:
            filters.append(Q(start_at__date=date_normalize(input.start_at).date()))
        if input.profession_id:
            filters.append(Q(profession__id__in=input.profession_id))
        if input.is_archived_for_admin is not None:
            filters.append(Q(is_archived_for_admin=input.is_archived_for_admin))

        return Task.objects.all().exclude(status="DELETED").filter(*filters)
