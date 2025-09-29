import graphene
from graphene import ObjectType, relay
from graphene_django import DjangoObjectType

from ...models import MetaInformationNotification, Notification
from ..pagination import ExtendedConnection


class MetaType(DjangoObjectType):
    class Meta:
        model = MetaInformationNotification
        exclude = ("notification",)


class NotifyType(DjangoObjectType):
    """
    Уведомление
    """

    class Meta:
        model = Notification
        interfaces = (relay.Node,)
        connection_class = ExtendedConnection
        exclude = ("role",)

    category = graphene.String(required=True, description="Категория", deprecation_reason="Переход к типам")
    meta = graphene.Field(MetaType)

    def resolve_category(self, info):
        return self.type
