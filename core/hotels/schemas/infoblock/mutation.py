import graphene
from .input import InputForUpsertInfoBlock
from ..input import InputID
from .type import InfoBlockType
from ..schema_handler import is_admin
from ...models import FileInfo, InfoBlock, RoleAdmin


class UpsertInfoBlock(graphene.Mutation):
    class Arguments:
        input = InputForUpsertInfoBlock(required=True)

    info_block = graphene.NonNull(InfoBlockType)

    @staticmethod
    def mutate(root, info, input):
        admin = is_admin(info=info, permission=RoleAdmin.Roles.SEO.value, model=True)
        if input.id:
            info_block = InfoBlock.objects.get(id=input.id)
        else:
            info_block = InfoBlock()
        info_block.admin = admin
        info_block.title = input.title
        info_block.content = input.content
        info_block.visible = input.visible
        info_block.weight = input.weight if input.weight is not None else 0
        info_block.category = input.category
        info_block.save()
        info_block.files.all().delete()
        for file in input.files:
            fileInfo, _ = FileInfo.objects.get_or_create(**file)
            fileInfo.save()
            info_block.files.add(fileInfo)
            info_block.save()
        return UpsertInfoBlock(info_block=info_block)


class PublishInfoBlock(graphene.Mutation):
    class Arguments:
        input = InputID(required=True)

    info_block = graphene.NonNull(InfoBlockType)

    def mutate(root, info, input):
        is_admin(info=info, permission=RoleAdmin.Roles.SEO.value)
        info_block = InfoBlock.objects.filter(**input)
        info_block.update(is_public=True)
        return PublishInfoBlock(info_block=info_block.first())


class UnpublishInfoBlock(graphene.Mutation):
    class Arguments:
        input = InputID(required=True)

    info_block = graphene.NonNull(InfoBlockType)

    def mutate(root, info, input):
        is_admin(info=info, permission=RoleAdmin.Roles.SEO.value)
        info_block = InfoBlock.objects.filter(**input)
        info_block.update(is_public=False)
        return PublishInfoBlock(info_block=info_block.first())


class DeleteInfoBlock(graphene.Mutation):
    class Arguments:
        input = InputID(required=True)

    ok = graphene.Boolean(required=True)

    def mutate(root, info, input):
        is_admin(info=info, permission=RoleAdmin.Roles.SEO.value)
        info_block = InfoBlock.objects.filter(**input)
        info_block.delete()
        return DeleteInfoBlock(ok=True)


class MutationInfoBlock(graphene.ObjectType):
    admin_upsert_info_block = UpsertInfoBlock.Field(required=True)
    admin_publish_info_block = PublishInfoBlock.Field(required=True)
    admin_unpublish_info_block = UnpublishInfoBlock.Field(required=True)
    admin_delete_info_block = DeleteInfoBlock.Field(required=True)

