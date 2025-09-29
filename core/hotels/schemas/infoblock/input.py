import graphene
from ..schema_fileinfo import fileInfoInput
from ...models import TypeVisibleEnum


class InputForUpsertInfoBlock(graphene.InputObjectType):
    id = graphene.ID(required=False)
    title = graphene.String(required=True)
    content = graphene.String(required=True)
    files = graphene.List(graphene.NonNull(fileInfoInput), required=True)
    visible = graphene.NonNull(TypeVisibleEnum)
    category = graphene.String(required=True)
    weight = graphene.Int(required=False)


class InputForQueryInfoBlocksWithFilters(graphene.InputObjectType):
    title = graphene.String(required=False)
    is_public = graphene.Boolean(required=False)
    date = graphene.DateTime(required=False)
    visible = graphene.NonNull(TypeVisibleEnum)
    category = graphene.String(required=False)
    weight = graphene.Int(required=False)
