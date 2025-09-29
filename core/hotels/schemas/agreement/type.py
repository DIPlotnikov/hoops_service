from graphene_django.types import DjangoObjectType
import graphene
from ...models import Agreement, TypeAgreementEnum
from ..schema_fileinfo import FileInfoType


class AgreementType(DjangoObjectType):
    class Meta:
        model = Agreement
    type = graphene.NonNull(TypeAgreementEnum)
    file = graphene.NonNull(FileInfoType)
