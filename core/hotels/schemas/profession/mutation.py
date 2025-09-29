import graphene
from .input import InputForUpsertProfession
from .type import ProfessionType
from ..schema_handler import is_admin
from ...models import Profession, Executer, RoleAdmin


class UpsertProfession(graphene.Mutation):
    """
    Обновление/создание профессии Администратором
    """

    class Meta:
        description = 'Обновление/создание профессии Администратором'

    class Arguments:
        input = InputForUpsertProfession(required=True, description='Параметры создания/обновления профессии')

    profession = graphene.NonNull(ProfessionType, description='Профессия')

    @staticmethod
    def mutate(root, info, input: graphene.InputObjectType):
        # проверяем на администратора
        is_admin(info=info, permission=RoleAdmin.Roles.SETTINGS.value)
        # получаем ID профессии
        id_profession = input.pop('id', None)
        # обновляем или создаем профессию
        profession, created = Profession.objects.update_or_create(id=id_profession, defaults={**input})
        # если создана - то надо добавить ее техническому пользователю
        if created:
            profession.executer_set.add(Executer.get_technical_account())
            profession.save()
        return UpsertProfession(profession=profession)


class MutationProfession(graphene.ObjectType):
    """
    Мутации профессий
    """

    class Meta:
        description = 'Мутации профессий'

    admin_profession_upsert = UpsertProfession.Field(required=True,
                                                     description='Создание/обновление профессии Администратором')
