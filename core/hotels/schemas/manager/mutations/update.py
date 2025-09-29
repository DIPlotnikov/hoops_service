import graphene

from ....models import Manager, Notification, RoleManager
from ....scripts import exception_handler as EH
from ...schema_handler import getIDRoleAdmin, is_manager_admin, isAuth
from ..input import InputForUpdateManagerRoles, managerInputForUpdate
from ..type import ManagerType


class UpdateRoles(graphene.Mutation):
    class Arguments:
        input = InputForUpdateManagerRoles(required=True)

    class Meta:
        description = "Обновление ролей менеджера"
        output = ManagerType

    @staticmethod
    def mutate(root, info, input):
        is_manager_admin(info)
        manager = Manager.objects.prefetch_related("roles").filter(id=input.id).first()

        assert manager, "Менеджер не найден"

        manager.roles.exclude(role__in=input.roles).delete()
        actual_roles = manager.roles.all().values_list("role", flat=True)
        for role in input.roles:
            if role in actual_roles:
                continue
            RoleManager.objects.create(manager=manager, role=role)

        return manager


class UpdateManager(graphene.Mutation):
    class Arguments:
        input = managerInputForUpdate(required=True)

    manager = graphene.Field(ManagerType)

    @staticmethod
    def mutate(root, info, input):
        id_o, role, admin = getIDRoleAdmin(isAuth(info))
        if role != 1:
            raise EH.customError("Ошибка", "нет доступа")
        manager = Manager.objects.filter(id=id_o)
        manager.update(**input)
        notify = Notification(
            type=Notification.TypeNotification.ACCOUNT,
            id_instance=manager[0].pk,
            role="manager",
            read=False,
            text="Вы произвели изменение своего профиля",
        )
        notify.save(notification=True)
        return UpdateManager(manager=manager[0])


class MutationManagerUpdate(graphene.ObjectType):
    manager_update = UpdateManager.Field(required=True)
    manager_update_roles_manager_by_id = UpdateRoles.Field(required=True)
