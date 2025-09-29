import graphene
from graphene_django.fields import DjangoConnectionField

from ...models import Manager
from ...scripts import exception_handler as EH
from ...tasks import send_simple_message
from ..executer.type import ExecuterType
from ..schema_handler import getIDRoleAdmin, is_manager, isAuth
from ..scheme_requisites import RequisitesType
from .type import ManagerType

"""Класс Query менеджера"""


class QueryManager(graphene.ObjectType):
    manager = graphene.Field(ManagerType, required=True, email=graphene.String(required=True))
    manager_bool = graphene.Boolean(required=True, email=graphene.String(required=True))
    manager_me = graphene.Field(ManagerType, required=True)
    manager_get_my_managers = graphene.List(graphene.NonNull(ManagerType), required=True)
    manager_get_requisites_of_my_hotel = graphene.Field(RequisitesType)

    manager_get_favorite_executers = DjangoConnectionField(ExecuterType, required=True)

    # обработчик managers
    def resolve_manager(self, info, **kwargs):
        isAuth(info)
        email = kwargs.get("email")
        if email is not None:
            return Manager.objects.filter(email=email).first()

    def resolve_manager_get_my_managers(self, info, **kwargs):
        id_o, role, _ = getIDRoleAdmin(isAuth(info))
        if role != 1:
            raise EH.customError("Ошибка", "пользователь не авторизован")

        return (
            Manager.objects.filter(hotel=Manager.objects.get(id=id_o).hotel)
            .exclude(status=1)
            .exclude(is_active=False)
            .exclude(id=id_o)
        )

    def resolve_manager_bool(self, info, **kwargs):
        # token = isAuth(info)
        email = kwargs.get("email")
        if email is not None:
            manager = Manager.objects.filter(email=email, is_admin=False).exclude(status=2).first()
            if manager is not None:
                return True
            raise EH.customError("Account already verified")

    def resolve_manager_me(self, info):
        id_o, role, _ = getIDRoleAdmin(isAuth(info))
        if role != 1:
            raise EH.customError("Ошибка", "пользователь не авторизован")
        return Manager.objects.get(id=id_o)

    def resolve_manager_get_requisites_of_my_hotel(self, info):
        id_o, role, _ = getIDRoleAdmin(isAuth(info))
        if role != 1:
            raise EH.customError("Ошибка", "пользователь не авторизован")
        hotel = Manager.objects.get(id=id_o).hotel
        if hasattr(hotel, "requisites"):

            return hotel.requisites
        else:
            return None

    def resolve_manager_resend_invate(self, info, input):
        id_o, role, admin = getIDRoleAdmin(isAuth(info))
        if admin is False:
            raise EH.customError("Ошибка", "нет прав доступа")
        manager = Manager.objects.get(
            email=input.email, hotel=Manager.objects.filter(id=id_o).first().hotel, is_active=True, is_admin=False
        )
        metka = manager.metka
        send_simple_message.delay(
            email=input.email, Name="manager", text=metka, url=info.context.headers.get("Origin")
        )
        return metka

    def resolve_manager_get_favorite_executers(self, info, **kwargs):
        manager = is_manager(info=info, permission=["FAVORITE"])
        return manager.favourite_executers
