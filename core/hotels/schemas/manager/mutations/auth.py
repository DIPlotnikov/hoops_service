import graphene

from ....models import Manager
from ....scripts import exception_handler as EH
from ...schema_handler import set_session
from ..input import inputEmailPassword, inputInnPassword


class AuthenticateByEmail(graphene.Mutation):
    class Arguments:
        input = inputEmailPassword(required=True)

    token = graphene.String(required=True)

    @staticmethod
    def mutate(root, info, input):

        manager = Manager.objects.filter(email=input.email, is_active=True, is_admin=False).first()
        if manager is None:
            raise EH.customError("Ошибка", "не верный логин или пароль")
        if manager.check_password(input.password):
            # set_session(info, manager)
            return AuthenticateByEmail(token=manager.token)
        else:
            raise EH.customError("Ошибка", "не верный логин или пароль")


class AuthenticateByInn(graphene.Mutation):
    class Arguments:
        input = inputInnPassword(required=True)

    token = graphene.String(required=True)

    @staticmethod
    def mutate(root, info, input):

        manager = Manager.objects.filter(hotel__inn=input.inn, is_active=True, is_admin=True).first()
        if manager is None:
            raise EH.customError("Ошибка", "не верный логин или пароль")
        if manager.check_password(input.password):
            # set_session(info, manager)
            return AuthenticateByInn(token=manager.token)
        else:
            raise EH.customError("Ошибка", "не верный логин или пароль")


class MutationManagerAuth(graphene.ObjectType):
    manager_authenticate_by_email = AuthenticateByEmail.Field(required=True)
    manager_authenticate_by_inn = AuthenticateByInn.Field(required=True)
