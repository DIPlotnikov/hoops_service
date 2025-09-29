import graphene
from graphene_django.fields import DjangoConnectionField

from ...models import RoleAdmin, Task
from ..schema_handler import is_admin
from ..task.type import TaskForAdminType
from .input import InputName, inputPaymentStatus
from .queries.admin import QueryAdminAdmin
from .queries.executer import AdminExecuterQuery
from .queries.hotel import QueryAdminHotel
from .queries.payment import QueryPaymentAdmin
from .type import adminType


class QueryAdmin(QueryPaymentAdmin, AdminExecuterQuery, QueryAdminHotel, QueryAdminAdmin):

    admin_me = graphene.Field(adminType, required=True)

    admin_all_admins = DjangoConnectionField(adminType, required=True, description="Все Админы с пагинацией")
    admin_get_admins_by_name = graphene.List(
        graphene.NonNull(adminType),
        input=InputName(required=True),
        required=True,
        description="Получение списка Администраторов по имени",
    )

    admin_get_tasks_by_status = DjangoConnectionField(
        TaskForAdminType, input=inputPaymentStatus(required=True), required=True
    )
    admin_get_task_payment_executers_by_status = DjangoConnectionField(
        TaskForAdminType, input=inputPaymentStatus(required=True), required=True
    )

    def resolve_admin_get_task_payment_executers_by_status(self, info, input, **kwargs):
        is_admin(info=info, permission=RoleAdmin.Roles.TASK.value)
        return Task.objects.all().filter(executers__payment_status=input.status)

    def resolve_admin_get_tasks_by_status(self, info, input, **kwargs):
        is_admin(info=info, permission=RoleAdmin.Roles.TASK.value)
        tasks = Task.objects.filter(payment_status=input.status)
        if input.id:
            tasks = tasks.filter(manager__hotel__id=input.id)
        if input.start_date and input.end_date:
            start_date = input.start_date.replace(hour=0, minute=0, second=0, microsecond=0)
            tasks = tasks.filter(start_at__range=(start_date, input.end_date))
        return tasks
