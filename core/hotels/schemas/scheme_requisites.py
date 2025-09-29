import graphene
from graphene_django.types import DjangoObjectType

from .scalars import BIK, INN, KPP, CardNumber, CorrectBill, PaymentBill, validate_inn
from .schema_handler import getIDRole, getIDRoleAdmin, isAuth
from ..models import Executer, Manager, Requisites, SimpleRequisite
from ..scripts import exception_handler as EH


# Create a GraphQL type for the Requisites model
class RequisitesType(DjangoObjectType):
    class Meta:
        description = "Реквизиты Гостиницы"
        model = Requisites
        exclude = ("executer", "owner")


class SimpleRequisiteType(DjangoObjectType):

    class Meta:
        model = SimpleRequisite
        exclude = ("executer", "bank_name")


class QueryRequisites(graphene.ObjectType):
    executer_requisites = graphene.Field(RequisitesType)
    executer_get_simple_requisite = graphene.Field(SimpleRequisiteType)

    def resolve_executer_requisites(self, info, **kwargs):
        token = isAuth(info)
        id_o, role = getIDRole(token)
        if str(role) != "2":
            raise EH.customError("Ошибка", "нет прав доступа")

        return Requisites.objects.filter(executer_id=id_o).first()

    def resolve_executer_get_simple_requisite(self, info, **kwargs):
        token = isAuth(info)
        id_o, role = getIDRole(token)

        if str(role) != "2":
            raise EH.customError("Ошибка", "нет прав доступа")

        return SimpleRequisite.objects.filter(executer_id=id_o).first()


class requisitesInput(graphene.InputObjectType):
    """
    Игпут для создания/обновления реквизитов Гостиницы
    """

    innBank = INN(required=True, description="ИНН")
    paymentBill = PaymentBill(required=True, description="Расчетный счет")
    correctBill = CorrectBill(required=True, description="Корр счет")
    kpp = KPP(required=False, description="КПП")
    bik = BIK(required=True, description="БИК")
    name = graphene.String(required=True, description="Имя банка")
    legal_address = graphene.String(required=True, description="Юридический адрес")
    signer = graphene.String(required=True, description="Имя подписанта")


class SimpleRequisiteInput(graphene.InputObjectType):
    inn = INN(required=True)
    card_number = CardNumber(required=True)


class ExecuterUpsertSimpleRequisite(graphene.Mutation):
    class Arguments:
        input = graphene.NonNull(SimpleRequisiteInput)

    requisite = graphene.Field(SimpleRequisiteType, required=True)

    @staticmethod
    def mutate(root, info, input):
        assert validate_inn(input.inn), "Не верный ИНН"
        token = isAuth(info)
        id_o, role = getIDRole(token)
        if str(role) != "2":
            raise EH.customError("Ошибка", "редактирование реквизитов доступно только исполнителям")
        executer = Executer.objects.get(id=id_o)
        req = SimpleRequisite.objects.filter(executer=executer)
        if len(req) > 0:
            if req[0].inn != input.inn:
                executer.break_status()
            req.update(**input)
            return ExecuterUpsertSimpleRequisite(requisite=req[0])
        req = SimpleRequisite(executer=executer, **input)
        req.save()

        return ExecuterUpsertSimpleRequisite(requisite=req)


class ManagerUpsertRequisites(graphene.Mutation):
    class Arguments:
        input = graphene.NonNull(requisitesInput)

    requisites = graphene.Field(RequisitesType, required=True)

    @staticmethod
    def mutate(root, info, input):
        # Проверка менеджера на ИНН Менеджера
        id_o, role, admin = getIDRoleAdmin(isAuth(info))
        # если он не он
        if str(role) != "1" or admin is False:
            # делаем ошибку
            raise EH.customError("Ошибка", "редактирование реквизитов доступно только менеджеру")
        # получаем гостиницу Менеджера
        hotel = Manager.objects.select_related("hotel").filter(id=id_o).first().hotel
        # апдейтим ли создаем реквизиты
        req, created = Requisites.objects.update_or_create(owner=hotel, defaults={**input})
        # скидываем статус гостинице
        hotel.go_to_start()
        # возвращаем созданные реквизиты
        return ManagerUpsertRequisites(requisites=req)


class Mutationrequisites(graphene.ObjectType):
    executer_upsert_simple_requisite = ExecuterUpsertSimpleRequisite.Field(required=True)
    manager_upsert_requisites = ManagerUpsertRequisites.Field(required=True)
