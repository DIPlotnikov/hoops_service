from datetime import datetime

import graphene
from graphene_django import DjangoObjectType

from hotels.schemas.enums import EnumCitizenShip
from hotels.schemas.schema_fileinfo import FileInfoType
from passports.choices import CitizenshipOtherG
from passports.models import PassportData


class PassportDataType(DjangoObjectType):
    class Meta:
        model = PassportData
        exclude = (
            "executer",
            "firstPage",
            "secondPage",
        )

    passportData = graphene.List(graphene.NonNull(FileInfoType), required=True)
    citizenship = EnumCitizenShip(required=True)
    citizenship_other = CitizenshipOtherG(required=False)
    date_of_issue = graphene.DateTime(required=True)
    series = graphene.String(required=False)

    def resolve_date_of_issue(self, info):
        return datetime.combine(self.date_of_issue, datetime.min.time())

    def resolve_passportData(self, info):
        res = []
        if self.firstPage is not None:
            res.append(self.firstPage)
        if self.secondPage is not None:
            res.append(self.secondPage)
        return res

    def resolve_series(self, info):
        series = str(self.series)
        return series.zfill(4)

    def resolve_citizenship_other(self, info):
        return self.citizenship_other
