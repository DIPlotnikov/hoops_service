from datetime import datetime, timedelta
import json

import graphene

from closing_documents.models import ClosingDocument, ClosingDocumentFile
from hotels.models import (
    Agreement,
    Payment,
    Requisites,
    RoleAdmin,
    TypeAgreementEnum,
)
from hotels.schemas.admin.input import InputIds
from hotels.schemas.schema_handler import is_admin
from hotels.scripts.act_priem import act_creator, act_creator_for_group_cd
from hotels.scripts.bill_ver_create import BillCreator, BillCreatorGCD
from hotels.scripts.diadok_builder import DiadokBuilder
from hotels.scripts.invoice import format_executers_states_to_invoice_format, invoice_creator, \
    invoice_creator_for_group_cd
from hotels.utils.date_time import date_normalize
from hotels.utils.tasks import get_executer_by_hotel_id_and_period, get_tasks_by_hotel_id_and_period
from settings.models import get_nds, get_remuneration
from .input import InputForCreateClosingDocuments, CreateGroupedClosingDocumentsInput
from .utils.requisites_utils import check_and_log_requisites_differences
from .type import ClosingDocumentType


class CreateClosingDocument(graphene.Mutation):
    """Создание закрывающих документов Администратором"""

    class Arguments:
        input = InputForCreateClosingDocuments(
            required=True, description="Параметры для создания закрывающих документов"
        )

    closing_document = graphene.NonNull(ClosingDocumentType)

    def mutate(root, info, input):
        # закрывающие документы доступны Администратору с полным доступом
        admin = is_admin(info=info, permission=RoleAdmin.Roles.DOCUMENT.value, model=True)
        # ставка НДС
        nds = get_nds()
        # доля вознаграждения
        remuneration = get_remuneration()
        # получаем актуальную дату Договора оферты
        offer_date = (
            Agreement.objects.filter(is_actual=True, type=TypeAgreementEnum.OFFER.value)
            .first()
            .create_at.date()
            .strftime("%d.%m.%Y")
        )

        # берем все заявки из периода
        tasks = get_tasks_by_hotel_id_and_period(input.id, input.start_date, input.end_date)
        # получаем реквизиты компании
        requisites = Requisites.objects.select_related("owner").get(owner__id=input.id)
        # объект для закрывающих документов
        if not input.closing_date:
            input.closing_date = datetime.now()
        normalize_date = date_normalize(input.closing_date)
        closing_document = ClosingDocument(
            start_date=input.start_date, end_date=input.end_date, closing_date=input.closing_date, admin=admin
        )
        closing_document.save()
        # связываем объект и заявки
        [closing_document.tasks.add(current_task) for current_task in tasks]
        closing_document.save()
        # пробуем
        try:
            # список Исполнителей на оплату
            executors_for_paid, tasks = get_executer_by_hotel_id_and_period(
                input.id, input.start_date, input.end_date, type="primary"
            )

            data_for_payment, sum_for_hoops, sum_for_executer, total_tax = format_executers_states_to_invoice_format(
                executors_for_paid, nds=nds, remuneration_percent=remuneration
            )

            accepted_at = (requisites.owner.accepted_at + timedelta(hours=12)).strftime("%d.%m.%Y")

            # производство счет-фактуры
            file = ClosingDocumentFile(name="Счёт-фактура", amount=0, number="-")
            file.path = invoice_creator(
                executor_states=data_for_payment,
                number=closing_document.pk,
                offer_date=offer_date,
                accepted_at=accepted_at,
                total_price=sum_for_hoops,
                total_tax=total_tax,
                closing_date=normalize_date,
                requisites=requisites,
            )
            file.save()
            closing_document.files.add(file)

            # производство файла диадок

            diadok_file_path, amount_diadok = DiadokBuilder().create_document(
                rows=data_for_payment,
                total_price=sum_for_hoops,
                total_tax=total_tax,
                number=closing_document.pk,
                date=normalize_date,
                inn=requisites.innBank,
                kpp=requisites.kpp,
                hotel_name=requisites.owner.nameLegalEntity,
                legal_address=requisites.legal_address,
                date_offer=offer_date,
                accepted_date=accepted_at,
            )
            file = ClosingDocumentFile.objects.create(
                name="Счёт-фактура Диадок", amount=amount_diadok, number=closing_document.pk, path=diadok_file_path
            )
            closing_document.files.add(file)

            # производство платежки
            payment = Payment(start_date=input.start_date, end_date=input.end_date, admin=admin)
            payment.save()
            # пробуем
            try:
                # список номеров заявок
                # формируем платежки
                bill = BillCreator(
                    number=str(payment.pk),
                    email=tasks[0].manager.hotel.email,
                    ur_name=tasks[0].manager.hotel.nameLegalEntity,
                    adress=tasks[0].manager.hotel.requisites.legal_address,
                    inn=str(tasks[0].manager.hotel.requisites.innBank),
                    kpp=tasks[0].manager.hotel.requisites.kpp,
                    phone=tasks[0].manager.hotel.phone_number,
                    closing_date=normalize_date,
                )
                # формируем оба документа
                payment.file_path_hoops, payment.file_path_hotel = bill.calculateBill(
                    data_for_payment,
                    offer_date=offer_date,
                    hoops_cost=sum_for_hoops,
                    total_tax=total_tax,
                    executer_cost=sum_for_executer,
                    join_documents=input.join_payment_docs,
                )
                payment.save()
            # в случае ошибки
            except Exception as e:
                # удаляем Платежку
                payment.delete()
                raise ValueError(e)
            if input.join_payment_docs:
                # платежка объединенная
                join_file = ClosingDocumentFile(
                    name="Счёт объединенный",
                    path=payment.file_path_hoops,
                    amount=sum_for_hoops + sum_for_executer,
                    number=payment.id,
                )
                join_file.save()
                closing_document.files.add(join_file)
            else:
                # платежка в счет HOOPS
                file_hoops = ClosingDocumentFile(
                    name="Счёт за услуги HOOPS", path=payment.file_path_hoops, amount=sum_for_hoops, number=payment.id
                )
                file_hoops.save()
                closing_document.files.add(file_hoops)
                # платежка в счет Исполнителей
                file_executors = ClosingDocumentFile(
                    name="Счёт за услуги Исполнителей",
                    path=payment.file_path_hotel,
                    amount=sum_for_executer,
                    number=f"{payment.id}/1",
                )
                file_executors.save()
                closing_document.files.add(file_executors)
            payment.delete()

            # акт сдачи приема
            file_act = ClosingDocumentFile(name="Акт сдачи приемки", number=closing_document.pk)
            file_act.path, file_act.amount = act_creator(
                rows=data_for_payment,
                total_tax=total_tax,
                number=closing_document.pk,
                offer_date=offer_date,
                accepted_at=accepted_at,
                inn=requisites.innBank,
                kpp=requisites.kpp,
                hotel_name=requisites.owner.nameLegalEntity,
                address=requisites.legal_address,
                hoops_cost=sum_for_hoops,
                executer_cost=sum_for_executer,
                signer=requisites.signer,
                closing_date=normalize_date,
            )
            file_act.save()
            closing_document.files.add(file_act)
            ##
            closing_document.save()

        # в случае ошибки
        except Exception as e:
            # удаляем объект
            closing_document.delete()
            # толкаем ошибку - в Админку можно сырую
            raise ValueError(e)
        return CreateClosingDocument(closing_document=closing_document)


class CreateGroupedClosingDocuments(graphene.Mutation):
    """Создание закрывающих документов Администратором для всех организаций с указанным ИНН"""

    class Arguments:
        input = CreateGroupedClosingDocumentsInput(
            required=True, description="Параметры для создания закрывающих документов"
        )

    closing_document = graphene.NonNull(ClosingDocumentType)

    def mutate(root, info, input):
        # закрывающие документы доступны Администратору с полным доступом
        admin = is_admin(info=info, permission=RoleAdmin.Roles.DOCUMENT.value, model=True)
        # ставка НДС
        nds = get_nds()
        # доля вознаграждения
        remuneration = get_remuneration()
        # получаем актуальную дату Договора оферты
        offer_date = (
            Agreement.objects.filter(is_actual=True, type=TypeAgreementEnum.OFFER.value)
            .first()
            .create_at.date()
            .strftime("%d.%m.%Y")
        )

        # Валидация ИНН
        inn = str(input.inn or "").strip()
        if not inn.isdigit() or len(inn) not in (10, 12):
            raise ValueError("Некорректный ИНН: допустимы только цифры длиной 10 или 12")

        # Находим все организации по ИНН в реквизитах
        requisites_qs = (
            Requisites.objects.select_related("owner")
            .filter(innBank=inn, owner__isnull=False)
        )
        if not requisites_qs.exists():
            raise ValueError("Организации с указанным ИНН не найдены")

        # Готовим агрегированные данные и список всех заявок
        if not input.closing_date:
            input.closing_date = datetime.now()
        normalize_date = date_normalize(input.closing_date)

        all_tasks = []
        orgs_data = []
        full_data_for_payment = []
        full_sum_for_hoops = 0
        full_sum_for_executer = 0
        full_total_tax = 0

        # Собираем общие данные
        for req in requisites_qs:
            hotel = req.owner
            if not hotel:
                print("[CreateGroupedClosingDocuments] Пропуск: у реквизитов нет владельца (owner)" )
                continue

            # Получаем заявки по организации. Функция может выбрасывать AssertionError, если заявок нет.
            try:
                tasks_by_org = get_tasks_by_hotel_id_and_period(
                    hotel.id,
                    input.start_date,
                    input.end_date
                )
            except AssertionError as e:
                print(f"[CreateGroupedClosingDocuments] Пропуск организации id={hotel.id}: {e}")
                continue
            except Exception as e:
                print(f"[CreateGroupedClosingDocuments] Ошибка при получении заявок для id={hotel.id}: {e}")
                continue

            if not tasks_by_org:
                print(f"[CreateGroupedClosingDocuments] Пропуск организации id={hotel.id}: заявок нет в периоде")
                continue

            # Получаем исполнителей. Функция может выбрасывать AssertionError, если исполнителей нет.
            try:
                executors_for_paid, _ = get_executer_by_hotel_id_and_period(
                    hotel.id,
                    input.start_date,
                    input.end_date,
                    type="primary"
                )
            except AssertionError as e:
                print(f"[CreateGroupedClosingDocuments] Пропуск организации id={hotel.id}: {e}")
                continue
            except Exception as e:
                print(f"[CreateGroupedClosingDocuments] Ошибка при получении исполнителей для id={hotel.id}: {e}")
                continue

            # Формируем данные для счетов. Возможен ValueError (например, незавершённые статусы исполнителей).
            try:
                data_for_payment, sum_for_hoops, sum_for_executer, total_tax = format_executers_states_to_invoice_format(
                    executor_states=executors_for_paid,
                    nds=nds,
                    remuneration_percent=remuneration,
                    hotel=hotel,
                    date_start=input.start_date,
                    date_end=input.end_date,
                )
            except ValueError as e:
                print(f"[CreateGroupedClosingDocuments] Пропуск организации id={hotel.id}: {e}")
                continue
            except Exception as e:
                print(f"[CreateGroupedClosingDocuments] Ошибка форматирования данных для id={hotel.id}: {e}")
                continue

            if not hotel.accepted_at:
                print(f"[CreateGroupedClosingDocuments] Пропуск организации id={hotel.id}: отсутствует accepted_at")
                continue
            accepted_at = (hotel.accepted_at + timedelta(hours=12)).strftime("%d.%m.%Y")

            orgs_data.append(
                {
                    "hotel_id": hotel.id,
                    "hotel_name": hotel.nameLegalEntity,
                    "requisites": {
                        "inn": req.innBank,
                        "kpp": req.kpp,
                        "legal_address": req.legal_address,
                        "signer": req.signer,
                    },
                    "accepted_at": accepted_at,
                    "data_for_payment": data_for_payment,
                    "sum_for_hoops": sum_for_hoops,
                    "sum_for_executer": sum_for_executer,
                    "total_tax": total_tax,
                }
            )

            all_tasks.extend(list(tasks_by_org))

            full_data_for_payment.extend(data_for_payment)
            full_sum_for_hoops += sum_for_hoops
            full_sum_for_executer += sum_for_executer
            full_total_tax += total_tax

            # получаем реквизиты компании TODO ВРЕМЕННО!!!
            requisites = Requisites.objects.select_related("owner").get(owner__id=hotel.id)

        if not orgs_data:
            raise ValueError("Заявки за период не найдены ни у одной организации по указанному ИНН")

        # Сравнение реквизитов между организациями и вывод алармов при отличиях
        check_and_log_requisites_differences(orgs_data)

        # Создаём общий закрывающий документ и привязываем все собранные заявки
        closing_document = ClosingDocument(
            start_date=input.start_date, end_date=input.end_date, closing_date=input.closing_date, admin=admin
        )
        closing_document.save()
        for current_task in all_tasks:
            closing_document.tasks.add(current_task)
        closing_document.save()

        try:

            accepted_at = (requisites.owner.accepted_at + timedelta(hours=12)).strftime("%d.%m.%Y")

            # производство счет-фактуры (УПД)
            file = ClosingDocumentFile(name="Счёт-фактура", amount=0, number="-")
            file.path = invoice_creator_for_group_cd(
                executor_states=full_data_for_payment,
                number=closing_document.pk,
                offer_date=offer_date,
                accepted_at=accepted_at,
                total_price=full_sum_for_hoops,
                total_tax=full_total_tax,
                closing_date=normalize_date,
                requisites=requisites,
                date_start=input.start_date,
                date_stop=input.end_date,
            )
            file.save()
            closing_document.files.add(file)

            # производство файла диадок (групповой формат строк как в счет-фактуре группы)

            diadok_file_path, amount_diadok = DiadokBuilder().create_document_for_group_cd(
                rows=full_data_for_payment,
                total_price=full_sum_for_hoops,
                total_tax=full_total_tax,
                number=closing_document.pk,
                date=normalize_date,
                inn=requisites.innBank,
                kpp=requisites.kpp,
                hotel_name=requisites.owner.nameLegalEntity,
                legal_address=requisites.legal_address,
                date_offer=offer_date,
                accepted_date=accepted_at,
            )
            file = ClosingDocumentFile.objects.create(
                name="Счёт-фактура Диадок", amount=amount_diadok, number=closing_document.pk, path=diadok_file_path
            )
            closing_document.files.add(file)

            # производство платежки
            payment = Payment(start_date=input.start_date, end_date=input.end_date, admin=admin)
            payment.save()
            # пробуем
            try:
                # список номеров заявок
                # формируем платежки
                # todo после такси с уточнением инфы нужно будет поменять.
                bill = BillCreatorGCD(
                    number=str(payment.pk),
                    email=all_tasks[0].manager.hotel.email,
                    ur_name=all_tasks[0].manager.hotel.nameLegalEntity,
                    adress=all_tasks[0].manager.hotel.requisites.legal_address,
                    inn=str(all_tasks[0].manager.hotel.requisites.innBank),
                    kpp=all_tasks[0].manager.hotel.requisites.kpp,
                    phone=all_tasks[0].manager.hotel.phone_number,
                    closing_date=normalize_date,
                )
                # формируем оба документа
                # Параметры hoops_cost/executer_cost не используются внутри calculateBill → не передаем их
                payment.file_path_hoops, payment.file_path_hotel = bill.calculateBill(
                    rows=full_data_for_payment,
                    offer_date=offer_date,
                    total_tax=full_total_tax,
                    join_documents=input.join_payment_docs,
                    for_group=True,
                )
                payment.save()
            # в случае ошибки
            except Exception as e:
                # удаляем Платежку
                payment.delete()
                raise ValueError(e)


            if input.join_payment_docs:
                # платежка объединенная
                join_file = ClosingDocumentFile(
                    name="Счёт объединенный",
                    path=payment.file_path_hoops,
                    amount=full_sum_for_hoops + full_sum_for_executer,
                    number=payment.id,
                )
                join_file.save()
                closing_document.files.add(join_file)
            else:
                # платежка в счет HOOPS
                file_hoops = ClosingDocumentFile(
                    name="Счёт за услуги HOOPS",
                    path=payment.file_path_hoops,
                    amount=full_sum_for_hoops,
                    number=payment.id
                )
                file_hoops.save()
                closing_document.files.add(file_hoops)
                # платежка в счет Исполнителей
                file_executors = ClosingDocumentFile(
                    name="Счёт за услуги Исполнителей",
                    path=payment.file_path_hotel,
                    amount=full_sum_for_executer,
                    number=f"{payment.id}/1",
                )
                file_executors.save()
                closing_document.files.add(file_executors)
            payment.delete()

            # акт сдачи приема
            file_act = ClosingDocumentFile(name="Акт сдачи приемки", number=closing_document.pk)
            file_act.path, file_act.amount = act_creator_for_group_cd(
                rows=full_data_for_payment,
                total_tax=full_total_tax,
                number=closing_document.pk,
                offer_date=offer_date,
                accepted_at=accepted_at,
                inn=requisites.innBank,
                kpp=requisites.kpp,
                hotel_name=requisites.owner.nameLegalEntity,
                address=requisites.legal_address,
                hoops_cost=full_sum_for_hoops,
                executer_cost=full_sum_for_executer,
                signer=requisites.signer,
                closing_date=normalize_date,
                date_start=input.start_date,
                date_stop=input.end_date,
            )
            file_act.save()
            closing_document.files.add(file_act)
            ##
            closing_document.save()

        # в случае ошибки
        except Exception as e:
            # удаляем объект
            closing_document.delete()
            # толкаем ошибку - в Админку можно сырую
            raise ValueError(e)
        return CreateGroupedClosingDocuments(closing_document=closing_document)



class SendClosingDocuments(graphene.Mutation):
    class Arguments:
        input = InputIds(required=True)

    closing_documents = graphene.NonNull(graphene.List(ClosingDocumentType, required=True))

    def mutate(root, info, input):
        is_admin(info=info, permission=RoleAdmin.Roles.DOCUMENT.value)
        closing_documents = ClosingDocument.objects.filter(id__in=input.ids)
        closing_documents.update(is_sent=True)
        return SendClosingDocuments(closing_documents=closing_documents)


class ArchiveClosingDocuments(graphene.Mutation):
    class Arguments:
        input = InputIds(required=True)

    closing_documents = graphene.NonNull(graphene.List(ClosingDocumentType, required=True))

    def mutate(root, info, input):
        is_admin(info=info, permission=RoleAdmin.Roles.DOCUMENT.value)
        closing_documents = ClosingDocument.objects.filter(id__in=input.ids)
        closing_documents.update(is_archive=True)
        return ArchiveClosingDocuments(closing_documents=closing_documents)


class ActivateClosingDocuments(graphene.Mutation):
    class Arguments:
        input = InputIds(required=True)

    closing_documents = graphene.NonNull(graphene.List(ClosingDocumentType, required=True))

    def mutate(root, info, input):
        is_admin(info=info, permission=RoleAdmin.Roles.DOCUMENT.value)
        closing_documents = ClosingDocument.objects.filter(id__in=input.ids)
        closing_documents.update(is_archive=False)
        return ActivateClosingDocuments(closing_documents=closing_documents)


class MarAsPaidClosingDocuments(graphene.Mutation):
    class Arguments:
        input = InputIds(required=True)

    closing_documents = graphene.NonNull(graphene.List(ClosingDocumentType, required=True))

    def mutate(root, info, input):
        is_admin(info=info, permission=RoleAdmin.Roles.DOCUMENT.value)
        closing_documents = ClosingDocument.objects.filter(id__in=input.ids)

        closing_documents.update(is_paid=True)
        return MarAsPaidClosingDocuments(closing_documents=closing_documents)


class BlockPeriodClosingDocuments(graphene.Mutation):
    """
    Блокировка периода на перенос заявок
    """

    class Arguments:
        input = InputIds(required=True)

    closing_documents = graphene.NonNull(graphene.List(ClosingDocumentType, required=True))

    def mutate(root, info, input):
        is_admin(info=info, permission=RoleAdmin.Roles.DOCUMENT.value)
        closing_documents = ClosingDocument.objects.filter(id__in=input.ids)
        closing_documents.update(is_block=True)
        tasks = closing_documents[0].tasks.all()
        tasks.update(is_archived_for_admin=True)
        return BlockPeriodClosingDocuments(closing_documents=closing_documents)


class MutationClosingDocument(graphene.ObjectType):
    adminCreateClosingDocumentByIdHotelAndStartEndDate = CreateClosingDocument.Field(required=True)
    admin_archive_closing_documents = ArchiveClosingDocuments.Field(required=True)
    admin_activate_closing_documents = ActivateClosingDocuments.Field(required=True)
    admin_send_closing_documents = SendClosingDocuments.Field(required=True)
    admin_mark_as_paid_closing_documents = MarAsPaidClosingDocuments.Field(required=True)
    admin_block_period_closing_documents_by_id = BlockPeriodClosingDocuments.Field(
        required=True, description="Блокировка периодов"
    )
    adminCreateGroupedClosingDocuments = CreateGroupedClosingDocuments.Field(required=True)
