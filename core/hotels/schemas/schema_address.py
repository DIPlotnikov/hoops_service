import graphene
from graphene_django.types import DjangoObjectType

from ..models import Address, Executer
from ..scripts import exception_handler as EH
from .hotel.mutation import checkAdmin
from .hotel.types import HotelType
from .scalars import PostalCode
from .schema_coordinates import coordinatesInput
from .schema_handler import getIDRole, isAuth


class CoordinatesExecuterType(DjangoObjectType):
    class Meta:
        model = Address
        exclude = ("zoom",)


class AddressType(DjangoObjectType):
    class Meta:
        model = Address
        fields = ("id",)

    coordinates = graphene.NonNull(CoordinatesExecuterType)

    def resolve_coordinates(self, info):
        return self


class addressInput(graphene.InputObjectType):
    coordinates = coordinatesInput(required=True)


class executerSetAddress(graphene.Mutation):
    class Arguments:
        input = addressInput(required=True)

    coordinates = graphene.NonNull(AddressType)

    @staticmethod
    def mutate(root, info, input):
        token = isAuth(info)
        id, role = getIDRole(token)

        if str(role) != "2":
            raise EH.customError("Ошибка", "нет прав доступа (ошибка роли)")

        address = Address.objects.filter(executer=id).first()

        if address:
            Address.objects.filter(executer=id).update(**input.coordinates)
        else:
            address = Address(executer=id, **input.coordinates)
            address.save()
        address = Address.objects.filter(executer=id).first()
        return executerSetAddress(coordinates=address)


class QueryAddress(graphene.ObjectType):
    executer_address = graphene.Field(AddressType)

    def resolve_executer_address(self, info, **kwargs):
        token = isAuth(info)
        id_o, role = getIDRole(token)
        if str(role) != "2":
            raise EH.customError("Ошибка", "нет прав доступа")

        return Address.objects.filter(executer=id_o).first()


class MutationAddress(graphene.ObjectType):
    executer_set_address = executerSetAddress.Field(required=True)
