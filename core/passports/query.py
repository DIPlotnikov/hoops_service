import graphene

from hotels.schemas.schema_handler import isAuth, getIDRole
from passports.models import PassportData
from passports.type import PassportDataType


class QueryPassportData(graphene.ObjectType):
    executer_passport = graphene.Field(PassportDataType, required=False)

    def resolve_executer_passport(self, info, **kwargs):
        token = isAuth(info)
        id_o, role = getIDRole(token)
        if str(role) != "2":
            raise ValueError("данные доступны только исполнителям")
        return PassportData.objects.filter(executer=id_o).first()
