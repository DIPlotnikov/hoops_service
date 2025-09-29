import graphene
from django.db.models import Q


class FiltersInput(graphene.InputObjectType):
    class Meta:
        description = "Входной параметр фильтров"

    @property
    def q_filters(self):
        return [
            Q(attr, self.__getattribute__(attr))
            for attr in self.__dict__
            if not callable(getattr(self, attr)) and not attr.startswith("_")
        ]


class InputCode(graphene.InputObjectType):
    class Meta:
        description = "Входной параметр секретного кода"

    code = graphene.String(required=True)


class InputID(graphene.InputObjectType):
    class Meta:
        description = "Входной параметр ID"

    id = graphene.ID(required=True)


class InputURL(graphene.InputObjectType):
    class Meta:
        description = "Входной параметр URL"

    url = graphene.String(required=True)


class InputIDs(graphene.InputObjectType):
    class Meta:
        description = "Входной параметр список ID"

    ids = graphene.List(graphene.NonNull(graphene.ID), required=True)


class InputDate(graphene.InputObjectType):
    class Meta:
        description = "Входной параметр формат ISO Date"

    date = graphene.Date(required=True)


class InputDateTime(graphene.InputObjectType):
    class InputDate(graphene.InputObjectType):
        class Meta:
            description = "Входной параметр формат ISO DateTime"

    datetime = graphene.DateTime(required=True)


class InputPassword(graphene.InputObjectType):
    """
    Параметры смены пароля
    """

    id = graphene.ID(required=True, description="Идентификатор субъекта")
    new_password = graphene.String(required=True, description="Новый пароль субъекта")


class InputFullName(graphene.InputObjectType):
    """
    Инпут для изменения полного имени
    """

    surname = graphene.String(required=True, description="Фамилия")
    first_name = graphene.String(required=True, description="Имя")
    middle_name = graphene.String(required=True, description="Отчество")


class InputIdTaskIdExecuter(graphene.InputObjectType):
    """
    Инпут для устновки отклика
    """

    id_task = graphene.ID(required=True, description="Идентификатор задачи")
    id_executer = graphene.ID(required=True, description="Идентификатор Исполнителя")


class InputIdDatetime(InputID, InputDateTime):
    """
    Инпут для устновки даты и времени по айди
    """

    pass
