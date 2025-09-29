import graphene
from ...models import Agreement, TypeDocument, TypeAgreementEnum
from .type import AgreementType
from .input import InputTypeAgreement
from ..schema_handler import isAuth


class QueryAgreement(graphene.ObjectType):
    all_get_main_offer = graphene.NonNull(AgreementType)
    all_get_actual_agreement_by_type = graphene.NonNull(AgreementType,
                                                        input=InputTypeAgreement(required=True))
    all_get_agreements_types = graphene.List(graphene.NonNull(TypeAgreementEnum), required=True)
    all_get_all_offers = graphene.List(graphene.NonNull(AgreementType), required=True)
    all_get_all_agreements = graphene.List(graphene.NonNull(AgreementType), required=True)

    def resolve_all_get_offer(self, info):
        isAuth(info)
        return Agreement.objects.get(type=TypeDocument.OFFER.value, is_actual=True)

    def resolve_all_get_actual_agreement_by_type(self, info, input):
        # isAuth(info)
        return Agreement.objects.filter(type=input.type, is_actual=True).first()

    def resolve_all_get_agreements_types(self, info):
        # isAuth(info)
        return Agreement.objects.filter(is_actual=True).distinct().values_list('type', flat=True)

    def resolve_all_get_all_offers(self, info):
        isAuth(info)
        return Agreement.objects.filter(type=TypeDocument.OFFER.value)

    def resolve_all_get_all_agreements(self, info):
        isAuth(info)
        return Agreement.objects.filter(is_actual=True).exclude(type=TypeDocument.OFFER.value)
