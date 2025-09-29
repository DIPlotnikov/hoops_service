import graphene

from hotels.schemas.scalars import Phonenumber


class PhonenumberInput(graphene.InputObjectType):
    """
    Инпут для номера телефона
    """

    number = Phonenumber(required=True, description="Номер телефона")


class FilterExecutorInput(graphene.InputObjectType):
    """
    Инпут для фильтрации исполнителей
    """

    name = graphene.String(required=False, description="Имя исполнителя")
    id = graphene.ID(required=False, description="ID исполнителя")
