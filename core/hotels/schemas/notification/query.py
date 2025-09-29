import graphene
from graphene_django import DjangoConnectionField

from ...models import Notification
from .input import InputForQueryNotification
from .type import NotifyType
from ..schema_handler import getIDRole, isAuth


class QueryNotification(graphene.ObjectType):
    """
    Запросы Уведомлений
    """
    get_read_notifications = DjangoConnectionField(
        NotifyType, required=True,
        input=InputForQueryNotification(required=True,
                                        description='Параметры запроса Уведомлений'),
        description='Получить все прочитанные уведомления')
    get_unread_notifications = graphene.List(
        graphene.NonNull(NotifyType), required=True,
        input=InputForQueryNotification(required=True,
                                        description='Параметры запроса Уведомлений'),
        description='Получить все непрочитанные уведомления')
    get_count_unread_notifications = graphene.Int(
        required=True,  # input=InputForQueryNotification(required=True,
        #                               description='Параметры запроса Уведомлений'),
        description='Получить количество всех непрочитанных уведомлений')
    get_all_notifications = DjangoConnectionField(
        NotifyType, required=True,
        input=InputForQueryNotification(required=True,
                                        description='Параметры запроса Уведомлений'),
        description='Получить все уведомления')

    def resolve_get_count_unread_notifications(self, info):
        # получение роли и идентификатора
        id, role = getIDRole(isAuth(info))
        # возвращаем количество непрочитанных уведомлений
        return Notification.objects.filter(id_instance=id,
                                           role=Notification.ROLES[role - 1][0],
                                           read=False).count()

    def resolve_get_read_notifications(self, info, input, **kwargs):
        # получение роли и идентификатора
        id, role = getIDRole(isAuth(info))
        # возвращаем все прочитанные уведомления
        res = Notification.objects.filter(id_instance=id,
                                          role=Notification.ROLES[role - 1][0]).order_by("created_at").reverse()
        if input.type:
            res = res.filter(type=input.type)
        return res

    def resolve_get_unread_notifications(self, info, input):
        # получение роли и идентификатора
        id, role = getIDRole(isAuth(info))
        #
        # if str(role) == '2':
        #     object = Executer.objects.get(id=id)
        #     role = 'executer'
        #
        # if str(role) == '1':
        #     object = Manager.objects.get(id=id)
        #     role = 'manager'
        res = Notification.objects.filter(id_instance=id,
                                          role=Notification.ROLES[role - 1][0],
                                          read=False).order_by("created_at").reverse()
        if input.type:
            res = res.filter(type=input.type)

        return res
    def resolve_get_unread_notifications(self, info, input, **kwargs):
        # получение роли и идентификатора
        id, role = getIDRole(isAuth(info))
        # возвращаем все прочитанные уведомления
        res = Notification.objects.filter(id_instance=id,
                                          role=Notification.ROLES[role - 1][0]).order_by("created_at").reverse()
        if input.type:
            res = res.filter(type=input.type)
        return res
