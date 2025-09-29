import graphene

from ...models import AdminStatDoc
from ..enums import TypeExecutersDoc, TypeReportDoc


class InputForStatisticDoc(graphene.InputObjectType):
    class Meta:
        description = "Параметры генерации отчёта для менеджера"

    start_date = graphene.DateTime(required=True, description="Начало периода отчёта")
    end_date = graphene.DateTime(required=True, description="Конец периода отчёта")
    type = TypeReportDoc(required=True, description="Тип отчета")
    profession_id = graphene.List(
        graphene.NonNull(graphene.ID), required=False, description="Идентификатор профессии для отчета ПО ТИПАМ"
    )
    second_start_date = graphene.DateTime(required=False, description="Дополнительная дата ")
    second_end_date = graphene.DateTime(required=False, description="Дополнительная дата ")


class InputForStatisticDocForExecuter(graphene.InputObjectType):
    class Meta:
        description = "Параметры генерации отчёта для исполнителя"

    start_date = graphene.DateTime(required=True, description="Начало периода отчёта")
    end_date = graphene.DateTime(required=True, description="Конец периода отчёта")
    type = TypeExecutersDoc(required=True, description="Тип отчета")


class InputForAdminCreateReport(graphene.InputObjectType):
    class Meta:
        description = "Параметры генерации отчёта для администратора"

    start_date = graphene.DateTime(required=True, description="Начало периода отчёта")
    end_date = graphene.DateTime(required=True, description="Конец периода отчёта")
    start_date_second_period = graphene.DateTime(required=False, description="Начало второго периода отчёта")
    end_date_second_period = graphene.DateTime(required=False, description="Конец второго периода отчёта")
    type = graphene.NonNull(AdminStatDoc.TypeAdminReportEnum, description="Тип отчета")
    hotel_id = graphene.ID(required=False, description="Идентификатор гостиницы")
    executer_id = graphene.ID(required=False, description="Идентификатор Исполнителя")


class inputForListExecuter(graphene.InputObjectType):
    class Meta:
        description = "Параметры генерации списка исполнителей"

    id = graphene.ID(required=True, description="Идентификатор заявки")
