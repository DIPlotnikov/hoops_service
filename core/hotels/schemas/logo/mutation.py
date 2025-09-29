import graphene
from .input import InputForUpsertLogo
from ..input import InputID
from .type import LogoType
from ..schema_handler import is_admin
from ...models import FileInfo, Logo, Hotel, RoleAdmin


class UpsertLogo(graphene.Mutation):
    class Arguments:
        input = InputForUpsertLogo(required=True,
                                   description='Массив логотипов')

    logo = graphene.NonNull(LogoType)

    def mutate(root, info, input):
        is_admin(info=info, permission=[RoleAdmin.Roles.CUSTOMER.value], model=True)
        file_info = input.pop('files', [])
        hotel = Hotel.objects.get(id=input.pop('id'))
        logo, created = Logo.objects.select_related('file').update_or_create(hotel=hotel,
                                                                             defaults={**input})

        if created:
            file_info = FileInfo(**file_info[0])
            file_info.save()
            logo.file = file_info
        else:
            if file_info:
                if logo.file:
                    FileInfo.objects.filter(pk=logo.file.pk).update(**file_info[0])
                else:
                    file_info = FileInfo.objects.create(**file_info[0])
                    logo.file = file_info
            else:
                logo.file = None
        logo.save()
        hotel.logo = logo
        hotel.save()
        logo.refresh_from_db()
        return UpsertLogo(logo=logo)


class DeleteLogo(graphene.Mutation):
    class Arguments:
        input = InputID(required=True)

    class Meta:
        output = graphene.Boolean

    def mutate(root, info, input):
        is_admin(info=info, permission=[RoleAdmin.Roles.CUSTOMER.value])
        Logo.objects.filter(hotel__id=input.id).delete()
        return True


class MutationLogo(graphene.ObjectType):
    admin_upsert_logo = UpsertLogo.Field(required=True, description='Создание и обновление логотипов')
    admin_delete_logo = DeleteLogo.Field(required=True, description='Удаление логотипа')

