import graphene
from .input import InputForUpsertPost
from ..input import InputID
from .type import PostType, Post
from ..schema_handler import is_admin
from ...models import FileInfo, Executer, Notification, TypeVisible, Manager, RoleAdmin


class UpsertPost(graphene.Mutation):
    class Arguments:
        input = InputForUpsertPost(required=True)

    post = graphene.NonNull(PostType)

    @staticmethod
    def mutate(root, info, input):
        admin = is_admin(info=info, permission=[RoleAdmin.Roles.SEO.value], model=True)
        if input.id:
            post = Post.objects.get(id=input.id)
        else:
            post = Post()
        post.admin = admin
        post.title = input.title
        post.content = input.content
        post.visible = input.visible
        post.save()
        if post.file:
            file = post.file
            file.delete()
        if input.files:
            file_info = FileInfo(**input.files[0])
            file_info.save()
            post.file = file_info
        post.save()
        return UpsertPost(post=post)


class PublishPost(graphene.Mutation):
    class Arguments:
        input = InputID(required=True)

    post = graphene.NonNull(PostType)

    def mutate(root, info, input):
        is_admin(info=info, permission=RoleAdmin.Roles.SEO.value)
        post = Post.objects.filter(**input)
        post.update(is_public=True)
        if post.first().visible != TypeVisible.MANAGER.value:
            for executer in Executer.objects.filter(is_active=True):
                notify = Notification(type=Notification.TypeNotification.OTHER,
                                      id_instance=executer.pk, role='executer', read=False,
                                      text=f'В HOOPS Service новая новость!')
                notify.save(notification=True, url='news')
        if post.first().visible != TypeVisible.EXECUTOR.value:
            for manager in Manager.objects.filter(is_active=True):
                notify = Notification(type=Notification.TypeNotification.OTHER,
                                      id_instance=manager.pk, role='manager', read=False,
                                      text=f'В HOOPS Service новая новость!')
                notify.save(notification=True, url='news')
        return PublishPost(post=post.first())


class UnpublishPost(graphene.Mutation):
    class Arguments:
        input = InputID(required=True)

    post = graphene.NonNull(PostType)

    def mutate(root, info, input):
        is_admin(info=info, permission=RoleAdmin.Roles.SEO.value)
        post = Post.objects.filter(**input)
        post.update(is_public=False)
        return PublishPost(post=post.first())


class DeletePost(graphene.Mutation):
    class Arguments:
        input = InputID(required=True)

    ok = graphene.Boolean(required=True)

    def mutate(root, info, input):
        is_admin(info=info, permission=RoleAdmin.Roles.SEO.value)
        post = Post.objects.filter(**input)
        post.delete()
        return DeletePost(ok=True)


class MutationPost(graphene.ObjectType):
    admin_upsert_post = UpsertPost.Field(required=True)
    admin_publish_post = PublishPost.Field(required=True)
    admin_unpublish_post = UnpublishPost.Field(required=True)
    admin_delete_post = DeletePost.Field(required=True)

