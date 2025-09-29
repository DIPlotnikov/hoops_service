import graphene

from .input import InputForGetCost
from .type import ProfessionType
from ..schema_handler import isAuth
from ...models import Profession


class QueryProfession(graphene.ObjectType):
    profession = graphene.Field(
        ProfessionType, id=graphene.Int(required=True), description="Получение профессии по ID", required=True
    )
    professions = graphene.List(
        graphene.NonNull(ProfessionType), description="Получение всех профессий", required=True
    )
    profession_get_cost = graphene.Float(
        required=True, description="Получение расчета стоимости для Исполнителя", input=InputForGetCost(required=True)
    )

    def resolve_profession(self, info, id):
        """
        Получение профессии по ID
        """
        # isAuth(info)
        # возвращаем запрошенную профессию
        return Profession.objects.get(id=id)

    def resolve_professions(self, info):
        """
        Получение всех профессий
        """
        # isAuth(info)
        # возвращаем все профессии
        return Profession.objects.all().order_by("name")

    def resolve_profession_get_cost(self, info, input):
        """
        Получение расчета стоимости для Исполнителя
        """
        isAuth(info)
        # получаем нужную профессию
        id_profession = input.pop("id_profession")
        profession = Profession.objects.get(id=id_profession)
        # расчет стоимости и возвращаем
        return profession.calculate_rate(**input)
