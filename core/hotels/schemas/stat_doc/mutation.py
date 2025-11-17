import uuid
from datetime import timedelta

import graphene

from ..schema_handler import is_manager
from ...models import Admin, AdminStatDoc, ExecuterStatDoc, ExecuterState, Hotel, RoleAdmin, StatDoc, Task
from ...schemas.schema_handler import getIDRole, is_admin, isAuth
from ...schemas.stat_doc.input import (
    InputForAdminCreateReport,
    InputForStatisticDoc,
    InputForStatisticDocForExecuter,
    inputForListExecuter,
)
from ...scripts import excel_handler as ExH
from ...scripts.reports.report_builder_by_pandas import ReportBuilder
from ...scripts.reports.standart_report import create_standart_report
from ...utils.tasks import (
    get_executer_by_period,
    get_normal_period_datetime,
    get_tasks_by_current_manager_by_period,
    get_tasks_by_period,
)


class CreateStat(graphene.Mutation):
    """
    Создание отчёта менеджера
    """

    class Meta:
        description = "Создание отчёта для Менеджера"

    class Arguments:
        input = InputForStatisticDoc(required=True, description="Входные параметры")

    path = graphene.String(required=True, description="Путь к отчету Менеджера")

    @staticmethod
    def mutate(root, info, input):
        manager = is_manager(info=info)
        type_doc = input.type.value if hasattr(input.type, "value") else input.type
        timezone_offset = int(info.context.headers.get("time-zone-offset", -180))

        if type_doc in ["EXECUTORS_LIST", "STANDART_REPORT"]:
            tasks = get_executer_by_period(start_date=input.start_date, end_date=input.end_date, manager=manager)
        else:
            tasks = get_tasks_by_current_manager_by_period(manager, input.start_date, input.end_date)
            if type_doc == "BY_TYPE":
                if input.profession_id is None:
                    input.profession_id = "1"
                tasks = tasks.filter(profession_id__in=input.profession_id)
                assert tasks.count(), "Заявок не найдено"
        doc_stat, created = StatDoc.objects.get_or_create(
            owner=manager, type=type_doc, path=f"statistic/{manager.pk}/{uuid.uuid4()}/{type_doc}.xlsx"
        )

        builder = ExH.ReportBuilder(path=doc_stat.path, type_report=type_doc, time_zone_offset=timezone_offset)
        report_builder = ReportBuilder(type_doc, doc_stat.path, timezone_offset)

        reports = {
            # "STANDART_REPORT": builder.create_manager_standart_report,
            "STANDART_REPORT": builder.create_manager_standart_report,
            "MANAGEMENT_REPORT": builder.create_manager_management_report,
            "BY_TYPE": builder.create_manager_by_type,
            "MANAGERS_REPORT": builder.create_manager_report,
            "DIFFERENCE_REPORT": builder.create_manager_correction,
            "EXECUTORS_LIST": report_builder.process,
        }

        period = "Период {0} - {1}".format(
            (input.start_date + timedelta(minutes=-timezone_offset)).strftime("%d.%m.%y"),
            (input.end_date + timedelta(minutes=-timezone_offset)).strftime("%d.%m.%y"),
        )
        if input.type == "STANDART_REPORT":
            create_standart_report(
                tasks,
                path=builder.path_storage,
                period=period,
                hotel_name=manager.hotel.nameHotel,
            )
        else:
            reports[type_doc](tasks=tasks, period=period)
        return CreateStat(path=doc_stat.path)


class CreateListExecuter(graphene.Mutation):
    """
    Создание списка исполнителей
    """

    class Meta:
        description = "Создание списка исполнителей"

    class Arguments:
        input = inputForListExecuter(required=True, description="Параметры создания списка исполнителей")

    path = graphene.String(required=True, description="Путь к файлу со списком исполнителей")

    @staticmethod
    def mutate(root, info, input):
        manager = is_manager(info=info)

        task = Task.objects.filter(manager.filter_for_query_task("TASK"), id=input.id).first()
        assert task, "Задача не найдена"

        doc_stat = StatDoc.objects.filter(owner=manager, type="LIST_EXECUTERS").first()

        if doc_stat is not None:
            new = False
            path = doc_stat.path
        else:

            new = True
            path = f"LISTS/{manager.pk}/{uuid.uuid4()}/LIST_EXECUTERS.xlsx"
        timezone_offset = int(info.context.headers.get("time-zone-offset", -180))
        builder = ExH.ReportBuilder(path=path, type_report="LIST_EXECUTERS", time_zone_offset=timezone_offset)
        url = builder.create_list_executer_of_task(task=task)

        if new:
            doc_stat = StatDoc(owner=manager, type="LIST_EXECUTERS", path=path)
            doc_stat.save()
        return CreateListExecuter(path=url)


class CreateStatForExecuter(graphene.Mutation):
    """
    Создание отчёта для исполнителя
    """

    class Meta:
        description = "Создание отчёта для исполнителя"

    class Arguments:
        input = InputForStatisticDocForExecuter(required=True, description="Параметры создания отчета для Исполнителя")

    path = graphene.String(required=True, description="Путь к файлу с отчётом для исполнителя")

    @staticmethod
    def mutate(root, info, input):

        id_o, role = getIDRole(isAuth(info))
        assert role == 2, "Нет прав доступа"

        # tasks = Task.objects.filter(
        #     executers__executer__id=id_o, start_at__range=get_normal_period_datetime(input.start_date, input.end_date)
        # ).exclude(status="DELETED")

        executer_states = (
            ExecuterState.objects.select_related("executer")
            .prefetch_related("task_set")
            .filter(
                executer__id=id_o, task__start_at__range=get_normal_period_datetime(input.start_date, input.end_date)
            )
        )

        assert len(executer_states) > 0, "Нет задач в данном промежутке"

        doc_stat, create = ExecuterStatDoc.objects.get_or_create(owner_id=id_o, type=input.type)
        if create:
            doc_stat.path = f"statistic_executer/{id_o}/{uuid.uuid4()}/{input.type}.xlsx"
            doc_stat.save()
        timezone_offset = int(info.context.headers.get("time-zone-offset", -180))
        period = "Период {0} - {1}".format(
            (input.start_date + timedelta(minutes=-timezone_offset)).strftime("%d.%m.%y"),
            (input.end_date + timedelta(minutes=-timezone_offset)).strftime("%d.%m.%y"),
        )

        builder = ExH.ReportBuilder(
            path=doc_stat.path, type_report=f"EXECUTER_{input.type}", time_zone_offset=timezone_offset
        )
        if input.type == "STANDART_REPORT":
            url = builder.create_executer_standart_report(tasks=executer_states, period=period)

        if input.type == "BY_TYPE":
            url = builder.create_executer_by_type(executer_states=executer_states, period=period)

        if input.type == "FINANCIAL":
            url = builder.create_executer_financial(executer_states=executer_states, period=period)

        if input.type == "DIFFERENCE_REPORT":
            url = builder.create_executer_correction(executer_states=executer_states, period=period)

        doc_stat.save()
        return CreateStatForExecuter(path=url)


class AdminCreateReport(graphene.Mutation):
    """
    Создание отчёта для Администратора
    """

    class Meta:
        description = "Создание отчёта для Администратора"

    class Arguments:
        input = InputForAdminCreateReport(required=True, description="Параметры создания отчета для Администратора")

    path = graphene.String(required=True, description="Путь к файлу с отчётом для исполнителя")

    @staticmethod
    def mutate(root, info, input):
        admin = is_admin(info=info, permission=RoleAdmin.Roles.REPORT.value, model=True)
        timezone_offset = int(info.context.headers.get("time-zone-offset", -180))
        period = "Период {0} - {1}".format(
            (input.start_date + timedelta(minutes=-timezone_offset)).strftime("%d.%m.%y"),
            (input.end_date + timedelta(minutes=-timezone_offset)).strftime("%d.%m.%y"),
        )
        stat_admin, created = AdminStatDoc.objects.get_or_create(type=input.type, owner=admin)
        if created:
            stat_admin.path = f"statistic/admin/{admin.id}/{uuid.uuid4()}/{input.type}.xlsx"
            stat_admin.save()
        builder = ExH.ReportBuilder(path=stat_admin.path, type_report=input.type)

        if input.type == AdminStatDoc.TypeAdminReport.STANDART:
            executer_states = get_executer_by_period(input.start_date, input.end_date, hotel_id=input.hotel_id)
            # tasks = get_tasks_by_hotel_id_and_period(input.hotel_id, input.start_date, input.end_date)
            create_standart_report(
                executer_states,
                path=builder.path_storage,
                period=period,
                hotel_name=executer_states[0].task.manager.hotel.nameHotel,
            )
            url = builder.path

            # url = builder.create_manager_standart_report(tasks=tasks, period=period)

        elif input.type == AdminStatDoc.TypeAdminReport.ACTIVITY:
            hotels = Hotel.objects.prefetch_related("manager_set", "manager_set__task_set").filter(
                is_active=True, status=Hotel.Statuses.STEP_3_VERIFIED
            )
            tasks = get_tasks_by_period(input.start_date, input.end_date)
            url = builder.create_admin_activity_report(
                period=period,
                hotels=hotels,
                period_datetime=get_normal_period_datetime(input.start_date, input.end_date),
                tasks=tasks,
            )

        elif input.type == AdminStatDoc.TypeAdminReport.COMPARATIVE:
            raise ValueError("Отчет не доступен")

        elif input.type == AdminStatDoc.TypeAdminReport.PAYMENT_FOR_COORDINATORS:
            tasks = get_tasks_by_period(input.start_date, input.end_date)
            url = builder.create_admin_payment_for_coordinators(tasks=tasks, period=period)
        elif input.type == AdminStatDoc.TypeAdminReport.ADMIN_STATISTIC:
            tasks = get_tasks_by_period(input.start_date, input.end_date)
            tasks2 = get_tasks_by_period(input.start_date_second_period, input.end_date_second_period)
            hotels = (
                Hotel.objects.prefetch_related("personalprofession_set")
                .filter(is_active=True, status=Hotel.Statuses.STEP_3_VERIFIED)
                .order_by("id")
            )
            period2 = "{0} - {1}".format(
                (input.start_date_second_period + timedelta(minutes=-timezone_offset)).strftime("%d.%m.%y"),
                (input.end_date_second_period + timedelta(minutes=-timezone_offset)).strftime("%d.%m.%y"),
            )
            url = builder.create_admin_admin_statistic(
                tasks=tasks, tasks2=tasks2, hotels=hotels, period=period, period2=period2
            )
        elif input.type == AdminStatDoc.TypeAdminReport.EXECUTER_STANDART:
            executer_states = (
                ExecuterState.objects.select_related("executer")
                .prefetch_related("task_set")
                .filter(
                    executer__id=input.executer_id,
                    task__start_at__range=get_normal_period_datetime(input.start_date, input.end_date),
                )
            )
            url = builder.create_executer_standart_report(tasks=executer_states, period=period)
        return AdminCreateReport(path=url)


class MutationStatDocs(graphene.ObjectType):
    """
    Объединение всех мутаций по отчетам
    """

    manager_create_report = CreateStat.Field(required=True)
    manager_create_list_executers_task_by_id = CreateListExecuter.Field(required=True)
    executer_create_report = CreateStatForExecuter.Field(required=True)
    admin_create_report_by_period_and_type = AdminCreateReport.Field(required=True)
