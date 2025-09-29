import graphene
from .input import InputAgreement
from .type import AgreementType
from ...models import Agreement, FileInfo, Admin, RoleAdmin
from ..schema_handler import is_admin


class AdminUpsertAgreement(graphene.Mutation):
    class Arguments:
        input = InputAgreement(required=True)

    agreement = graphene.NonNull(AgreementType)

    @staticmethod
    def mutate(root, info, input):
        is_admin(info=info, permission=RoleAdmin.Roles.DOCUMENT.value)
        agreements = Agreement.objects.filter(type=input.type)
        agreements.update(is_actual=False)
        file = FileInfo(**input.file)
        file.save()
        agreement = Agreement(file=file, type=input.type)
        agreement.save()
        return AdminUpsertAgreement(agreement=agreement)



class MutationAgreement(graphene.ObjectType):

    admin_upsert_agreement = AdminUpsertAgreement.Field(required=True)
