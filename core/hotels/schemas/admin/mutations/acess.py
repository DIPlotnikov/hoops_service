import graphene

from ....models import Admin, Executer, Manager, RoleAdmin
from ...schema_handler import is_admin
from ..input import inputForAcess


class TokenExecuter(graphene.Mutation):
    """
    Получение токена Администратором на вход в профиль
    """

    class Arguments:
        input = inputForAcess(required=True, description="Параметры запроса токена для доступа в профиль")

    token = graphene.String(required=True, description="Временный токен доступа")

    @staticmethod
    def mutate(root, info, input):
        # проверка на Администратора и его прав
        admin = is_admin(
            info=info,
            permission=[RoleAdmin.Roles.CUSTOMER_AUTH.value, RoleAdmin.Roles.EXECUTER_AUTH.value],
            model=True,
        )
        # получение объекта пользователя для манипуляций

        user_obj = Manager if input.role == "manager" else Executer
        # возвращаем токен доступа для администратора
        return TokenExecuter(
            token=user_obj.objects.get(id=input.id).token_for_admin(
                read=admin.get_permission_for_only_read_in_other_profiles(input.role)
            )
        )


class MutationAdminAccess(graphene.ObjectType):
    admin_get_access_by_role_and_id = TokenExecuter.Field(
        required=True, description="Получение токена" " Администратором на вход в профиль"
    )
