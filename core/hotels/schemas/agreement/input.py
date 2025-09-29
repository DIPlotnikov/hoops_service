from ...models import TypeAgreementEnum, TypeDocumentEnum
import graphene
from ..schema_fileinfo import fileInfoInput


class InputTypeAgreement(graphene.InputObjectType):
    type = graphene.NonNull(TypeAgreementEnum)


class InputTypeMedia(graphene.InputObjectType):
    type = graphene.NonNull(TypeDocumentEnum)
    fileName = graphene.String(required=True)


class InputAgreement(InputTypeAgreement):
    file = fileInfoInput(required=True)
