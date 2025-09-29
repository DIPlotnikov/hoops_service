from graphene_django.types import DjangoObjectType
from ...models import InfoBlock, TypeVisibleEnum
from graphene import relay, ID
from ..pagination import ExtendedConnection

class InfoBlockType(DjangoObjectType):
    class Meta:
        model = InfoBlock
        exclude = ('admin',)
        interfaces = (relay.Node,)
        connection_class = ExtendedConnection


    visible = TypeVisibleEnum(required=True)
    id = ID(required=True)

    def resolve_id(self, info):
        return self.id