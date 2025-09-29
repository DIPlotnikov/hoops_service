import graphene
import jwt
from django.conf import settings
from graphene_django.fields import DjangoConnectionField

from ..input import InputName
from ..type import adminType
from ...schema_handler import isAuth, is_admin
from ....models import Admin, RoleAdmin


class QueryAdminAdmin(graphene.ObjectType):
    admin_me = graphene.Field(adminType, required=True)

    admin_all_admins = DjangoConnectionField(adminType, required=True, description="Все Админы с пагинацией")
    admin_get_admins_by_name = graphene.List(
        graphene.NonNull(adminType),
        input=InputName(required=True),
        required=True,
        description="Получение списка Администраторов по имени",
        deprecation_reason="filter by whatever",
    )
    admin_filter_admin_by_whatever = graphene.List(
        graphene.NonNull(adminType),
        input=InputName(required=True),
        required=True,
        description="Получение списка Администраторов по чему-либо",
    )

    def resolve_admin_me(self, info):
        token = isAuth(info)
        token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        if token.get("role") != -1:
            raise PermissionError("Пользователь не авторизован")
        return Admin.objects.get(id=token.get("id"))

    def resolve_admin_all_admins(self, info, **kwargs):
        is_admin(info=info, permission=RoleAdmin.Roles.SETTINGS.value)
        return Admin.objects.filter(is_active=True)

    def resolve_admin_get_admins_by_name(self, info, input):
        is_admin(info=info, permission=RoleAdmin.Roles.SETTINGS.value)
        return Admin.objects.filter(name__icontains=input.name)[:5]
