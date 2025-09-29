import graphene
from .input import InputForUpsertPostLanding
from ..input import InputID
from .type import PostLandingType
from ..schema_handler import is_admin
from ...models import FileInfo, PostLanding, RoleAdmin


class UpsertPostLanding(graphene.Mutation):
    class Arguments:
        input = InputForUpsertPostLanding(required=True)

    post = graphene.NonNull(PostLandingType)

    @staticmethod
    def mutate(root, info, input):
        admin = is_admin(info=info, permission=RoleAdmin.Roles.SEO.value, model=True)
        if input.id:
            post = PostLanding.objects.get(id=input.id)
        else:
            post = PostLanding()
        post.admin = admin
        post.title = input.title
        post.content = input.content
        post.hashtag = input.hashtag
        post.url = input.url

        post.save()
        if post.file:
            file = post.file
            file.delete()
        if input.files:
            file_info = FileInfo(**input.files[0])
            file_info.save()
            post.file = file_info
        post.save()
        return UpsertPostLanding(post=post)


class PublishPostLanding(graphene.Mutation):
    class Arguments:
        input = InputID(required=True)

    post = graphene.NonNull(PostLandingType)

    def mutate(root, info, input):
        is_admin(info=info, permission=RoleAdmin.Roles.SEO.value)
        post = PostLanding.objects.filter(**input)
        post.update(is_public=True)
        return PublishPostLanding(post=post.first())


class UnpublishPostLanding(graphene.Mutation):
    class Arguments:
        input = InputID(required=True)

    post = graphene.NonNull(PostLandingType)

    def mutate(root, info, input):
        is_admin(info=info, permission=RoleAdmin.Roles.SEO.value)
        post = PostLanding.objects.filter(**input)
        post.update(is_public=False)
        return PublishPostLanding(post=post.first())


class DeletePostLanding(graphene.Mutation):
    class Arguments:
        input = InputID(required=True)

    ok = graphene.Boolean(required=True)

    def mutate(root, info, input):
        is_admin(info=info, permission=RoleAdmin.Roles.SEO.value)
        post = PostLanding.objects.filter(**input)
        post.delete()
        return DeletePostLanding(ok=True)


class MutationPostLanding(graphene.ObjectType):
    admin_upsert_post_landing = UpsertPostLanding.Field(required=True,
                                                        description='Создание и обновлние поста для лендинга')
    admin_publish_post_landing = PublishPostLanding.Field(required=True,
                                                          description='Публикация поста для лендинга')
    admin_unpublish_post_landing = UnpublishPostLanding.Field(required=True,
                                                              description='Убрать публикацию из лендинга')
    admin_delete_post_landing = DeletePostLanding.Field(required=True,
                                                        description='Удаление поста для лендинга')


