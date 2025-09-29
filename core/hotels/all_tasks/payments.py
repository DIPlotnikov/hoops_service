import logging
from datetime import datetime

from core.celery import app
from hotels.models import PaymentJumpFinance
from hotels.utils.payment.jump_finance import JumpFinance

logger = logging.getLogger(__name__)


@app.task
def create_payments(payments_jumpfinance_list_ids: list):
    payments_jumpfinance = PaymentJumpFinance.objects.filter(id__in=payments_jumpfinance_list_ids)
    root_payment = payments_jumpfinance[0].payment
    try:
        # флаг на обновление признака оплаты Исполнителям у Выплаты
        flag_to_set_flag_is_paid_to_executer = False
        # интерфейс взаимодействия с JumpFinance
        jumpfinance_interface = JumpFinance()
        # для каждой заготовки из списка заготовок JumpFinance
        for payment in payments_jumpfinance:
            try:
                # если есть идентификатор системы JumpFinance
                if payment.id_payment:
                    # производим обновление выплаты
                    payment_dict = jumpfinance_interface.get_payment(id_payment=payment.id_payment)
                    root_payment.log_data += f"Обновление выплаты {payment.id} {datetime.now()}\r\n"
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
                    root_payment.log_data += f"Создание выплаты в JF {payment.id} {datetime.now()}\r\n"
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
                    root_payment.log_data += f"Выплата {payment.id} окончена\r\n"
                # сохраняем заготовку (она уже выплата)
                payment.save()
                # try:
                #     if payment.is_final and payment.status != PaymentJumpFinance.STATUSES[-1][0]:
                #         notify = Notification(
                #             type=Notification.TypeNotification.FINANCE,
                #             text=f"Вам отправлена выплата в размере {payment.amount} руб. за период {payment.payment.period_str}",
                #             role="executer",
                #             id_instance=payment.contractor.executer.id,
                #         )
                #         notify.save(notification=True)
                # except Exception as e:
                #     logger.error(f"Ошибка нотификации: {e}")
                #     pass
            except Exception as e:
                logger.error(f"Ошибка обновления выплаты {payment}: {e}")
                root_payment.log_data += f"Ошибка в {payment.id}: " + str(e) + "\r\n"
                pass
        # отмечаем выплату оплаченной для исполнителя
        if flag_to_set_flag_is_paid_to_executer:
            root_payment.status_executers = "paid_payment"
            root_payment.save()
            root_payment.executerstate_set.update(payment_status="paid_payment")
    except Exception as e:
        logger.error(f"Ошибка обновления выплат: {e}")
        root_payment.log_data += "Ошибка: " + str(e) + "\r\n"
    finally:
        root_payment.log_data += "Обновление выплат завершено " + str(datetime.now()) + "\r\n"
        root_payment.log_data += "------------------\r\n"
        root_payment.is_busy = False
        root_payment.save()
