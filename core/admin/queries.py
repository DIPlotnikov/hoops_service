import graphene
from django.db.models import Q

from admin.inputs import FilterAdminInput
from hotels.models import RoleAdmin, Admin
from hotels.schemas.admin.type import adminType
from hotels.schemas.schema_handler import is_admin


class AdminQueries(graphene.ObjectType):
    """
    Запросы Админов
    """

    admin_filter_admin_by_whatever = graphene.List(
        graphene.NonNull(adminType),
        input=FilterAdminInput(required=True),
        description="Получение списка Админа по чему-нибудь",
        required=True,
    )

    def resolve_admin_filter_admin_by_whatever(self, info, input):
        is_admin(info=info, permission=RoleAdmin.Roles.EXECUTER.value)
        filters = [
            Q(is_active=True),
        ]
        if input.name:
            filters.append(Q(name__icontains=input.name))
        if input.id:
            filters.append(Q(id=input.id))
        return Admin.objects.filter(*filters)[:10]
