from datetime import timedelta

import graphene
from django.db.models import Q
from django.db.models import Value as V
from django.db.models.functions import Concat
from django.utils import timezone
from graphene_django.fields import DjangoConnectionField

from executor.models import Metrics
from passports.models import PassportData
from ..input import InputForGetExecuterByName, InputForQueryAllExecuter
from ..type import PaymentJumpFinanceType, executerForAdmin
from ...input import InputID
from ...schema_handler import is_admin
from ...task.type import TaskForAdminType
from ....models import Executer, PaymentJumpFinance, RoleAdmin, Task
from ....scripts.FNS import check_inn_selfwork


class AdminExecuterQuery(graphene.ObjectType):
    """
    Квери Администратора на сущность Исполнитель
    """

    admin_all_executers = DjangoConnectionField(
        executerForAdmin,
        input=InputForQueryAllExecuter(required=False),
        description="Получение списка всех Исполнителей Администратором",
        required=True,
    )
    admin_get_executer_by_name = graphene.List(
        graphene.NonNull(executerForAdmin),
        input=InputForGetExecuterByName(required=True),
        description="Получение списка Исполнителей по имени Администратором",
        required=True,
        deprecation_reason="filter by whatever",
    )
    admin_get_executer_by_id = graphene.NonNull(
        executerForAdmin,
        input=InputID(required=True),
        description="Получение списка Исполнителей по ID Администратором",
    )

    admin_get_payments_of_executer_by_id = DjangoConnectionField(
        PaymentJumpFinanceType,
        input=InputID(required=True),
        description="Получение списка Выплат Исполнителя по ID Администратором",
        required=True,
    )

    admin_check_executer_in_fns = graphene.String(
        input=InputID(required=True, description="Параметры проверки в ФНС"),
        required=True,
        description="Проверка Исполнителя в ФНС Администратором",
    )
    admin_get_current_task_id_executer = graphene.Field(
        TaskForAdminType, input=InputID(required=True), description="Текущая заявка Исполнителя Администратором"
    )

    def resolve_admin_all_executers(self, info, input, **kwargs):
        # проверяем что Администратор
        is_admin(info=info, permission=RoleAdmin.Roles.EXECUTER.value)
        # получаем всех активных Исполнителей
        res = Executer.objects.select_related("simplerequisite").prefetch_related("professions").filter(is_active=True)
        # фильтруем по входным параметрам
        if input.is_test is not None:
            res = res.filter(is_test=input.is_test)
        if input.status:
            res = res.filter(status=input.status)
        if input.email:
            res = res.filter(email__icontains=input.email)
        if input.inn:
            res = res.filter(simplerequisite__inn__icontains=input.inn)
        if input.phone:
            res = res.filter(phone_number__icontains=input.phone)
        if input.id:
            res = res.filter(id=input.id)
        if input.id_profession:
            res = res.filter(professions__id=input.id_profession)
        if input.list_of_id_profession:
            res = res.filter(professions__id__in=input.list_of_id_profession)
        if input.full_name:
            res = res.annotate(
                full_name_search=Concat("middle_name", V(" "), "first_name", V(" "), "second_name")
            ).filter(full_name_search__icontains=input.full_name)
        if input.count_day_for_last_task is not None:
            # TODO перевести на метрику
            # raise ValueError("Поиск по последней задаче временно не доступен")
            current_date = timezone.now() - timedelta(days=input.count_day_for_last_task)

            executors_id = Metrics.objects.filter(last_request_task__lte=current_date).values_list(
                "executor__id", flat=True
            )
            res = res.filter(id__in=executors_id)

            # res = [
            #     x
            #     for x in res
            #     if x.count_day_for_last_task and x.count_day_for_last_task >= input.count_day_for_last_task
            # ]
        if input.count_day_for_end_registration:
            res = res.filter(
                work_expiration__lte=timezone.now() + timedelta(days=input.count_day_for_end_registration)
            )
        if input.count_day_for_end_medical_book:
            res = res.filter(
                medical_book_expiration__lte=timezone.now() + timedelta(days=input.count_day_for_end_medical_book)
            )
        if input.agreement_datetime:
            res = res.filter(agreement_datetime=input.agreement_datetime)
        if input.citizenship:
            pp = PassportData.objects.filter(citizenship=input.citizenship).values_list("executer", flat=True)
            res = res.filter(id__in=pp)
        return res

    def resolve_admin_get_executer_by_name(self, info, input):
        is_admin(info=info, permission=RoleAdmin.Roles.EXECUTER.value)
        res = Executer.objects.filter(
            Q(first_name__icontains=input.name)
            | Q(second_name__icontains=input.name)
            | Q(middle_name__icontains=input.name)
        )
        if input.name.isdigit():
            res = Executer.objects.filter(Q(id=int(input.name)))
        filters = [
            Q(is_active=True),
        ]
        if input.is_test is not None:
            filters.append(Q(is_test=input.is_test))
        if input.status:
            filters.append(Q(status=input.status))
        return res.filter(*filters)[:10]

    def resolve_admin_get_executer_by_id(self, info, input):
        # проверяем на Админситратора
        is_admin(info=info, permission=RoleAdmin.Roles.EXECUTER.value)
        # возвращаем Исполнителя по параметрам
        return (
            Executer.objects.select_related("requisites", "profile_pic", "simplerequisite", "executorjumpfinance")
            .prefetch_related("professions")
            .get(**input)
        )

    def resolve_admin_get_payments_of_executer_by_id(self, info, input, **kwargs):
        # проверяем на Админситратора
        is_admin(info=info, permission=RoleAdmin.Roles.EXECUTER.value)
        # возвращаем Выплаты JumpFianance
        return PaymentJumpFinance.objects.filter(contractor__executer__id=input.id)

    def resolve_admin_check_executer_in_fns(self, info, input):
        # проверка на Администратора
        is_admin(info=info, permission=RoleAdmin.Roles.EXECUTER.value)
        # получение Исполнителя для проверки
        executor = Executer.objects.prefetch_related("simplerequisite").get(id=input.id)
        # если у Исполнителя нет его реквизитов
        assert hasattr(executor, "simplerequisite") is True, "У исполнителя ошибки в реквизитах = отсутсвуют"
        # проводим проверку в ФНС и отправляем результат
        return check_inn_selfwork(str(executor.inn))

    def resolve_admin_get_current_task_id_executer(self, info, input):
        # проверка на Администратора
        is_admin(info=info, permission=RoleAdmin.Roles.EXECUTER.value)
        # получаем заявку, где в исполнителях есть Исполнитель и дата Сегодня исключая заявки со стопом и не начавшиеся
        task = (
            Task.objects.filter(
                executers__executer__id=input.id, is_approved=True, start_at__date=timezone.now().date()
            )
            .exclude(status="DELETED", executers__status__in=[None, "STOP"])
            .first()
        )
        # если заявка есть
        if task is not None:
            # проверяем что она не закончилась
            if (task.start_at + timedelta(hours=task.duration)) < timezone.now():
                return None

        return task
