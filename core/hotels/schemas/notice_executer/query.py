from django.db.models import Q

from .input import InputForQueryExecuterNotices
from .type import ExecuterNotice, ExecuterNoticeType
from ..input import InputID
from ..schema_handler import getIDRole, isAuth, is_admin
import graphene
from graphene_django.fields import DjangoConnectionField

from ...models import Admin, RoleAdmin


class QueryExecuterNotice(graphene.ObjectType):
    admin_get_executer_notices = DjangoConnectionField(ExecuterNoticeType, input=InputForQueryExecuterNotices(required=True), required=True, description='Получение списка уведомлений для Исполнителя администратором')
    admin_get_executer_notice_by_id = graphene.NonNull(ExecuterNoticeType, input=InputID(required=True), description='Получение уведомления для Исполнителя администраторов по ID')

    executer_get_executer_notices = graphene.List(graphene.NonNull(ExecuterNoticeType), required=True, description='Получение списка уведомлений для Исполнителя')

    def resolve_admin_get_executer_notices(self, info, input, **kwargs):
        is_admin(info=info, permission=RoleAdmin.Roles.DOCUMENT.value)
        notices = ExecuterNotice.objects.select_related('admin', 'executer').prefetch_related('files').all()

        if input.executer_fullname:
            notices = notices.filter(Q(executer__first_name__icontains=input.executer_fullname) | Q(executer__second_name__icontains=input.executer_fullname) | Q(executer__middle_name__icontains=input.executer_fullname))
        return notices

    def resolve_admin_get_executer_notice_by_id(self, info, input):
        is_admin(info=info, permission=RoleAdmin.Roles.DOCUMENT.value)
        return ExecuterNotice.objects.select_related('admin', 'executer').prefetch_related('files').get(**input)


    def resolve_executer_get_executer_notices(self, info):
        id_o, role = getIDRole(isAuth(info))
        assert str(role) in ['2'], "Нет прав доступа"
        return ExecuterNotice.objects.select_related('admin','executer').prefetch_related('files').filter(executer_id=id_o)