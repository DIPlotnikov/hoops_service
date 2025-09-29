from datetime import datetime, timedelta

import graphene

from settings.models import get_nds
from .input import InputForCreateClosingDocuments
from .type import ClosingDocumentType
from ..admin.input import InputIds
from ..schema_handler import is_admin
from ...models import (
    Agreement,
    ClosingDocument,
    ClosingDocumentFile,
    Payment,
    Requisites,
    RoleAdmin,
    TypeAgreementEnum,
)
from ...scripts.act_priem import act_creator
from ...scripts.bill_ver_create import BillCreator
from ...scripts.diadok_builder import DiadokBuilder
from ...scripts.invoice import format_executers_states_to_invoice_format, invoice_creator
from ...utils.date_time import date_normalize
from ...utils.tasks import get_executer_by_hotel_id_and_period, get_tasks_by_hotel_id_and_period


class CreateClosingDocument(graphene.Mutation):
    """
    Создание закрывающих документов Администратором
    """

    class Arguments:
        input = InputForCreateClosingDocuments(
            required=True, description="Параметры для создания закрывающих документов"
        )

    closing_document = graphene.NonNull(ClosingDocumentType)

    def mutate(root, info, input):
        # закрывающие документы доступны Администратору с полным доступом
        admin = is_admin(info=info, permission=RoleAdmin.Roles.DOCUMENT.value, model=True)
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
            nds = get_nds()
            assert nds, "Ставка НДС не указана"
            # получаем актуальную дату Договора оферты
            offer_date = (
                Agreement.objects.filter(is_actual=True, type=TypeAgreementEnum.OFFER.value)
                .first()
                .create_at.date()
                .strftime("%d.%m.%Y")
            )
            # список Исполнителей на оплату
            executors_for_paid, tasks = get_executer_by_hotel_id_and_period(
                input.id, input.start_date, input.end_date, type="primary"
            )

            data_for_payment, sum_for_hoops, sum_for_executer, total_tax = format_executers_states_to_invoice_format(
                executors_for_paid, nds=nds
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
