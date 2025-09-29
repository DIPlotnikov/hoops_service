from .type import SessionType
import graphene
from graphene_django.fields import DjangoConnectionField
from ..schema_handler import isAuth, getIDRole
from .input import InputForQueryPostWithFilters
from ...models import Post, TypeVisible


class QueryPost(graphene.ObjectType):
    get_my_sessions = DjangoConnectionField(PostType, required=True)
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
