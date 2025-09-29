import graphene
from django.db.models import Q
from django.db.models import Value as V
from django.db.models.functions import Concat
from graphene_django.fields import DjangoConnectionField

from ..input import (
    inputEmailAndInn,
    InputINN,
    InputNameHotel,
    InputNameOrInn,
    InputForQueryAllHotels,
    InputForFilterHotels,
)
from ..type import hotelForAdmin, managerForAdmin
from ...input import InputID
from ...schema_handler import is_admin
from ....models import Hotel, Manager, RoleAdmin


class QueryAdminHotel(graphene.ObjectType):
    admin_all_hotels = DjangoConnectionField(
        hotelForAdmin,
        input=InputForQueryAllHotels(required=False),
        required=True,
        description="Получение всех Гостиниц с фильтром",
    )

    admin_all_managers = DjangoConnectionField(managerForAdmin, input=inputEmailAndInn(required=False), required=True)

    admin_get_hotel_by_inn = graphene.List(
        graphene.NonNull(hotelForAdmin),
        input=InputINN(required=True),
        required=True,
        deprecation_reason="admin_filter_hotel_by_whatever",
    )
    admin_get_hotel_by_id = graphene.NonNull(
        hotelForAdmin, input=InputID(required=True), description="Получение Гостиницы по ID"
    )
    admin_get_hotel_by_name = graphene.List(
        graphene.NonNull(hotelForAdmin),
        input=InputNameHotel(required=True),
        required=True,
        deprecation_reason="admin_filter_hotel_by_whatever",
    )
    admin_get_hotel_by_name_or_inn = graphene.List(
        graphene.NonNull(hotelForAdmin),
        input=InputNameOrInn(required=True),
        required=True,
        deprecation_reason="admin_filter_hotel_by_whatever",
    )
    admin_filter_hotel_by_whatever = graphene.List(
        graphene.NonNull(hotelForAdmin), input=InputForFilterHotels(required=True), required=True
    )

    def resolve_admin_all_hotels(self, info, input, **kwargs):
        is_admin(info=info, permission=RoleAdmin.Roles.CUSTOMER.value)
        hotels = Hotel.objects.all()
        if input.is_test is not None:
            hotels = hotels.filter(is_test=input.is_test)
        if input.id:
            hotels = hotels.filter(id=input.id)
        if input.email:
            hotels = hotels.filter(email__icontains=input.email)
        if input.nameHotel:
            hotels = hotels.filter(nameHotel__icontains=input.nameHotel)
        if input.nameLegalEntity:
            hotels = hotels.filter(nameLegalEntity__icontains=input.nameLegalEntity)
        if input.inn:
            hotels = hotels.filter(inn__icontains=input.inn)
        if input.status:
            hotels = hotels.filter(status=input.status)
        return hotels

    def resolve_admin_all_managers(self, info, input, **kwargs):
        is_admin(info=info, permission=RoleAdmin.Roles.CUSTOMER.value)

        managers = Manager.objects.select_related("hotel").all().exclude(status__in=[0, 1]).exclude(is_active=False)
        if input.is_test is not None:
            managers = managers.filter(hotel__is_test=input.is_test)
        if input.manager_email:
            managers = managers.filter(email__icontains=input.manager_email)
        if input.inn:
            managers = managers.filter(hotel__inn__icontains=input.inn)
        if input.id:
            managers = managers.filter(id=input.id)
        if input.hotel_name:
            managers = managers.filter(
                Q(hotel__nameLegalEntity__icontains=input.hotel_name) | Q(hotel__nameHotel__icontains=input.hotel_name)
            )
        if input.hotel_id:
            managers = managers.filter(hotel__id=input.hotel_id)
        if input.manager_full_name:
            managers = managers.annotate(
                full_name=Concat("first_name", V(" "), "second_name", V(" "), "middle_name")
            ).filter(full_name__icontains=input.manager_full_name)
        return managers

    def resolve_admin_filter_hotel_by_whatever(self, info, input):
        is_admin(info=info, permission=RoleAdmin.Roles.CUSTOMER.value)
        filters = [Q(is_active=True)]
        if input.id:
            filters.append(Q(id=input.id))
        if input.inn:
            filters.append(Q(inn__contains=input.inn))
        if input.name:
            filters.append(Q(nameHotel__icontains=input.name))
        if input.innOrName:
            filters.append(Q(inn__contains=input.innOrName) | Q(nameHotel__icontains=input.innOrName))
        return Hotel.objects.filter(*filters)[:10]

    def resolve_admin_get_hotel_by_inn(self, info, input):
        is_admin(info=info, permission=RoleAdmin.Roles.CUSTOMER.value)
        return Hotel.objects.filter(inn__contains=input.inn)[:10]

    def resolve_admin_get_hotel_by_id(self, info, input):
        is_admin(info=info, permission=RoleAdmin.Roles.CUSTOMER.value)
        return (
            Hotel.objects.select_related("profile_pic", "coordinates", "requisites")
            .prefetch_related("manager_set")
            .get(id=input.id)
        )

    def resolve_admin_get_hotel_by_name(self, info, input):
        is_admin(info=info, permission=RoleAdmin.Roles.CUSTOMER.value)
        return Hotel.objects.filter(nameHotel__icontains=input.nameHotel)[:10]

    def resolve_admin_get_hotel_by_name_or_inn(self, info, input):
        is_admin(info=info, permission=RoleAdmin.Roles.CUSTOMER.value)
        return Hotel.objects.filter(Q(nameHotel__icontains=input.nameOrInn) | Q(inn__icontains=input.nameOrInn))[:10]
