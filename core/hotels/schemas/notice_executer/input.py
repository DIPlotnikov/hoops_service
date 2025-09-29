import graphene
from ..schema_fileinfo import fileInfoInput


class InputForCreateExecuterNotice(graphene.InputObjectType):
    class Meta:
        description = 'Параметры создания уведомления для Исполнителя'

    id_executer = graphene.ID(required=True, description='ID Исполнителя')
    files = graphene.List(graphene.NonNull(fileInfoInput), required=True,
                          description='Список FileInfoType c файлами уведомления')


class InputForQueryNotices(graphene.InputObjectType):
    class Meta:
        description = 'Параметры запроса таблицы уведомлений для Исполнителей по ID Исполнителя'

    id_executer = graphene.ID(required=False, description='Фильтр по ID Исполнителя')


class InputForQueryExecuterNotices(graphene.InputObjectType):
    class Meta:
        description = 'Параметры запроса таблицы уведомлений для Исполнителей'

    executer_fullname = graphene.String(required=False, description="Фильтр по имени исполнителя")

