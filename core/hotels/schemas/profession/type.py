import graphene
from graphene_django import DjangoObjectType

from ...models import Profession


class ProfessionType(DjangoObjectType):
    class Meta:
        model = Profession
        exclude = ("executer_set", "personalprofession_set", "task_set")

    multiplier = graphene.Int(
        required=True,
        description="Процент HOOOPS",
        deprecation_reason="Перешли на процент",
    )

    def resolve_percent_for_hoops(self, info):
        return 100 - self.percent
