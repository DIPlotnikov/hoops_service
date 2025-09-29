from graphene import ID, Boolean, DateTime, String

from ..input import FiltersInput


class InputPaymentForAdmin(FiltersInput):
    """
    Фильтры для Выплат
    """

    hotel_id = ID(required=False, description="Указатель гостиницы")
    task_id = ID(required=False, description="Указатель задачи")
    date = DateTime(required=False, description="Дата выплаты")
    is_archive = Boolean(required=False, description="Архивная выплата")
