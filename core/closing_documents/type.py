from graphene import relay, NonNull, ID, List, DateTime
from graphene_django.types import DjangoObjectType

from closing_documents.models import ClosingDocument, ClosingDocumentFile
from hotels.schemas.hotel.types import HotelType
from hotels.schemas.pagination import ExtendedConnection


class DocumentFileType(DjangoObjectType):
    """Файл закрывающих документов"""

    class Meta:
        model = ClosingDocumentFile


class ClosingDocumentType(DjangoObjectType):
    """Тип Закрывающих документов"""

    class Meta:
        model = ClosingDocument
        exclude = ("file_path", "closing_date")
        interfaces = (relay.Node,)
        connection_class = ExtendedConnection

    hotel = NonNull(HotelType)
    id = ID(required=True)
    files = List(NonNull(DocumentFileType), required=True)
    closing_datetime = DateTime(required=True, description="Дата закрытия")

    def resolve(self, info):
        return self.id

    def resolve_hotel(self, info):
        return self.tasks.first().manager.hotel

    def resolve_files(self, info):
        return self.files.all()

    def resolve_closing_datetime(self, info):
        return self.closing_date or self.start_date
