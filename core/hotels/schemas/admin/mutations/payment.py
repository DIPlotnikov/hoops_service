import logging

import graphene
from django.utils import timezone
from django.utils.datetime_safe import datetime

from ..input import InputCreatePaymentIndividual, InputCreatePayments, InputForCreatePaymentReport, InputId, InputIds
from ..type import PaymentJumpFinanceType, PaymentType
from ...schema_handler import is_admin
from ....all_tasks.payments import create_payments
from ....models import ExecuterState, ExecutorJumpFinance, Notification, Payment, PaymentJumpFinance, RoleAdmin
from ....scripts.excel_handler import create_blank_with_receipt, executer_payment
from ....utils.payment.jump_finance import JumpFinance
from ....utils.tasks import get_executer_by_hotel_id_and_period

logger = logging.getLogger(__name__)


class CreatePayment(graphene.Mutation):
    class Arguments:
        input = InputCreatePayments(required=True)

    payment = graphene.NonNull(PaymentType)

    def mutate(root, info, input):
        admin = is_admin(info=info, permission=RoleAdmin.Roles.PAYMENTS.value, model=True)
        executors_for_paid, tasks = get_executer_by_hotel_id_and_period(
            input.id, input.start_date, input.end_date, type=input.type
        )
        executors_for_paid = executors_for_paid.exclude(payment_status="paid_payment")
        payment = Payment(start_date=input.start_date, end_date=input.end_date, type=input.type, admin=admin)
        payment.save()

        try:
            executors = set(executors_for_paid.values_list("executer__id", flat=True))
            payments_jump_finance = []

            for executor in executors:

                states = executors_for_paid.filter(executer__id=executor)
                tasks = states.values_list("task__id", flat=True)

                summ = sum(state.get_sum_for_pay for state in states)

                if not summ:
                    continue
                purpose = "Оказание услуг по заявкам №" + " и ".join(str(x) for x in tasks)

                contractor, _ = ExecutorJumpFinance.objects.get_or_create(executer=states.last().executer)

                payment_jump_finance = PaymentJumpFinance(
                    payment=payment, contractor=contractor, amount=round(summ, 2), purpose=purpose
                )
                payment_jump_finance.save()
                payments_jump_finance.append(payment_jump_finance)

            payment.file_path_executer = executer_payment(payments_jump_finance, payment.pk)
            [payment.executerstate_set.add(x) for x in executors_for_paid]
            [payment.tasks.add(current_task) for current_task in tasks]
            payment.save()
            executors_for_paid.filter(stop_at__isnull=False).update(payment_status="create_payment")
        except Exception as e:
            payment.delete()
            raise ValueError(e)
        return CreatePayment(payment=payment)


class CreatePaymentIndividual(graphene.Mutation):
    class Arguments:
        input = InputCreatePaymentIndividual(required=True)

    payment = graphene.NonNull(PaymentType)

    def mutate(root, info, input):
        admin = is_admin(info=info, permission=RoleAdmin.Roles.PAYMENTS.value, model=True)

        executers = (
            ExecuterState.objects.select_related("executer")
            .prefetch_related("task_set")
            .filter(id__in=input.id_executer_states)
            .exclude(payment_status="paid_payment")
        )
        assert executers.count() > 0, "Указанные работы помечены оплаченными"

        payment = Payment(start_date=timezone.now(), end_date=timezone.now(), is_individual=True, admin=admin)
        payment.save()
        table_with_executers = {}

        try:
            for executer in executers:
                assert executer.status == "STOP", f"{executer.executer} не закончил работать"
                if executer.executer not in table_with_executers:
                    table_with_executers[executer.executer] = {"tasks": [], "sum": 0.0}
                table_with_executers[executer.executer]["tasks"].append(executer.task.id)
                table_with_executers[executer.executer]["sum"] += round(executer.get_sum_for_pay, 2)
                task = executer.task
                payment.tasks.add(task)
                payment.executerstate_set.add(executer)
                payment.save()
            executer_with_zero = {
                executer_key: sum_value for executer_key, sum_value in table_with_executers.items() if sum_value == 0
            }
            if executer_with_zero:
                raise ValueError(executer_with_zero)
            for executer, info in table_with_executers.items():
                contractor, _ = ExecutorJumpFinance.objects.get_or_create(executer=executer)

                payment_jump_finance = PaymentJumpFinance(
                    payment=payment,
                    contractor=contractor,
                    amount=info.get("sum", 0.0),
                    purpose=f'Оказание услуг по заявке №{", ".join(str(x) for x in info.get("tasks",[]))}',
                )
                payment_jump_finance.save()

                payment.file_path_executer = ""  # executer_payment(payment_jump_finance, payment.pk)

                payment.save()

            executers.update(payment_status="create_payment")
        except Exception as e:
            payment.delete()
            raise ValueError(e)
        return CreatePaymentIndividual(payment=payment)


class MarkPaymentAsPaidToExecuter(graphene.Mutation):
    class Arguments:
        input = InputIds(required=True)

    payments = graphene.List(graphene.NonNull(PaymentType))

    def mutate(root, info, input):
        is_admin(info=info, permission=RoleAdmin.Roles.PAYMENTS.value)
        payments = Payment.objects.filter(id__in=input.ids)
        payments.update(status_executers="paid_payment")
        for payment in payments:
            executors_state = payment.executerstate_set.all()
            executors_state.update(payment_status="paid_payment")
        return MarkPaymentAsPaidToExecuter(payments=payments)


class ArchivePayments(graphene.Mutation):
    class Arguments:
        input = InputIds(required=True)

    payments = graphene.List(graphene.NonNull(PaymentType))

    def mutate(root, info, input):
        is_admin(info=info, permission=RoleAdmin.Roles.PAYMENTS.value)
        payments = Payment.objects.filter(id__in=input.ids)
        payments.update(is_archive=True)
        return ArchivePayments(payments=payments)


class ActivatePayments(graphene.Mutation):
    class Arguments:
        input = InputIds(required=True)

    payments = graphene.List(graphene.NonNull(PaymentType))

    def mutate(root, info, input):
        is_admin(info=info, permission=RoleAdmin.Roles.PAYMENTS.value)
        payments = Payment.objects.filter(id__in=input.ids)
        payments.update(is_archive=False)
        return ActivatePayments(payments=payments)


class UpsertPaymentJumpFinance(graphene.Mutation):
    """
    Создание или обновление выплат в ЛК JumpFinance
    """

    class Arguments:
        # на вход идентификаторы платежек
        input = InputId(required=True)

    # в ответ сами выплаты JumpFinance
    receipts = graphene.List(graphene.NonNull(PaymentJumpFinanceType), required=True)

    def mutate(root, info, input):
        # проверка на админа
        is_admin(info=info, permission=RoleAdmin.Roles.PAYMENTS.value)
        # флаг на обновление признака оплаты Исполнителям у Выплаты
        flag_to_set_flag_is_paid_to_executer = False
        # берем все заготовки платежек JumpFinance c isFinal=False, которые относятся к платежкам на входе
        payments_jumpfinance = (
            PaymentJumpFinance.objects.select_related("payment", "contractor", "contractor__executer__simplerequisite")
            .filter(payment__id=input.id, is_final=False)
            .distinct()
        )
        # интерфейс взаимодецствия с JumpFinance
        jumpfinance_interface = JumpFinance()
        # для каждой заготовки из списка заготовок JumpFinance
        for payment in payments_jumpfinance:
            # если есть идентификатор системы JumpFinance
            if payment.id_payment:
                # производим обновление выплаты
                payment_dict = jumpfinance_interface.get_payment(id_payment=payment.id_payment)
            # если идентификатора нет - выплата не зарегистрирована
            else:
                # обращаемся к JumpFinance для создания выплаты у них
                payment_dict = jumpfinance_interface.create_payment(
                    contractor_id=payment.contractor.id_contractor,
                    account_number=payment.contractor.executer.simplerequisite.card_number,
                    amount=payment.amount,
                    purpose=payment.purpose,
                    id_payment=str(payment.id),
                )
                # из результата забираем внутренний идентификатор
                payment.id_payment = payment_dict.get("id", -1)

            # сумма окончательной выплаты
            payment.amount_paid = payment_dict.get("amount_paid")
            # сумма комиссий
            payment.comission = payment_dict.get("comission")
            # сумма комиссии банка
            payment.comission_bank = payment_dict.get("comission_bank")
            # налоговый сбор
            payment.tax_amount = payment_dict.get("tax_amount")
            # статус выплаты
            payment.status = PaymentJumpFinance.STATUSES[payment_dict.get("status", {}).get("id", 0)][0]
            # если есть чек
            receipt = payment_dict.get("receipt")
            if receipt:
                # забираем идентификатор в налоговой
                payment.fns_key = receipt.get("key")
                # если есть ссылки на чеки
                links = receipt.get("links")
                if links:
                    # ссылка на чек налоговой
                    payment.fns_url = links.get("fns_url")
                    # ссылка на чек локальный от JumpFinance
                    payment.saved_url = links.get("saved_url")
            # забираем флаг окончания выплаты (он тут всегда False - но вдруг автоотмена будет)
            payment.is_final = payment_dict.get("is_final")
            if not flag_to_set_flag_is_paid_to_executer and payment.is_final:
                flag_to_set_flag_is_paid_to_executer = True
            # сохраняем заготовку (она уже выплата)
            payment.save()

            try:
                if payment.is_final and payment.status != PaymentJumpFinance.STATUSES[-1][0]:
                    notify = Notification(
                        type=Notification.TypeNotification.FINANCE,
                        text=f"Вам отправлена выплата в размере {payment.amount} руб. за период {payment.payment.period_str}",
                        role="executer",
                        id_instance=payment.contractor.executer.id,
                    )
                    notify.save(notification=True)
            except Exception as e:
                logger.error(f"Ошибка нотификации: {e}")
                pass
        # отмечаем выплату оплаченной для исполнителя
        if flag_to_set_flag_is_paid_to_executer:
            payment = payments_jumpfinance[0].payment
            payment.status_executers = "paid_payment"
            payment.save()
            payment.executerstate_set.update(payment_status="paid_payment")
        # возвращаем выплаты
        return UpsertPaymentJumpFinance(receipts=payments_jumpfinance)


class UpsertPaymentJumpFinanceAsync(graphene.Mutation):
    """
    Создание или обновление выплат в ЛК JumpFinance асинхронная
    """

    class Arguments:
        # на вход идентификаторы платежек
        input = InputId(required=True)

    class Meta:
        output = graphene.Boolean

    def mutate(root, info, input):
        # проверка на админа
        is_admin(info=info, permission=RoleAdmin.Roles.PAYMENTS.value)
        payment = Payment.objects.get(id=input.id)
        # берем все заготовки платежек JumpFinance c isFinal=False, которые относятся к платежкам на входе
        payments_jumpfinance = (
            PaymentJumpFinance.objects.filter(payment__id=input.id, is_final=False)
            .distinct()
            .values_list("id", flat=True)
        )
        assert payments_jumpfinance.count() > 0, "Не найдено выплат для обработки"
        payment.is_busy = True
        payment.log_data = (payment.log_data or "") + f"Старт платежа {datetime.now()}\r\n"
        payment.save()
        create_payments(payments_jumpfinance_list_ids=list(payments_jumpfinance))
        return True


class CreateDocumentPaymentJumpFinance(graphene.Mutation):
    """
    Создание или обновление документа с чеками
    """

    class Arguments:
        # на вход идентификатор платежки
        input = InputForCreatePaymentReport(required=True)

    # в ответ сами выплаты JumpFinance
    path = graphene.String(required=True, description="Путь к файлу с данными платежки")

    def mutate(root, info, input):
        # проверка на админа
        is_admin(info=info, permission=RoleAdmin.Roles.PAYMENTS.value)
        payments_jumpfinance = (
            PaymentJumpFinance.objects.select_related("payment", "contractor", "contractor__executer__simplerequisite")
            .filter(payment__id=input.id)
            .distinct()
        )
        assert payments_jumpfinance, "Не найдено чеков"
        path = create_blank_with_receipt(
            receipts=payments_jumpfinance,
            to_load_receipts=input.to_load_receipts,
            period=payments_jumpfinance[0].payment.period_str,
            hotel_name=payments_jumpfinance[0].payment.tasks.first().manager.hotel.nameHotel,
        )

        return CreateDocumentPaymentJumpFinance(path=path)


class DeletePayment(graphene.Mutation):
    """
    Удаление платежки
    """

    class Arguments:
        # на вход идентификатор платежки
        input = InputId(required=True)

    class Meta:
        output = graphene.Boolean

    def mutate(root, info, input):
        # проверка на админа
        is_admin(info=info, permission=RoleAdmin.Roles.PAYMENTS.value)
        # получаем Платежку по id
        payment = Payment.objects.prefetch_related("paymentjumpfinance_set").get(id=input.id)
        # проверяем возможность удаления
        assert payment.can_delete is True, "Нельзя удалить платежку"
        # удаляем платежку
        payment.delete()
        return True


class MutationAdminPayment(graphene.ObjectType):
    admin_payment_create_by_period = CreatePayment.Field(required=True)
    admin_payment_create_by_executer_state_as_individual_payment = CreatePaymentIndividual.Field(required=True)

    admin_payment_mark_as_paid_to_executers = MarkPaymentAsPaidToExecuter.Field(required=True)
    admin_payment_archive = ArchivePayments.Field(required=True)
    admin_payment_activate = ActivatePayments.Field(required=True)

    admin_upsert_jumpfinance_payments_by_id_payment = UpsertPaymentJumpFinance.Field(
        required=True, description="Создание/обновление выплат в JumpFinance по ID платежки"
    )
    admin_upsert_jumpfinance_payments_by_id_payment_async = UpsertPaymentJumpFinanceAsync.Field(
        required=True, description="Асинхронное создание/обновление выплат в JumpFinance по ID платежки"
    )

    admin_get_document_with_jumpfinance_payments_by_id_payment = CreateDocumentPaymentJumpFinance.Field(
        required=True, description="Создание/обновление файла с выплатами в JumpFinance по ID платежки"
    )
    admin_delete_payment_by_id = DeletePayment.Field(required=True, description="Удаление Платежки по ID платежки")
