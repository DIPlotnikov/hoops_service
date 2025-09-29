import datetime
from datetime import timedelta
from uuid import uuid4

import graphene
from django.utils import timezone
from executor.models import Metrics
from passports.models import PassportData

from ..input import (
    inputForDenyExecuterPayment,
    InputId,
    InputIdPassword,
    InputForMarkObjectsAsTest,
    InputForSendPush,
    InputForQueryAllExecuter,
    InputForSendPushToExecutorsWithFilter,
    InputForSetAgreementDatetime,
)
from ..type import executerForAdmin
from ...schema_handler import is_admin
from ....models import (
    Executer,
    Notification,
    ExecutorJumpFinance,
    ExecuterNotice,
    FileInfo,
    RoleAdmin,
)
from ....scripts import exception_handler as EH
from ....scripts.contract_handler import ContractBuilder
from ....scripts.excel_handler import create_blank_with_executors
from ....tasks import send_push
from ....utils.date_time import date_normalize
from ....utils.payment.jump_finance import JumpFinance


class confirmExecuterPayment(graphene.Mutation):
    class Arguments:
        input = InputId(required=True)

    executer = graphene.Field(graphene.NonNull(executerForAdmin))

    @staticmethod
    def mutate(root, info, input):
        is_admin(info=info, permission=RoleAdmin.Roles.EXECUTER_VERIFICATION.value)

        executer = Executer.objects.filter(id=input.id).first()
        if executer is None:
            raise EH.customError("Ошибка", "исполнитель не найден")

        executer.status = "STEP_3_VERIFIED"
        executer.save()

        notify = Notification(
            type=Notification.TypeNotification.ACCOUNT,
            id_instance=executer.pk,
            role="executer",
            read=False,
            text="Ваш аккаунт подтвержден! Добро пожаловать!",
        )
        notify.save(notification=True)

        return confirmExecuterPayment(executer=executer)


class denyExecuterPayment(graphene.Mutation):
    class Arguments:
        input = inputForDenyExecuterPayment(required=True)

    executer = graphene.Field(graphene.NonNull(executerForAdmin))

    @staticmethod
    def mutate(root, info, input):
        is_admin(info=info, permission=RoleAdmin.Roles.EXECUTER_VERIFICATION.value)

        executer = Executer.objects.filter(id=input.id).first()
        if executer is None:
            raise EH.customError("Ошибка", "исполнитель не найден")
        if executer.status == "STEP_3_VERIFIED":
            raise EH.customError("Ошибка", "аккаунт подтвержден")
        executer.status = "STEP_3_VERIFICATION_DECLINED"
        executer.save()
        notify = Notification(
            text=input.text, id_instance=executer.pk, role="executer", type=Notification.TypeNotification.ACCOUNT
        )
        notify.save(notification=True)

        return denyExecuterPayment(executer=executer)


class DeactivateExecutor(graphene.Mutation):
    class Arguments:
        input = InputId(required=True)

    executer = graphene.Field(graphene.NonNull(executerForAdmin))

    @staticmethod
    def mutate(root, info, input):
        is_admin(info=info, permission=RoleAdmin.Roles.EXECUTER_VERIFICATION.value)

        executer = Executer.objects.filter(id=input.id).first()
        if executer is None:
            raise EH.customError("Ошибка", "исполнитель не найден")
        executer.status = "STEP_2_WAITING_FOR_VERIFICATION"
        executer.save()
        notify = Notification(
            text="Ваш профиль деактивирован, обратитесь в HOOPS",
            id_instance=executer.pk,
            role="executer",
            type=Notification.TypeNotification.ACCOUNT,
        )
        notify.save(notification=True)

        return DeactivateExecutor(executer=executer)


class SetPasswordGorExecuter(graphene.Mutation):
    class Arguments:
        input = InputIdPassword(required=True)

    executer = graphene.Field(graphene.NonNull(executerForAdmin))

    @staticmethod
    def mutate(root, info, input):
        is_admin(info=info, permission=RoleAdmin.Roles.EXECUTER.value)
        executer = Executer.objects.filter(id=input.id).first()
        if executer is None:
            raise EH.customError("Ошибка", "исполнитель не найден")
        executer.set_password(input.password)
        executer.save()
        return SetPasswordGorExecuter(executer=executer)


class SendPushToExecuter(graphene.Mutation):
    """
    Отправка push уведомлений Исполнителям Админситратором
    """

    class Meta:
        output = graphene.Boolean

    class Arguments:
        input = InputForSendPush(
            required=True, description="Список идентификаторов Исполниетелей и текст для отправки"
        )

    @staticmethod
    def mutate(root, info, input):
        # проверка на Администратора
        is_admin(info=info, permission=RoleAdmin.Roles.EXECUTER.value)
        # для всех Исполнителей из списка
        for executer in Executer.objects.filter(id__in=input.ids):
            # создаем уведомление
            notify = Notification(
                type=Notification.TypeNotification.OTHER,
                id_instance=executer.pk,
                role="executer",
                read=False,
                text=f"{input.text}",
            )
            # сохраняем
            notify.save(notification=True)
        # если есть флаг отправки уведомления техническому аккаунту
        if input.send_to_technical_account:
            # создаем уведомление для него
            notify = Notification(
                type=Notification.TypeNotification.OTHER,
                id_instance=Executer.get_technical_account(),
                role="executer",
                read=False,
                text=f"{input.text}",
            )
            # сохраняем
            notify.save(notification=True)

        # по пути не было ошибок - успех
        return True


class MarkExecutersAsTest(graphene.Mutation):
    """
    Отметка Исполнителей тестовыми/обычными Админситратором
    """

    class Arguments:
        input = InputForMarkObjectsAsTest(required=True, description="Параметры для проставлени отметок")

    executers = graphene.List(
        graphene.NonNull(executerForAdmin),
        required=True,
        description="Исполнители, над которыми производились манипуляции",
    )

    @staticmethod
    def mutate(root, info, input):
        # проверка на Администратора
        is_admin(info=info, permission=RoleAdmin.Roles.EXECUTER_TEST.value)
        # получаем Исполнителей для обработки
        executors = Executer.objects.prefetch_related("executernotice_set").filter(id__in=input.ids)

        # ДАЛЕЕ НЕОБХОДИМО СДЕЛАТЬ ДОГОВОР И СОЗДАТЬ ПОЛЬЗОВАТЕЛЯ ДЛЯ ВЫПЛАТ В JumpFINANCE

        # если переводим пользователя в нормального - то нужно сделать ему генерацию договора работы
        if input.is_test is False:
            # для всех указанных исполнителей
            for executor in executors:

                # region ГЕНЕРАЦИЯ ДОКУМЕНТА типа ДОГОВОР

                # #  если отсутсвует автоматически сгенерированный документ
                if not executor.executernotice_set.filter(is_auto_generate=True):

                    # создаем уведомление с флагом, что сгененерировано автоматически
                    passport_data = PassportData.objects.filter(executer=executor.id).last()
                    if passport_data is None:
                        continue
                    # создаем запись о договоре
                    doc = ExecuterNotice.objects.create(executer=executor, is_auto_generate=True)
                    # создаем объект создателя документов
                    # document = WordBuilder(path=f'executer_offers/{executor.pk}/{uuid4()}', type_report='CONTRACT')
                    document = ContractBuilder(path=f"executer_offers/{executor.pk}/{uuid4()}", type_report="CONTRACT")
                    # создание договора
                    path = document.executer_offer(
                        fio=executor.full_name,
                        passport=passport_data.full_number,
                        passport_object=f"{passport_data.issued_by} {str(passport_data.date_of_issue.day).zfill(2)}.{str(passport_data.date_of_issue.month).zfill(2)}.{passport_data.date_of_issue.year}",
                        date=date_normalize(input.datetime) if input.datetime else datetime.datetime.now(),
                    )
                    file = FileInfo.objects.create(url=path, fileName="Договор")
                    # добавление файла в уведомления Исполнителя
                    doc.files.add(file)
                    doc.save()
                # endregion

        # обновление у всех флага о состоянии
        executors.update(is_test=input.is_test)
        executors.update(
            agreement_datetime=date_normalize(input.datetime) if input.datetime else datetime.datetime.now()
        )
        # возвращаем пользователей над которыми были манипуляции
        return MarkExecutersAsTest(executers=executors)


class SetAgreementDatetimeForExecuter(graphene.Mutation):
    """
    Установка Даты подписания договора у Исполнителей
    """

    class Arguments:
        input = InputForSetAgreementDatetime(required=True, description="Параметры для установки даты")

    executer = graphene.Field(
        executerForAdmin, required=True, description="Исполнители, над которыми производились манипуляции"
    )

    @staticmethod
    def mutate(root, info, input):
        # проверка на Администратора
        is_admin(info=info, permission=RoleAdmin.Roles.EXECUTER.value)
        # получаем Исполнителей для обработки
        executor = Executer.objects.get(id=input.id)
        assert executor.agreement_datetime is None, "Дата договора уже установлена"
        executor.agreement_datetime = input.agreement_datetime
        executor.save()
        # возвращаем пользователей над которыми были манипуляции
        return SetAgreementDatetimeForExecuter(executer=executor)


class CreateBlankWithExecutors(graphene.Mutation):
    """
    Создание или обновление документа с списком Исполнителей
    """

    class Arguments:
        # на вход фильтры исполнителей
        input = InputForQueryAllExecuter(required=True)

    # в ответ сами выплаты JumpFinance
    path = graphene.String(required=True, description="Путь к файлу с данными")

    def mutate(root, info, input):
        # проверка на админа
        is_admin(info=info, permission=RoleAdmin.Roles.EXECUTER.value)
        res = Executer.objects.select_related("simplerequisite").prefetch_related("professions").filter(is_active=True)
        # фильтруем по входным параметрам
        if input.id_profession:
            res = res.filter(professions__id=input.id_profession)
        if input.list_of_id_profession:
            res = res.filter(professions__id__in=input.list_of_id_profession)
        if input.count_day_for_last_task is not None:
            current_date = timezone.now() - timedelta(days=input.count_day_for_last_task)

            executors_id = Metrics.objects.filter(last_request_task__lte=current_date).values_list(
                "executor__id", flat=True
            )
            res = res.filter(id__in=executors_id)
        if input.count_day_for_end_registration:
            res = res.filter(
                work_expiration__lte=timezone.now() + timedelta(days=input.count_day_for_end_registration)
            )
        if input.count_day_for_end_medical_book:
            res = res.filter(
                medical_book_expiration__lte=timezone.now() + timedelta(days=input.count_day_for_end_medical_book)
            )

        path = create_blank_with_executors(executors=res)

        return CreateBlankWithExecutors(path=path)


class SendPushToExecuters(graphene.Mutation):
    """
    Отправка Push уведомления Исполнителям по фильтрам
    """

    class Meta:
        output = graphene.Boolean

    class Arguments:
        # на вход фильтры исполнителей
        input = InputForSendPushToExecutorsWithFilter(required=True)

    def mutate(root, info, input):
        # проверка на админа
        is_admin(info=info, permission=RoleAdmin.Roles.EXECUTER.value)
        res = Executer.objects.select_related("simplerequisite").prefetch_related("professions").filter(is_active=True)
        # фильтруем по входным параметрам
        if input.id:
            res = res.filter(id=input.id)
        if input.list_of_id_profession:
            res = res.filter(professions__id__in=input.list_of_id_profession)
        if input.id_profession:
            res = res.filter(professions__id=input.id_profession)
        if input.count_day_for_last_task is not None:
            # TODO перевести на метрику
            current_date = timezone.now() - timedelta(days=input.count_day_for_last_task)

            executors_id = Metrics.objects.filter(last_request_task__lte=current_date).values_list(
                "executor__id", flat=True
            )
            res = res.filter(id__in=executors_id)
        if input.count_day_for_end_registration:
            res = res.filter(
                work_expiration__lte=timezone.now() + timedelta(days=input.count_day_for_end_registration)
            )
        if input.is_test is not None:
            res = res.filter(is_test=input.is_test)
        if input.status is not None:
            res = res.filter(status=input.status)
        if input.count_day_for_end_medical_book:
            res = res.filter(
                medical_book_expiration__lte=timezone.now() + timedelta(days=input.count_day_for_end_medical_book)
            )
        # для каждого Исполнителя
        for executor in res:
            # создаем уведомление
            notify = Notification(
                type=Notification.TypeNotification.OTHER,
                id_instance=executor.pk,
                role="executer",
                read=False,
                text=f"{input.text}",
            )
            # сохраняем
            notify.save()

        if input.send_to_technical_account:
            # создаем уведомление для него
            notify = Notification(
                type=Notification.TypeNotification.OTHER,
                id_instance=Executer.get_technical_account(),
                role="executer",
                read=False,
                text=f"{input.text}",
            )
            # сохраняем
            notify.save(notification=True)
        # исключаем пользователей у которых нет токена для пуша
        receivers = list(res.exclude(fcmtoken=None).values_list("fcmtoken__token", flat=True))
        # создаем таску на отправку массовой рассылки
        send_push.delay(text=input.text, fcm_tokens=receivers, url="notifications")
        return True


class SyncJumpFinanceStatus(graphene.Mutation):
    class Arguments:
        input = InputId(required=True)

    executer = graphene.Field(graphene.NonNull(executerForAdmin))

    @staticmethod
    def mutate(root, info, input):
        is_admin(info=info, permission=RoleAdmin.Roles.EXECUTER.value)
        jump_finance = JumpFinance()

        executor = Executer.objects.filter(id=input.id).first()
        assert executor, "Исполнитель не найден"

        executor_jump_finance, created = ExecutorJumpFinance.objects.get_or_create(executer=executor)
        if created or executor_jump_finance.id_contractor is None:
            try:
                # создаем исполнителя в JF по вводным данным и присваиваем идентификатор Исполнителя JF в нашей БД
                executor_jump_finance.id_contractor = jump_finance.create_executor(
                    phone=executor.phone_number_international_format,
                    last_name=executor.middle_name,
                    first_name=executor.first_name,
                    miidle_name=executor.second_name,
                    inn=executor.inn,
                )
                # сохраняем сущность Исполнитель JF
                executor_jump_finance.save()
                if executor_jump_finance.id_contractor == None:
                    raise ValueError("Ошибка создания Исполнителя в JumpFinance")
            # в случае ошибки
            except Exception as e:
                # запись в нашей БД удаляем
                executor_jump_finance.delete()
                # выводим ошибку с текстом БД
                raise ValueError("Ошибка JumpFinance:" + str(e))
            # raise ValueError("Произошло первичное создание Исполнителя JumpFinance")
        res = jump_finance.sync_status_selfemployer_of_executor(contractor_id=executor_jump_finance.id_contractor)
        executor_jump_finance.is_verified = res.get("is_verified", False)
        executor_jump_finance.is_can_pay_taxes = res.get("is_can_pay_taxes", False)
        executor_jump_finance.has_company_agrees_pay_taxes = res.get("has_company_agrees_pay_taxes", False)
        executor_jump_finance.has_warning = res.get("has_warning", False)
        executor_jump_finance.last_message = res.get("messages", {}).get("status", {}).get("detail", None)
        executor_jump_finance.save()
        return SyncJumpFinanceStatus(executer=executor_jump_finance.executer)


class MutationAdminExecuters(graphene.ObjectType):
    """
    Класс мутаций Администратора в отношении Исполнителя
    """

    admin_confirm_executer_payment = confirmExecuterPayment.Field(
        required=True, description="Подтвердить заявку на подтверждения Исполнителя Администратором"
    )
    admin_deny_executer_payment = denyExecuterPayment.Field(
        required=True, description="Отклонить заявку на подтверждения Исполнителя Администратором"
    )
    admin_deactivate_executor_by_id = DeactivateExecutor.Field(
        required=True, description="Деактивация Исполнителя Администратором"
    )

    admin_set_password_for_executer_by_id = SetPasswordGorExecuter.Field(
        required=True, description="Установка пароля для Исполнителя Администратором"
    )
    admin_send_push_for_executer_device_by_list_of_id_executer = SendPushToExecuter.Field(
        required=True, description="Отправка push уведомления для указанных исполнителей Администратором"
    )
    admin_mark_executers_as_test_by_list_of_id = MarkExecutersAsTest.Field(
        required=True, description="Отметка Исполнителей тестовыми/обычными Администратором"
    )
    admin_set_agreement_datetime_for_executer = SetAgreementDatetimeForExecuter.Field(
        required=True, description="Установка даты договора Администратором"
    )
    admin_create_document_with_executors_by_filters = CreateBlankWithExecutors.Field(
        required=True, description="Создание документа с списком Исполнителей по фильтрам"
    )
    admin_send_push_to_executors_by_filters = SendPushToExecuters.Field(
        required=True, description="Отправка Push Исполнителям по фильтрам"
    )

    admin_executer_sync_jump_finance_by_id = SyncJumpFinanceStatus.Field(
        required=True, description="Синхронизация статуса самозанятого у Исполнителя"
    )
