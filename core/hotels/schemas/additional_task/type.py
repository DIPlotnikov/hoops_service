from graphene_django import DjangoObjectType

from ...models import AdditionalTask


class AdditionalTaskType(DjangoObjectType):
    """
    Тип дополнительной информации по Заявке
    """

    class Meta:
        model = AdditionalTask
        exclude = ("task",)
