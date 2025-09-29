import graphene

from ...models import Profession


class InputForGetCost(graphene.InputObjectType):
    class Meta:
        description = "Параметры запроса стоимости часа по профессии"

    id_profession = graphene.ID(required=True, description="ID профессии")
    cost = graphene.Float(required=True, description="Стоимость")
    calculate_cost_for_executer = graphene.Boolean(
        required=True,
        description="True - надо рассчитать сколько получит Исполнитель,"
        "если гостиница заплатит cost, False - наоборот",
    )


class InputForUpsertProfession(graphene.InputObjectType):
    class Meta:
        description = "Параметры создания/обновления профессии"

    id = graphene.ID(required=False, description="ID профессии")
    name = graphene.String(required=True, description="Наименование профессии")
    description = graphene.String(required=True, description="Описание услуги")
    rate_max = graphene.Int(required=True, description="Максимальная ставка")
    rate_min = graphene.Int(required=True, description="Минимальная ставка")
    rate_step = graphene.Int(required=True, description="Шаг ставки")
    percent = graphene.Int(required=True, description="Процент")
    numerate = Profession.NumeratesEnum(required=True, description="Период выплат Исполнителям")
