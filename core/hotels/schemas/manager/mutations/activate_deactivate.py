import graphene

from ....models import Manager, TempString
from ....scripts import exception_handler as EH
from ...schema_handler import getIDRoleAdmin, isAuth
from ..input import managerInputForActivate


class ActivateManager(graphene.Mutation):
    class Arguments:
        input = managerInputForActivate(required=True)

    token = graphene.String(required=True)

    @staticmethod
    def mutate(root, info, input):
        try:
            temp_string = TempString.objects.get(first_field=input.email, second_field=input.secret)
        except:
            raise EH.customError("Ошибка", "нет прав доступа")

        manager = Manager.objects.get(email=input.email, is_admin=False)
        # manager.password = input.password
        manager.set_password(input.password)
        manager.status = 2
        manager.is_active = True
        manager.save()
        temp_string.delete()
        return ActivateManager(token=manager.token)


class DeleteManager(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)

    ok = graphene.Boolean(required=True)

    @staticmethod
    def mutate(root, info, id):
        id_o, role, admin = getIDRoleAdmin(isAuth(info))
        if admin != True:
            raise EH.customError("Ошибка", "не достаточно прав")
        if id_o == id:
            raise EH.customError("Ошибка", "без директора никак :(")
        Manager.objects.filter(id=id, hotel=Manager.objects.get(id=id_o).hotel, is_admin=False).update(
            is_active=False, status=1
        )
        return DeleteManager(ok=True)


class DeleteAccountManager(graphene.Mutation):
    ok = graphene.Boolean(required=True)

    def mutate(root, info):
        id_o, role, admin = getIDRoleAdmin(isAuth(info))
        if str(role) != "1":
            raise EH.customError("Ошибка", "нет прав доступа")
        Manager.objects.filter(id=id_o).update(is_active=False)
        return DeleteAccountManager(ok=True)


class MutationManagerActivate(graphene.ObjectType):
    manager_deactivate_manager = DeleteManager.Field(required=True)
    manager_activate = ActivateManager.Field(required=True)
    manager_delete_account = DeleteAccountManager.Field(required=True)
