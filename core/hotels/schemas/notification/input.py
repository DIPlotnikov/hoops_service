import graphene

from ...models import Notification


class InputForQueryNotification(graphene.InputObjectType):
    """
    Параметры получения Уведомлений
    """

    type = Notification.TypeNotificationEnum(required=False, description='Тип уведомления')
