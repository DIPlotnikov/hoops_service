from graphene import DateTime, InputObjectType, String


class InputForAdditionalTask(InputObjectType):
    """
    Параметры на добавление дополнительной информации к заявке
    """

    datetime = DateTime(required=False, desciption="Дата и время")
    description = String(required=False, description="Описание задачи")
