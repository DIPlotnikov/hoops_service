import graphene
from ..scalars import INN, Email
from ...models import RoleManager


class managerInputResend(graphene.InputObjectType):
    email = graphene.String(required=True)

class inputEmail(graphene.InputObjectType):
    email = graphene.String(required=True)


class InputForCreateManager(graphene.InputObjectType):
    email = Email(required=True, description='email менеджера')
    roles = graphene.List(graphene.NonNull(RoleManager.RolesManagerEnum), required=True, description='Роли Менеджера ко всем заявкам')


class InputForUpdateManagerRoles(graphene.InputObjectType):
    id = graphene.ID(required=True, description='ID менеджера')
    roles = graphene.List(graphene.NonNull(RoleManager.RolesManagerEnum), required=True,
                          description='Роли Менеджера ко всем заявкам')

class inputInnPassword(graphene.InputObjectType):
    inn = INN(required=True)
    password = graphene.String(required=True)

class inputEmailPassword(inputEmail):
    password = graphene.String(required=True)

# Create Input Object Types


class managerInputForActivate(graphene.InputObjectType):
    email = graphene.String(required=True)
    password = graphene.String(required=True)
    secret = graphene.String(required=True)


class managerInputForUpdate(graphene.InputObjectType):
    #email = graphene.String(required=True)
    first_name = graphene.String(required=True)
    second_name = graphene.String(required=True)
    middle_name = graphene.String(required=True)
    #password = graphene.String()


class inputInnEmail(graphene.InputObjectType):
    inn = INN(required=True)
    email = graphene.String(required=True)


class inputInnEmailSecret(inputInnEmail):
    secret = graphene.String(required=True)
    new_password = graphene.String(required=True)


class inputSetNewPasswordManager(graphene.InputObjectType):
    old_password = graphene.String(required=True)
    new_password = graphene.String(required=True)

class inputExecuterID(graphene.InputObjectType):
    id = graphene.ID(required=True)
