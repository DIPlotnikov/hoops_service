import graphene
from django.utils import timezone

from ....models import Manager, TempString
from ....scripts import exception_handler as EH
from ....tasks import send_recovery_message
from ...schema_handler import getIDRoleAdmin, isAuth
from ..input import inputInnEmail, inputInnEmailSecret, inputSetNewPasswordManager
from ..type import ManagerType


class RequestToRecoveryPasswordByInnEmail(graphene.Mutation):
    class Arguments:
        input = inputInnEmail(required=True)

    ok = graphene.Boolean(required=True)

    @staticmethod
    def mutate(root, info, input):
        manager = Manager.objects.filter(email=input.email, hotel__inn=input.inn, is_active=True).first()
        if not manager:
            raise ValueError("Такого менеджера нет у нас...")
        metka = manager.metka
        send_recovery_message.delay(
            email=input.email, Name="manager", text=f"{metka}/{input.inn}", url=info.context.headers.get("Origin")
        )
        return RequestToRecoveryPasswordByInnEmail(ok=True)


class RecoveryPasswordByInnEmail(graphene.Mutation):
    class Arguments:
        input = inputInnEmailSecret(required=True)

    token = graphene.String(required=True)

    @staticmethod
    def mutate(root, info, input):

        manager = Manager.objects.filter(email=input.email, hotel__inn=input.inn, is_active=True).first()
        if not manager:
            raise ValueError("Такого менеджера нет у нас...")

        tempString = TempString.objects.filter(first_field=input.email, second_field=input.secret).first()

        if not tempString:
            raise ValueError("Что-то пошло не так...")
        # manager.password = input.new_password
        manager.set_password(input.new_password)
        manager.update_password_at = timezone.now()
        manager.save()

        return RecoveryPasswordByInnEmail(token=manager.token)


class SetNewPasswordManager(graphene.Mutation):
    class Arguments:
        input = inputSetNewPasswordManager(required=True)

    manager = graphene.NonNull(ManagerType)

    def mutate(root, info, input):
        id_o, role, admin = getIDRoleAdmin(isAuth(info))
        if str(role) != "1":
            raise EH.customError("Ошибка", "нет прав доступа")
        manager = Manager.objects.get(id=id_o)
        if manager.check_password(input.old_password):
            manager.password = input.new_password
            manager.set_password(input.new_password)
            manager.update_password_at = timezone.now()
            manager.save()
        else:
            raise ValueError("Старый пароль не верный")

        return SetNewPasswordManager(manager=manager)


class MutationManagerPassword(graphene.ObjectType):
    manager_request_recovery_password_by_inn_email = RequestToRecoveryPasswordByInnEmail.Field(required=True)
    manager_recovery_password_by_inn_email = RecoveryPasswordByInnEmail.Field(required=True)
    manager_set_new_password = SetNewPasswordManager.Field(required=True)
