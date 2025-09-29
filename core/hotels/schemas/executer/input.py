from ..enums import TypeMedia
from ..scalars import Email, Phonenumber
from ..schema_fileinfo import *
from ...models import Genders


class executerInputForUpdate(graphene.InputObjectType):
    first_name = graphene.String(required=True)
    second_name = graphene.String(required=False)
    middle_name = graphene.String(required=False)
    email = graphene.String()
    professions = graphene.List(graphene.NonNull(graphene.ID), required=True, description="Список id профессий")
    # profile_pic = graphene.List(graphene.NonNull(fileInfoInput), required=True,
    #                            description='Список из 1 элемента с типом метаданных файла')
    gender = graphene.String(required=True, description="male/female")
    birthday = graphene.DateTime(required=True, description="YYYY-MM-DD")
    # requisites = graphene.List(graphene.NonNull(requisitesInput), required=True,
    #                          description="Список с реквизитами исполнителя")

    about = graphene.String(required=True, description="Описание исполнителя")
    kind = graphene.String(required=True, description="Тип исполнителя по умолчанию unknown")


class inputPhonenumberPassword(graphene.InputObjectType):
    phonenumber = Phonenumber(required=True)
    password = graphene.String(required=True)
    token = graphene.String(required=False)


class executerInputForCreate(graphene.InputObjectType):
    first_name = graphene.String(required=True)
    second_name = graphene.String(required=False)
    middle_name = graphene.String(required=True)
    birthday = graphene.DateTime(required=True)
    gender = Genders(required=True)
    email = Email(required=True)
    phone_number = Phonenumber(required=True)
    password = graphene.String(required=True)
    code = graphene.String(required=True)
    professions = graphene.List(graphene.NonNull(graphene.ID), required=True)


class executerInputValidatePhone(graphene.InputObjectType):
    phonenumber = graphene.String(required=True)
    code = graphene.String(required=True)


class InputForSendCode(graphene.InputObjectType):
    phonenumber = graphene.String(required=True)
    is_request_for_recovery_password = graphene.Boolean(required=True, default=True)


class InputForRecoveryPassword(graphene.InputObjectType):
    phonenumber = graphene.String(required=True)
    password = graphene.String(required=True)
    code = graphene.String(required=True)


class executerInputFiles(graphene.InputObjectType):
    file_info_types = graphene.List(graphene.NonNull(fileInfoInput), required=True)


class executerInputFileInfo(graphene.InputObjectType):
    fileName = graphene.String(required=True)
    type = TypeMedia(required=True)


class inputIDHotel(graphene.InputObjectType):
    id = graphene.ID(required=True)


class inputSetNewPassword(graphene.InputObjectType):
    old_password = graphene.String(required=True)
    new_password = graphene.String(required=True)


class inputPermints(graphene.InputObjectType):
    # files = graphene.List(graphene.NonNull(fileInfoInput), required=True, desc='array from permints')
    work_expiration = graphene.DateTime(required=False, desc="expiration date of work")
    medical_book_expiration = graphene.DateTime(required=True, desc="expiration date of medical book")


class InputAvatar(graphene.InputObjectType):
    avatar = graphene.List(graphene.NonNull(fileInfoInput), required=True)


class CreatePaymentInput(graphene.InputObjectType):
    success_path = graphene.String(required=True, description="Путь для успешного платежа")
