import graphene
from django.contrib.auth import authenticate
from django.db import IntegrityError
from django.utils import timezone

from ....models import Admin, RoleAdmin
from ...input import InputFullName, InputPassword
from ...schema_handler import is_admin, set_session
from ..input import InputForUpsertAdmin, InputId, adminInputForAuth
from ..type import adminType


class AuthenticateAdmin(graphene.Mutation):
    """
    Авторизация Администратора
    """

    class Arguments:
        input = adminInputForAuth(required=True, description="Параметры авторизации Администратора")

    token = graphene.String(required=True, description="Токен Bearer")
    sessionid = graphene.String(required=True, description="Токен sessionid из сеанса")

    @staticmethod
    def mutate(root, info, input):
        # Ищем Администратора с указанным именем
        admin = Admin.objects.filter(name=input.name).first()
        # если такого нет
        if admin is None:
            # ошибка
            raise ValueError("Ошибка: не верный логин или пароль")
        # если пароль не верный
        if not admin.check_password(input.password):
            # ошибка
            raise ValueError("Ошибка: не верный логин или пароль")
        # устанавливаем ему сессию
        set_session(info, admin)
        # пишем время последнего захода
        admin.last_login = timezone.now()
        admin.save()
        # возвращаем токен Bearer
        return AuthenticateAdmin(token=admin.token, sessionid=info.context.session.session_key)


class UpsertAdmin(graphene.Mutation):
    """
    Обновление/создание Администратора
    """

    class Meta:
        description = "Обновление/создание Администратора"

    class Arguments:
        input = InputForUpsertAdmin(required=True, description="Параметры для содздания и обновления Администратора")

    admin = graphene.NonNull(adminType, description="Администратор")

    @staticmethod
    def mutate(root, info, input):
        # проверяем на администратора и его права и получаем его идентификатор
        id_current_admin = is_admin(info=info, permission=[RoleAdmin.Roles.SETTINGS])

        # получаем ID Администратора
        id_admin = input.pop("id", None)
        # самого себя нельзя редактировать
        assert str(id_current_admin) != id_admin, "Нельзя самого себя редактировать"
        # получаем его пароль, если он есть
        raw_password = input.pop("password", None)
        # получаем роли администратора
        roles = input.pop("roles", [])
        try:
            # обновляем или создаем Администратора
            admin, created = Admin.objects.update_or_create(id=id_admin, defaults={**input})
        except IntegrityError as e:
            raise ValueError(f"Нельзя использовать одинаковые логины:{e}")
        # если администратор был создан и его пароль не указан
        if created and raw_password is None:
            # ошибка
            raise ValueError("При создании Администратора необходимо указать пароль!")
        # если пароль указан
        if raw_password:
            # устанавливаем пароль
            admin.set_password(input.password)
            # сохраняем
            admin.save()

        # работа с ролями
        roles_set = set(roles)
        current_roles = set(admin.roleadmin_set.all().values_list("role", flat=True))
        new_roles = roles_set - current_roles
        for_delete_roles = current_roles - roles_set
        for role in new_roles:
            RoleAdmin.objects.create(role=role, admin=admin)
        admin.roleadmin_set.filter(role__in=for_delete_roles).delete()

        admin.save()

        return UpsertAdmin(admin=admin)


class SetFullNameAdmin(graphene.Mutation):
    """
    Указание полного имени Администратора
    """

    class Meta:
        description = "Указание полного имени Администратора"

    class Arguments:
        input = InputFullName(required=True, description="Параметры для указания полного имени Администратора")

    admin = graphene.NonNull(adminType, description="Администратор")

    @staticmethod
    def mutate(root, info, input):
        # проверяем на администратора и его права и получаем его идетификатор
        id_current_admin = is_admin(info=info, permission=RoleAdmin.Roles.SETTINGS.value)
        # обновление полей Администратора
        admin, _ = Admin.objects.update_or_create(id=id_current_admin, defaults={**input})
        return SetFullNameAdmin(admin=admin)


class DeactivateAdmin(graphene.Mutation):
    """
    Деактивация Администратора
    """

    class Arguments:
        input = InputId(required=True, description="Параметры деактивации Администратора")

    admin = graphene.Field(graphene.NonNull(adminType), description="Изменяемый Администратор")

    @staticmethod
    def mutate(root, info, input=None):
        # проверяем на администратора и его права
        is_admin(info=info, permission=RoleAdmin.Roles.SETTINGS.value)
        # получаем субъект
        admin = Admin.objects.get(id=input.id)
        # деактивируем его
        admin.is_active = False
        # сохраняем
        admin.save()
        return DeactivateAdmin(admin=admin)


class SetNewPasswordAdmin(graphene.Mutation):
    """
    Смена пароля Администратора
    """

    class Arguments:
        input = InputPassword(required=True, description="Параметры смена пароля")

    admin = graphene.Field(graphene.NonNull(adminType), description="Изменяемый Администратор")

    @staticmethod
    def mutate(root, info, input):
        # проверяем на администратора и его права
        is_admin(info=info, permission=RoleAdmin.Roles.SETTINGS.value)
        # получаем субъект
        admin = Admin.objects.get(id=input.id)
        # меняем пароль ему
        admin.set_password(input.new_password)
        # сохраняем
        admin.save()
        return SetNewPasswordAdmin(admin=admin)


class MutationAdminMain(graphene.ObjectType):
    admin_authenticate = AuthenticateAdmin.Field(required=True)
    admin_upsert_admin = UpsertAdmin.Field(required=True)
    admin_set_full_name = SetFullNameAdmin.Field(required=True)
    admin_deactivate = DeactivateAdmin.Field(required=True)
    admin_set_new_password_for_admin_by_id = SetNewPasswordAdmin.Field(required=True)
