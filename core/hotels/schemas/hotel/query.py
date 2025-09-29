import graphene
from ..schema_handler import isAuth, getIDRole
from ...models import Hotel
from .types import HotelType
from .input import inputForQueryById
from ...scripts import exception_handler as EH


class QueryHotel(graphene.ObjectType):

    hotel_by_id = graphene.Field(HotelType, required=True, input=inputForQueryById(required=True))
    executer_get_customer_location_list = graphene.List(graphene.NonNull(HotelType), required=True)
    executer_get_customer_by_id = graphene.Field(HotelType, required=True, input=inputForQueryById(required=True))


    def resolve_hotel_by_id(self, info, input):
        isAuth(info)
        hotel = Hotel.objects.filter(id=input.id).first()
        if hotel:
            return hotel
        else:
            raise EH.customError("Такого заказчика не сущетсвует!")

    def resolve_executer_get_customer_location_list(self, info):
        isAuth(info)
        return Hotel.objects.filter(status='STEP_3_VERIFIED')

    def resolve_executer_get_customer_by_id(self, info, input):
        isAuth(info)
        customer = Hotel.objects.filter(id=input.id).first()
        if customer:
            return customer
        else:
            raise EH.customError("Такой гостиницы не сущетсвует!")
