from graphene_django.types import DjangoObjectType
from ...models import Post, TypeVisibleEnum
from graphene import relay, ID
from ..schema_fileinfo import FileInfoType
from ..pagination import ExtendedConnection
from graphene.types import List, NonNull


class PostType(DjangoObjectType):
    class Meta:
        model = Post
        interfaces = (relay.Node,)
        connection_class = ExtendedConnection
        exclude = ('file',)

    id = ID(required=True)
    visible = TypeVisibleEnum(required=True)
    files = List(NonNull(FileInfoType), required=True)

    def resolve_id(self, info):
        return self.id

    def resolve_files(self, info):
        if self.file:
            return [self.file]
        return []