from graphene_django.types import DjangoObjectType
from graphene import relay, ID, NonNull

from ..executer.type import ExecuterType
from ...models import ExecuterNotice
from ..pagination import ExtendedConnection


class ExecuterNoticeType(DjangoObjectType):
    class Meta:
        model = ExecuterNotice
        interfaces = (relay.Node,)
        connection_class = ExtendedConnection

    id = ID(required=True)
    executer = NonNull(ExecuterType)

    def resolve_id(self, info):
        return self.id
