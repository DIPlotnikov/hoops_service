import graphene
from graphene_django.fields import DjangoConnectionField

from ...models import RoleAdmin
from ..schema_handler import is_admin, is_manager
from .input import InputForManagerQueryClosingDocuments, InputForQueryClosingDocument, InputForQueryClosingDocuments
from .type import ClosingDocument, ClosingDocumentType


class QueryClosingDocument(graphene.ObjectType):
    admin_get_closing_documents_by_filters = DjangoConnectionField(
        ClosingDocumentType, input=InputForQueryClosingDocuments(required=True), required=True
    )
    admin_get_closing_document_by_id = graphene.NonNull(
        ClosingDocumentType, input=InputForQueryClosingDocument(required=True)
    )

    manager_get_closing_document_by_id = graphene.NonNull(
        ClosingDocumentType, input=InputForQueryClosingDocument(required=True)
    )
    manager_get_closing_documents_by_filters = DjangoConnectionField(
        ClosingDocumentType, input=InputForManagerQueryClosingDocuments(required=True), required=True
    )

    def resolve_admin_get_closing_documents_by_filters(self, info, input, **kwargs):
        is_admin(info=info, permission=RoleAdmin.Roles.DOCUMENT.value)
        closing_documents = ClosingDocument.objects.all()

        if input.id_hotel:
            closing_documents = (
                closing_documents.filter(tasks__manager__hotel__id=input.id_hotel).order_by("id").distinct()
            )
        if input.is_archive is not None:
            closing_documents = closing_documents.filter(is_archive=input.is_archive)
        if input.is_sent is not None:
            closing_documents = closing_documents.filter(is_sent=input.is_sent)
        if input.start_date and input.end_date:
            start_date = input.start_date.replace(hour=0, minute=0, second=0, microsecond=0)
            closing_documents = closing_documents.filter(start_date__gte=start_date).filter(
                end_date__lte=input.end_date
            )
        if type(input.is_paid) is bool:
            closing_documents = closing_documents.filter(is_paid=input.is_paid)
        return closing_documents

    def resolve_admin_get_closing_document_by_id(self, info, input):
        is_admin(info=info, permission=RoleAdmin.Roles.DOCUMENT.value)
        return ClosingDocument.objects.get(id=input.id)

    def resolve_manager_get_closing_documents_by_filters(self, info, input, **kwargs):
        manager = is_manager(info=info, permission=["DOCUMENTS"])
        closing_documents = ClosingDocument.objects.filter(
            is_sent=True, tasks__manager__hotel__manager=manager
        ).distinct()
        if input.start_date and input.end_date:
            start_date = input.start_date.replace(hour=0, minute=0, second=0, microsecond=0)
            closing_documents = closing_documents.filter(start_date__gte=start_date).filter(
                end_date__lte=input.end_date
            )
        return closing_documents.order_by("pk")

    def resolve_manager_get_closing_document_by_id(self, info, input):
        manager = is_manager(info=info, permission=["DOCUMENTS"])
        return ClosingDocument.objects.filter(
            id=input.id, is_sent=True, tasks__manager__hotel__manager=manager
        ).first()
