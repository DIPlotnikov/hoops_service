import graphene
from .input import InputForCreateExecuterNotice
from .type import ExecuterNoticeType
from ..input import InputIDs
from ..schema_handler import is_admin
from ...models import FileInfo, ExecuterNotice, Admin, RoleAdmin


class CreateExecuterNotice(graphene.Mutation):
    class Meta:
        description = 'Создание уведомелния для Исполнителя'
    class Arguments:
        input = InputForCreateExecuterNotice(required=True)

    executer_notice = graphene.Field(graphene.NonNull(ExecuterNoticeType), description='Уведомление Исполнителя')

    @staticmethod
    def mutate(root, info, input):
        id_admin = is_admin(info=info, permission=RoleAdmin.Roles.DOCUMENT.value)

        executer_notice = ExecuterNotice(admin_id=id_admin, executer_id=input.id_executer)
        executer_notice.save()
        for file in input.files:
            fileInfo = FileInfo(**file)
            fileInfo.save()
            executer_notice.files.add(fileInfo)

        return CreateExecuterNotice(executer_notice=executer_notice)


class DeleteExecuterNotice(graphene.Mutation):
    class Meta:
        description = 'Удаление уведомелния для Исполнителя и его файлы'
        output = graphene.Boolean

    class Arguments:
        input = InputIDs(required=True)

    ok = graphene.Boolean(required=True, description='Флаг успешного действия')

    @staticmethod
    def mutate(root, info, input):
        is_admin(info=info, permission=RoleAdmin.Roles.DOCUMENT.value)

        executer_notice = ExecuterNotice.objects.prefetch_related("files").filter(id__in=input.ids)
        for notice in executer_notice:
            for file in notice.files.all():
                file.delete()
        executer_notice.delete()
        return True


class MutationExecuterNotice(graphene.ObjectType):
    admin_create_executer_notice_by_id_executer = \
        CreateExecuterNotice.Field(required=True, description='Создание уведомления для Исполнителя администратором')
    admin_delete_executer_notice_by_id = \
        DeleteExecuterNotice.Field(required=True,
                                   description='Удаление уведомления для Исполнителя по его ID администратором')
