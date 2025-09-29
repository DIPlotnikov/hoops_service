import graphene

from ...models import StatDoc, ExecuterStatDoc, AdminStatDoc, Admin, RoleAdmin
from ...schemas.schema_handler import getIDRoleAdmin, isAuth, getIDRole, is_admin
from ...schemas.stat_doc.type import ReportDocType, ExecuterReportDocType, AdminReportDocType


class QueryStatDocs(graphene.ObjectType):
    '''
    Запросы отчетов для всех ролей
    '''
    manager_get_my_report = graphene.List(graphene.NonNull(ReportDocType), required=True,
                                          description='Получение своих отчётов Менеджером')
    executer_get_my_report = graphene.List(graphene.NonNull(ExecuterReportDocType), required=True,
                                           description='Получение своих отчётов Исполнителем')
    admin_get_reports = graphene.List(graphene.NonNull(AdminReportDocType), required=True,
                                        description='Получение своих отчётов Администратор')

    def resolve_manager_get_my_report(self, info, **kwargs):
        id_o, role, admin = getIDRoleAdmin(isAuth(info))

        if role == 1:
            return StatDoc.objects.filter(owner_id=id_o).exclude(type='LIST_EXECUTERS')
        else:
            raise PermissionError("Ошибка", "нет прав доступа")

    def resolve_executer_get_my_report(self, info, **kwargs):
        id_o, role = getIDRole(isAuth(info))
        if role == 2:
            return ExecuterStatDoc.objects.filter(owner_id=id_o)
        else:
            raise PermissionError("Ошибка", "ну нельзя же сюда!")

    def resolve_admin_get_reports(self, info, **kwargs):
        admin = is_admin(info=info, permission=[RoleAdmin.Roles.REPORT.value, RoleAdmin.Roles.REPORT_MONEY.value], model=True)
        reports = AdminStatDoc.objects.filter(owner=admin)
        if RoleAdmin.Roles.REPORT_MONEY not in admin.roleadmin_set.all().values_list('role', flat=True):
            reports = reports.filter(type__in=['ADMIN_STATISTIC', 'EXECUTER_STANDART', 'STANDART'])

        return reports
