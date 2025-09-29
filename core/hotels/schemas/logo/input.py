import graphene
from ..schema_fileinfo import fileInfoInput


class InputForUpsertLogo(graphene.InputObjectType):
    """
    Параметры для создания или обновления логотипа
    """
    id = graphene.ID(required=False, description='Идентификатор логотипа')
    description = graphene.String(required=True, description='Описание логотипа')
    files = graphene.List(graphene.NonNull(fileInfoInput, description='Файл'), required=True)
    is_visible = graphene.Boolean(required=True, description='Видимость')
