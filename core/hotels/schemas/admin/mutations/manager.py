import graphene
from ..input import InputManagerIDAdminID, InputIdPassword
from ..type import managerForAdmin
from ...input import InputID

from ...schema_handler import is_admin
from ....models import Admin, Manager, RoleAdmin


class AddManagerToAdmin(graphene.Mutation):
    """
    Добавление Куратора(Администратора) Менеджеру
    """

    class Arguments:
        input = InputManagerIDAdminID(required=True, description='Идентификаторы Менеджера и Администратора')

    manager = graphene.NonNull(managerForAdmin)

    @staticmethod
    def mutate(root, info, input):
        is_admin(info=info, permission=RoleAdmin.Roles.CUSTOMER_SET_ADMIN.value)

        manager = Manager.objects.get(id=input.manager_id)
        admin = Admin.objects.get(id=input.admin_id)

        assert manager is not None, 'Менеджер гостиницы не найден'
        assert admin is not None, 'Администратор не найден'

        manager.admin = admin
        manager.save()

        return AddManagerToAdmin(manager=manager)


class ClearAdminOfManger(graphene.Mutation):
    """
    Очищение Куратора(Администратора) у Менеджера
    """

    class Arguments:
        input = InputID(required=True, description='Идентификатор Менеджера')

    manager = graphene.NonNull(managerForAdmin)

    @staticmethod
    def mutate(root, info, input):
        is_admin(info=info, permission=RoleAdmin.Roles.CUSTOMER_SET_ADMIN.value)
        manager = Manager.objects.get(id=input.id)
        assert manager is not None, 'Менеджер гостиницы не найден'
        manager.admin = None
        manager.save()
        return ClearAdminOfManger(manager=manager)


class SetManagerPassword(graphene.Mutation):
    """
    Смена пароля у менеджера
    """

    class Arguments:
        input = InputIdPassword(required=True)

    manager = graphene.Field(graphene.NonNull(managerForAdmin))

    @staticmethod
    def mutate(root, info, input):
        is_admin(info=info, permission=RoleAdmin.Roles.CUSTOMER.value)
        manager = Manager.objects.get(id=input.id)
        manager.set_password(input.password)
        manager.save()
        return SetManagerPassword(manager=manager)


class MutationAdminManager(graphene.ObjectType):
    admin_manager_add_admin = AddManagerToAdmin.Field(required=True, description='Добавить куратора Менеджеру')
    admin_manager_clear_admin = ClearAdminOfManger.Field(required=True, description='Убрать куратора у Менеджера ')
    admin_set_password_for_manager = SetManagerPassword.Field(required=True, description='Установка пароля менеджеру Администратором')
