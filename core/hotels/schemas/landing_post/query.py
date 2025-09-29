from django.db.models import Q

from .type import PostLandingType
import graphene
from graphene_django.fields import DjangoConnectionField

from ..input import InputID, InputURL
from ..schema_handler import is_admin
from .input import InputForQueryPostLandingWithFilters
from ...models import PostLanding, RoleAdmin


class QueryPostLanding(graphene.ObjectType):
    all_get_posts_landing = DjangoConnectionField(PostLandingType,
                                                  description='Все посты для лендинга',
                                                  required=True)
    admin_get_posts_landing = DjangoConnectionField(PostLandingType,
                                                    description='Все посты для лендинга для Администратора',
                                                    input=InputForQueryPostLandingWithFilters(required=False),
                                                    required=True)

    all_get_post_landing_by_url = graphene.NonNull(PostLandingType,
                                                   description='Пост лендинга по ID для Администратора',
                                                   input=InputURL(required=True))

    def resolve_all_get_posts_landing(self, info, **kwargs):
        return PostLanding.objects.filter(is_public=True).order_by('-id')


    def resolve_admin_get_posts_landing(self, info, input, **kwargs):
        is_admin(info=info, permission=RoleAdmin.Roles.SEO.value)
        filters = []
        if input.date:
            filters.append(Q(create_at__date=input.date.date()))
        if input.is_public is not None:
            filters.append(Q(is_public=input.is_public))
        if input.title:
            filters.append(Q(title__icontains=input.title))
        return PostLanding.objects.filter(*filters).order_by('-id')

    def resolve_all_get_post_landing_by_url(self, info, input):
        post = PostLanding.objects.filter(url=input.url, is_public=True).first()
        assert post is not None, 'Пост не найден'
        return post

