from graphene_django.types import DjangoObjectType, ObjectType
from ...models import ClosingDocument, ClosingDocumentFile
from graphene import relay, Int, Connection, NonNull, ID, List, String, DateTime
from ..hotel.types import HotelType
from ..pagination import ExtendedConnection


class DocumentFileType(DjangoObjectType):
    class Meta:
        model = ClosingDocumentFile


class ClosingDocumentType(DjangoObjectType):
    class Meta:
        model = ClosingDocument
        exclude = ("file_path",'closing_date')
        interfaces = (relay.Node,)
        connection_class = ExtendedConnection
    hotel = NonNull(HotelType)
    id = ID(required=True)
    files = List(NonNull(DocumentFileType), required=True)
    closing_datetime = DateTime(required=True, description='Дата закрытия')

    def resolve(self, info):
        return self.id

    def resolve_hotel(self, info):
        return self.tasks.first().manager.hotel

    def resolve_files(self, info):
        return self.files.all()

    def resolve_closing_datetime(self, info):
        return self.closing_date or self.start_date


