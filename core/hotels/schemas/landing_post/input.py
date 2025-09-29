import graphene
from ..schema_fileinfo import fileInfoInput


class InputForUpsertPostLanding(graphene.InputObjectType):
    """
    Создание и обновление поста для лендинга
    """
    id = graphene.ID(required=False, description='ID поста')
    title = graphene.String(required=True, description='Заголовок')
    content = graphene.String(required=True, description='Контент')
    hashtag = graphene.String(required=True, description='Хештег')
    url = graphene.String(required=True, description='URL')
    files = graphene.List(graphene.NonNull(fileInfoInput), required=True, description='Файлы')


class InputForQueryPostLandingWithFilters(graphene.InputObjectType):
    """
    Фильтры для отображения постов на лендинге
    """
    title = graphene.String(required=False, description='Заголовок')
    is_public = graphene.Boolean(required=False, description='Флаг публичности')
    date = graphene.DateTime(required=False, description='Дата создания')
