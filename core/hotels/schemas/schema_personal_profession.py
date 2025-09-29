import graphene
from graphene import ObjectType
from graphene_django.types import DjangoObjectType

from .input import InputID
from .schema_handler import is_manager
from ..models import PersonalProfession, Profession
from ..scripts import exception_handler as EH


class PersonalProfessionType(DjangoObjectType):
    class Meta:
        model = PersonalProfession
        exclude = ("task_set", "owner")

    for_executer = graphene.Float(required=True)

    def resolve_for_executer(self, info):
        res = self.rent * (self.analog.multiplier / 100)
        return round(res, 2)


class PersonalProfessionsBlockType(ObjectType):
    personal_profession = graphene.List(graphene.NonNull(PersonalProfessionType), required=True)
    max_count_of_personal_professions = graphene.Int(required=True)


class personalProfessionInput(graphene.InputObjectType):
    profession = graphene.ID(required=True, description="Указатель базовой профессии")
    rent = graphene.Float(required=True, description="Ставка эксклюзивной професии")
    name = graphene.String(required=True, description="Наименование эксклюзивной професии")
    is_rent_for_executer = graphene.Boolean(
        required=True, description="Флаг-указатель чья ставка указана при создании"
    )


class QueryPersonalProfession(graphene.ObjectType):

    manager_get_personal_professions = graphene.Field(PersonalProfessionsBlockType, required=True)

    def resolve_manager_get_personal_professions(self, info):
        manager = is_manager(info=info)
        res = PersonalProfessionsBlockType()
        res.personal_profession = manager.hotel.personalprofession_set.filter(active=True)
        res.max_count_of_personal_professions = manager.hotel.max_count_of_personal_profession

        return res


class createPersonalProfession(graphene.Mutation):
    class Arguments:
        input = personalProfessionInput(required=True)

    personal_profession = graphene.Field(graphene.NonNull(PersonalProfessionType))

    @staticmethod
    def mutate(root, info, input):
        manager = is_manager(info=info, permission=["SETTINGS_EDIT"])
        input["owner"] = manager.hotel
        try:
            input["analog"] = Profession.objects.get(id=input["profession"])
            input.pop("profession")
        except Exception:
            raise EH.customError("Ошибка", "не правильно указан аналог профессии")

        if (
            len(PersonalProfession.objects.filter(owner=input["owner"], active=True))
            == input["owner"].max_count_of_personal_profession
        ):
            raise EH.customError(
                "Ошибка", "превышено количество эксклюзивных профессий, " "для создания новых - удалите старые"
            )
        if input["is_rent_for_executer"]:
            input["rent"] = round(input["rent"] / input["analog"].multiplier * 100, 2)

        input.pop("is_rent_for_executer")
        personal_profession = PersonalProfession(**input)
        personal_profession.save()

        return createPersonalProfession(personal_profession=personal_profession)


class deletePersonalProfession(graphene.Mutation):
    class Arguments:
        input = InputID(required=True)

    ok = graphene.Boolean(required=True)

    @staticmethod
    def mutate(root, info, input):

        manager = is_manager(info=info, permission=["SETTINGS_EDIT"])
        personal_profession = PersonalProfession.objects.filter(id=input.id, owner__manager=manager).first()
        if personal_profession is None:
            raise EH.customError("Ошибка", "нет прав удаления профессии или профессия уже удалена")
        else:
            personal_profession.active = False
            personal_profession.save()

        return deletePersonalProfession(ok=True)


class MutationPersonalProfession(graphene.ObjectType):
    manager_personal_profession_create = createPersonalProfession.Field(required=True)
    manager_personal_profession_delete = deletePersonalProfession.Field(required=True)
