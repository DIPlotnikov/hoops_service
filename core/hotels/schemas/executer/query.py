import graphene
import jwt
from django.conf import settings
from django.db.models import Q
from graphene_django.fields import DjangoConnectionField

from .input import executerInputValidatePhone
from .type import ExecuterPermintsType
from .type import ExecuterType
from ..hotel.types import HotelType
from ..schema_handler import isAuth, getIDRole
from ...models import Executer, PhoneCode
from ...scripts import exception_handler as EH


class QueryExecuter(graphene.ObjectType):
    # возможные эндпоинты
    executer = graphene.Field(
        ExecuterType, required=True, inn=graphene.String(), phone_number=graphene.String(), email=graphene.String()
    )
    executers = graphene.NonNull(ExecuterType, idP=graphene.Int(required=True))
    executer_me = graphene.Field(ExecuterType, required=True)
    executer_permints = graphene.Field(ExecuterPermintsType)
    executer_check_code_by_phone = graphene.Boolean(input=executerInputValidatePhone(required=True), required=True)

    executer_get_favorite_hotels = DjangoConnectionField(HotelType, required=True)

    def resolve_executer(self, info, **kwargs):
        isAuth(info)
        email = kwargs.get("email")
        inn = kwargs.get("inn")

        phone_number = kwargs.get("phone_number")
        filters = [Q(is_active=True)]
        if inn is not None:
            filters.append(Q(inn=inn))
        if phone_number is not None:
            filters.append(Q(phone_number=phone_number))
        if email is not None:
            filters.append(Q(email=email))
        res = Executer.objects.filter(*filters).first()
        assert res, "Пользователь не найден"
        return res

    def resolve_executers(self, info, **kwargs):
        token = isAuth(info)
        id = kwargs.get("idP")
        if id is not None:
            return Executer.objects.filter(professions__id=id)
            # q = Event.objects.filter(tag__text__in = ['abc', 'def']).distinct() это обычный экзист

    def resolve_executer_me(self, info):
        # TODO: убрать в один метод
        token = isAuth(info)
        token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        if token.get("role") != 2:
            raise EH.customError("Ошибка", "пользователь не авторизован")
        return Executer.objects.filter(id=token.get("id"), is_active=True).first()

    def resolve_executer_permints(self, info, **kwargs):
        token = isAuth(info)
        id_o, role = getIDRole(token)
        if str(role) != "2":
            raise EH.customError("Ошибка", "нет доступа")
        res = ExecuterPermintsType()

        res.medical_book_expiration = Executer.objects.get(id=id_o).medical_book_expiration
        res.work_expiration = Executer.objects.get(id=id_o).work_expiration

        return res

    def resolve_executer_check_code_by_phone(self, info, input):
        phone_code = PhoneCode.objects.filter(**input).first()
        if phone_code is None:
            raise PermissionError("Код подтверждения неверный")
        phone_code.is_valid_number = True
        phone_code.save()
        return True

    def resolve_executer_get_favorite_hotels(self, info, **kwargs):
        id, role = getIDRole(isAuth(info))
        if str(role) != "2":
            raise PermissionError("Нельзя!")

        return Executer.objects.get(pk=id).favourites_hotel
