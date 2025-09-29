import graphene
from graphene_django import DjangoObjectType

from ...models import AdminStatDoc, ExecuterStatDoc, StatDoc
from ..enums import TypeExecutersDoc, TypeReportDoc


class ReportDocType(DjangoObjectType):
    """
    Класс типа Отчёт для менеджера
    """

    class Meta:
        model = StatDoc
        exclude = ("owner",)
        description = "Отчёт менеджера"

    path = graphene.String(required=True, description="Путь к файлу")
    type = TypeReportDoc(required=True, description="Тип отчёта")


class ExecuterReportDocType(DjangoObjectType):
    """
    Класс типа Отчёт для Исполнителя
    """

    class Meta:
        model = ExecuterStatDoc
        exclude = ("owner",)
        description = "Отчёт исполнителя"

    path = graphene.String(required=True, description="Путь к файлу")
    type = TypeExecutersDoc(required=True, description="Тип отчёта")


class AdminReportDocType(DjangoObjectType):
    """
    Класс типа Отчёт для Администратора
    """

    class Meta:
        model = AdminStatDoc
        exclude = ("owner",)
        description = "Отчёт Администратора"

    path = graphene.String(required=True, description="Путь к файлу")
    type = graphene.NonNull(AdminStatDoc.TypeAdminReportEnum, description="Тип отчёта")
