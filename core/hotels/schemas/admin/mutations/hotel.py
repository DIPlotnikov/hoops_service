import graphene

from ..input import InputForMarkObjectsAsTest, InputForSetSettingsHotel
from ..type import hotelForAdmin
from ...input import InputIdDatetime
from ...schema_handler import is_admin
from ....models import Hotel, Notification, Manager, RoleAdmin


class ConfirmHotelPayment(graphene.Mutation):
    """
    Подтверждение платежа Гостиницы
    """

    class Arguments:
        id = InputIdDatetime(required=True)

    hotel = graphene.Field(graphene.NonNull(hotelForAdmin))

    @staticmethod
    def mutate(root, info, id):
        is_admin(info=info, permission=RoleAdmin.Roles.CUSTOMER.value)
        hotel = Hotel.objects.get(id=id.id)
        hotel.accept(id.datetime)
        return ConfirmHotelPayment(hotel=hotel)


class denyUserPayment(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        text = graphene.String(required=True)

    hotel = graphene.Field(graphene.NonNull(hotelForAdmin))

    @staticmethod
    def mutate(root, info, id, text):
        is_admin(info=info, permission=RoleAdmin.Roles.CUSTOMER.value)

        hotel = Hotel.objects.get(id=id)
        # if Hotel.status == 'STEP_3_VERIFIED':
        #     raise EH.customError("Ошибка", "реквизиты подтверждены ранее")
        hotel.status = "STEP_3_VERIFICATION_DECLINED"
        hotel.save()

        notify = Notification(
            text=text,
            id_instance=Manager.objects.get(hotel=hotel, is_admin=True).pk,
            role="customer",
            type=Notification.TypeNotification.ACCOUNT,
        )

        notify.save()
        return denyUserPayment(hotel=hotel)


class MarkHotelsAsTest(graphene.Mutation):
    class Arguments:
        input = InputForMarkObjectsAsTest(required=True)

    hotels = graphene.List(graphene.NonNull(hotelForAdmin), required=True)

    @staticmethod
    def mutate(root, info, input):
        is_admin(info=info, permission=RoleAdmin.Roles.CUSTOMER_TEST.value)
        hotels = Hotel.objects.filter(id__in=input.ids)
        hotels.update(is_test=input.is_test)
        return MarkHotelsAsTest(hotels=hotels)


class SetSettingsHotel(graphene.Mutation):
    class Arguments:
        input = InputForSetSettingsHotel(
            required=True, description="Инпут для указания настроек у гостиницы Администратором"
        )

    hotel = graphene.NonNull(hotelForAdmin)

    @staticmethod
    def mutate(root, info, input):
        is_admin(info=info, permission=RoleAdmin.Roles.CUSTOMER.value)
        hotel = Hotel.objects.filter(id=input.id)
        assert len(hotel) == 1, "Не верный идентификатор гостиницы"
        hotel.update(**input)
        return SetSettingsHotel(hotel=hotel.first())


class MutationAdminHotel(graphene.ObjectType):
    admin_confirm_hotel_payment = ConfirmHotelPayment.Field(required=True, description="Подтверждение платежа")
    admin_deny_hotel_payment = denyUserPayment.Field(required=True, description="Отказ в подтверждении платежа")
    admin_mark_hotel_as_test_by_list_of_id = MarkHotelsAsTest.Field(
        required=True, description="Пометка Гостиницы тестовой"
    )
    admin_set_settings_by_hotel_id = SetSettingsHotel.Field(
        required=True, description="Установка настроек у Гостиницы Администратором"
    )
