import graphene

from hotels.schemas.enums import EnumCitizenShip
from hotels.schemas.scalars import PassportSeries, SubdivisionCode
from hotels.schemas.schema_fileinfo import fileInfoInput
from passports.choices import CitizenshipOtherG


class InputPassportData(graphene.InputObjectType):
    """Параметры создания паспортных данных"""

    passportFileInfo = graphene.List(graphene.NonNull(fileInfoInput), required=True)
    citizenship = EnumCitizenShip(required=True)
    citizenship_other = CitizenshipOtherG(required=False)
    series = PassportSeries(required=False)
    number = graphene.String(required=True)
    issued_by = graphene.String(required=True)
    date_of_issue = graphene.DateTime(required=True)
    subdivision_code = SubdivisionCode(required=False)
    place_birth = graphene.String(required=False)
