from graphene_django.types import DjangoObjectType
from ...models import Notice
from graphene import relay, Int, Connection, ID, NonNull
from ..admin.type import hotelForAdmin
from ..pagination import ExtendedConnection


class NoticeType(DjangoObjectType):
    class Meta:
        model = Notice
        interfaces = (relay.Node,)
        connection_class = ExtendedConnection

    id = ID(required=True)
    hotel = NonNull(hotelForAdmin)

    def resolve_id(self, info):
        return self.id
