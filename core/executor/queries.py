import graphene
from django.db.models import Q

from hotels.models import Executer, RoleAdmin
from hotels.schemas.admin.type import executerForAdmin
from hotels.schemas.schema_handler import is_admin
from .inputs import PhonenumberInput, FilterExecutorInput


class ExecutorQueries(graphene.ObjectType):
    """
    Запросы Исполнителей
    """

    phonenumber_check_exists = graphene.Boolean(
        input=PhonenumberInput(required=True),
        required=True,
        description="Проверка номера телефона на существование",
    )

    def resolve_phonenumber_check_exists(self, info, input, **kwargs):
        return Executer.objects.filter(phone_number=input.number, is_active=True).exists()


class ExecutorQueriesForAdmin(graphene.ObjectType):
    """
    Запросы Исполнителей для администратора
    """

    admin_filter_executor_by_whatever = graphene.List(
        graphene.NonNull(executerForAdmin),
        input=FilterExecutorInput(required=True),
        description="Получение списка Исполнителей по чему-нибудь",
        required=True,
    )

    def resolve_admin_filter_executor_by_whatever(self, info, input):
        is_admin(info=info, permission=RoleAdmin.Roles.EXECUTER.value)
        filters = [
            Q(is_active=True),
        ]
        res = Executer.objects.none()
        if input.name:
            res = Executer.objects.filter(
                *filters,
                Q(first_name__icontains=input.name)
                | Q(second_name__icontains=input.name)
                | Q(middle_name__icontains=input.name),
            )
        if input.id:
            res = Executer.objects.filter(*filters, id=input.id)
        return res[:10]
