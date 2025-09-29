import graphene
from hotels.models import FCMToken

from .input import InputForLogout


class Logout(graphene.Mutation):
    """
    Выход из системы
    """

    class Meta:
        output = graphene.Boolean

    class Arguments:
        input = InputForLogout(required=True)

    @staticmethod
    def mutate(root, info, input):
        if input.fcm_token:
            FCMToken.objects.filter(token=input.fcm_token).delete()
        return True


class MutationAuth(graphene.ObjectType):
    logout = Logout.Field(required=True)
