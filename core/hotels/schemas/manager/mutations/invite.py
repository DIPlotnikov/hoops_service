import graphene

from ....models import Manager, RoleManager
from ....tasks import send_simple_message
from ...schema_handler import is_manager
from ..input import InputForCreateManager, inputEmail
from ..type import ManagerType


class CreateManager(graphene.Mutation):
    class Arguments:
        input = InputForCreateManager(required=True)

    class Meta:
        description = "Приглашение менеджера с указанием ролей"
        output = graphene.Boolean

    @staticmethod
    def mutate(root, info, input):
        manager_admin = is_manager(info=info, permission=["SETTINGS_EDIT"])
        new_manager = Manager.objects.filter(email=input.email).first()
        if new_manager:
            assert new_manager.hotel != manager_admin.hotel, f'Менеджер уже значится в "{new_manager.hotel.nameHotel}"'
            assert new_manager.is_active, "Это действующий сотрудник"
        new_manager = Manager(email=input.email, hotel=manager_admin.hotel, is_active=True, status=0)
        new_manager.save()
        send_simple_message.delay(
            email=input.email, Name="manager", text=new_manager.metka, url=info.context.headers.get("Origin")
        )

        for role in input.roles:
            RoleManager.objects.create(manager=new_manager, role=role)

        return True


class CancelInvate(graphene.Mutation):
    class Arguments:
        input = inputEmail(required=True)

    manager = graphene.NonNull(ManagerType)

    @staticmethod
    def mutate(root, info, input):
        manager = is_manager(info=info, permission=["SETTINGS_EDIT"])
        manager = Manager.objects.get(email=input.email, hotel=manager.hotel)
        manager.is_active = False
        manager.status = 1
        manager.save()
        return CancelInvate(manager=manager)


class ResendInvate(graphene.Mutation):
    class Arguments:
        input = inputEmail(required=True)

    metka = graphene.String(required=True)

    @staticmethod
    def mutate(root, info, input):
        manager = is_manager(info=info, permission=["SETTINGS_EDIT"])
        manager = Manager.objects.get(email=input.email, hotel=manager.hotel, is_active=True, is_admin=False)
        metka = manager.metka
        send_simple_message.delay(
            email=input.email, Name="manager", text=metka, url=info.context.headers.get("Origin")
        )
        return ResendInvate(metka=metka)


class MutationManagerInvite(graphene.ObjectType):
    manager_create_new_manager = CreateManager.Field(required=True)
    manager_cancel_invite = CancelInvate.Field(required=True)
    manager_resend_invite = ResendInvate.Field(required=True)
