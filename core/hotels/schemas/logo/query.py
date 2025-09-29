from .type import LogoType
import graphene

from ..input import InputID
from ..schema_handler import is_admin
from ...models import Logo, Hotel, RoleAdmin


class QueryLogo(graphene.ObjectType):
    all_logo = graphene.List(graphene.NonNull(LogoType), required=True, description='Логотипы для всех')
    admin_get_logo = graphene.List(graphene.NonNull(LogoType),
                                   required=True, description='Логотипы для Администраторов')
    admin_get_logo_by_id = graphene.NonNull(LogoType,
                                            input=InputID(required=True),
                                            description='Логотипы для Администраторов')

    def resolve_all_logo(self, info, **kwargs):
        res = Logo.objects.filter(is_visible=True)
        return res

    def resolve_admin_get_logo(self, info, **kwargs):
        is_admin(info=info, permission=RoleAdmin.Roles.CUSTOMER.value)
        return Logo.objects.filter(is_visible=True)

    def resolve_admin_get_logo_by_id(self, info,input):
        is_admin(info=info, permission=RoleAdmin.Roles.CUSTOMER.value)
        hotel = Hotel.objects.select_related('logo').get(id=input.id)
        logo = hotel.logo
        if logo is None:
            logo = Logo()
            logo.file = None
            logo.hotel = hotel
        return logo
