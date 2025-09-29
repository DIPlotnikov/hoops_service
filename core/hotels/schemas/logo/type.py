from graphene_django.types import DjangoObjectType
from ...models import Logo
from ..schema_fileinfo import FileInfoType
from graphene.types import List, NonNull, ID


class LogoType(DjangoObjectType):
    """
    Логотип
    """
    class Meta:
        model = Logo
        # interfaces = (relay.Node,)
        # connection_class = ExtendedConnection
        exclude = ('file', 'admin')
    id = ID(required=True)
    files = List(NonNull(FileInfoType), required=True)

    def resolve_id(self, info):
        return self.hotel.id

    def resolve_files(self, info):
        if self.file:
            return [self.file]
        return []

