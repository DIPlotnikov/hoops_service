import graphene
from graphene_django.types import ObjectType

from .schema_handler import isValidate


class MetaInformationType(ObjectType):
    """
    Мета информация из токена
    """

    permissions = graphene.String(required=False, description="Права пользователя")


class ValidateTokenType(ObjectType):
    """
    Информация из токена доступа
    """

    def __init__(self, type, **kwargs):
        self.type = type
        self.meta = kwargs.get("meta")
        self.role = kwargs.get("role")

    type = graphene.String(required=True, description="Тип пользователя")
    meta = graphene.Field(MetaInformationType, description="Мета информация")
    role = graphene.Int(deprecation_reason="Переходим к полю type", description="Числовой тип пользователя")
    ok = graphene.Boolean(
        default_value=True, deprecation_reason="Если объект пришел - всё гуд", description="Флаг успеха"
    )


class InputForValidateToken(graphene.InputObjectType):
    """
    Входные параметры валидации токена
    """

    token = graphene.String(required=True, description="Токен доступа")
    fcm_token = graphene.String(required=False, description="FCM токен для push уведомлений")


class QueryValidateToken(graphene.ObjectType):
    """
    Квери валидации
    """

    validate_token = graphene.NonNull(
        ValidateTokenType,
        input=InputForValidateToken(
            required=True, description="Запрос информации из токена и проверка его валидности"
        ),
    )

    def resolve_validate_token(self, info, input):
        """
        Валидация токена
        :param info:
        :param input: токены
        :return: ValidateTokenType с данными в случае успешной проверки
        """
        res = isValidate(**input, info=info)
        return ValidateTokenType(**res)
