from .type import PostType
import graphene
from graphene_django.fields import DjangoConnectionField
from ..schema_handler import isAuth, getIDRole, is_admin
from .input import InputForQueryPostWithFilters
from ...models import Post, TypeVisible, RoleAdmin


class QueryPost(graphene.ObjectType):
    all_get_posts = DjangoConnectionField(PostType, required=True)
    admin_get_posts = DjangoConnectionField(PostType, input=InputForQueryPostWithFilters(required=False), required=True)


    def resolve_all_get_posts(self, info, **kwargs):
        _, role = getIDRole(isAuth(info))
        posts = Post.objects.filter(is_public=True).order_by('-id')
        if role == 1:
            # менеджер
            posts = posts.exclude(visible=TypeVisible.EXECUTOR.value)
        else:
            posts = posts.exclude(visible=TypeVisible.MANAGER.value)
        return posts


    def resolve_admin_get_posts(self, info, input, **kwargs):
        is_admin(info=info, permission=[RoleAdmin.Roles.SEO.value], model=True)
        posts = Post.objects.filter(visible=input.visible).order_by('-id')
        if input.date:
            posts = posts.filter(create_at__date=input.date.date())
        if input.is_public:
            posts = posts.filter(is_public=input.is_public)
        if input.title:
            posts = posts.filter(title__icontains=input.title)

        return posts
