import graphene

from ...models import Notification
from ..schema_handler import getIDRole, isAuth


class ReadNotify(graphene.Mutation):
    """
    Мутация прочтения уведомелний
    """

    # возвращаемое значение - флаг успеха
    ok = graphene.Boolean(required=True)

    @staticmethod
    def mutate(root, info):
        # получение роли и идентификатора
        id_o, role = getIDRole(isAuth(info))
        # получаем Уведомления обьекта
        notify = Notification.objects.filter(id_instance=id_o, role=Notification.ROLES[role - 1][0], read=False)
        # отмечаем их всех прочитанными
        notify.update(read=True)
        return ReadNotify(ok=True)


class MutationNotify(graphene.ObjectType):
    notification_read = ReadNotify.Field(required=True, description="Пометить все уведомления прочитанными")
