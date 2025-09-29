from .type import InfoBlockType
import graphene
from graphene_django.fields import DjangoConnectionField
from ..schema_handler import isAuth, getIDRole, is_admin
from .input import InputForQueryInfoBlocksWithFilters
from ...models import InfoBlock, TypeVisible, RoleAdmin


class QueryInfoBlock(graphene.ObjectType):
    all_get_info_blocks = graphene.List(graphene.NonNull(InfoBlockType), required=True)
    admin_get_info_blocks = DjangoConnectionField(InfoBlockType, input=InputForQueryInfoBlocksWithFilters(required=False), required=True)
    all_get_category_info_blocks = graphene.List(graphene.NonNull(graphene.String), required=True)

    def resolve_all_get_info_blocks(self, info):
        _, role = getIDRole(isAuth(info))
        info_blocks = InfoBlock.objects.filter(is_public=True).order_by('-weight')
        if role == 1:
            # менеджер
            info_blocks = info_blocks.exclude(visible=TypeVisible.EXECUTOR.value)
        else:
            info_blocks = info_blocks.exclude(visible=TypeVisible.MANAGER.value)
        return info_blocks


    def resolve_admin_get_info_blocks(self, info, input,  **kwargs):
        is_admin(info=info, permission=[RoleAdmin.Roles.SEO.value])
        info_blocks = InfoBlock.objects.filter(visible=input.visible).order_by('-weight')
        if input.date:
            info_blocks = info_blocks.filter(create_at__date=input.date.date())
        if input.is_public:
            info_blocks = info_blocks.filter(is_public=input.is_public)
        if input.title:
            info_blocks = info_blocks.filter(title__icontains=input.title)
        if input.category:
            info_blocks = info_blocks.filter(title__icontains=input.category)
        if input.weight:
            info_blocks = info_blocks.filter(title__icontains=input.weight)
        return info_blocks


    def resolve_all_get_category_info_blocks(self, info):
        _, role = getIDRole(isAuth(info))
        info_blocks = InfoBlock.objects.filter(is_public=True).order_by('-weight')
        if role == 1:
            # менеджер
            info_blocks = info_blocks.exclude(visible=TypeVisible.EXECUTOR.value)
        else:
            info_blocks = info_blocks.exclude(visible=TypeVisible.MANAGER.value)
        return set(info_blocks.values_list('category', flat=True))