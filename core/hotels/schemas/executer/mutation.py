import json
import logging
import time
import uuid

from django.conf import settings
from django.utils import timezone
from passports.models import PassportData

from .input import (
    InputAvatar,
    InputForRecoveryPassword,
    InputForSendCode,
    executerInputFileInfo,
    executerInputForCreate,
    executerInputForUpdate,
    executerInputValidatePhone,
    inputIDHotel,
    inputPermints,
    inputPhonenumberPassword,
    inputSetNewPassword,
    CreatePaymentInput,
)
from .type import ExecuterPermintsType, ExecuterType
from ..input import InputCode
from ..scalars import Phonenumber
from ..schema_fileinfo import *
from ..schema_handler import getID, getIDRole, isAuth, isExecuter
from ...models import Executer, FCMToken, Hotel, Notification, PaymentWithCard, PhoneCode, Profession
from ...scripts import exception_handler as EH
from ...scripts import server_handler as SH
from ...tasks import send_sms_code
from ...utils.date_time import date_normalize
from ...utils.payment.tinkoff import TinkoffPayment

logger = logging.getLogger(__name__)


class AuthenticateExecuter(graphene.Mutation):
    class Arguments:
        input = inputPhonenumberPassword(required=True)

    token = graphene.String(required=True, description="Токен Bearer")
    sessionid = graphene.String(required=True, description="Токен sessionid из сеанса")

    @staticmethod
    def mutate(root, info, input):
        executer = Executer.objects.filter(phone_number=input.phonenumber, is_active=True).first()
        if executer is None:
            raise ValueError("Неправильный номер телефона и/или пароль")
        if not executer.check_password(input.password):
            raise PermissionError("Неправильный номер телефона и/или пароль")
        if input.token:
            token, created = FCMToken.objects.get_or_create(token=input.token, executer=executer)
            token.save()
        # set_session(info, executer)

        return AuthenticateExecuter(token=executer.token, sessionid=info.context.session.session_key)


class CreateExecuter(graphene.Mutation):
    class Arguments:
        input = executerInputForCreate(required=True)

    token = graphene.String(required=True)

    @staticmethod
    def mutate(root, info, input):

        assert (
            Executer.objects.filter(is_active=True, phone_number=input.phone_number).exists() is False
        ), "Пользователь с таким номером телефона уже зарегистрирован"
        assert PhoneCode.objects.filter(
            phonenumber=input.phone_number, code=input.pop("code")
        ).exists(), "Неверный код подтверждения"

        try:
            bd = input.pop("birthday")
            bd = date_normalize(
                bd,
            )
            password = input.pop("password")
            professions = input.pop("professions")
            executer = Executer(**input, is_test=True, birthday=bd)
            executer.set_password(password)
            executer.save()
            executer.professions.add(*Profession.objects.filter(id__in=professions))
        except Exception as e:
            raise EH.customError("Ошибка", "пользователь с таким номером телефона уже зарегистрирован")
        return CreateExecuter(token=executer.token)


class UpdateExecuter(graphene.Mutation):
    class Arguments:
        input = executerInputForUpdate(required=True)

    executer = graphene.Field(ExecuterType)
    ok = graphene.Boolean()

    @staticmethod
    def mutate(root, info, input):

        token = isAuth(info)

        executer = Executer.objects.get(id=getID(token))
        flag_break_status = False
        ok = False
        email = str(input.email).strip()
        first_name = input.first_name
        second_name = input.second_name
        middle_name = input.middle_name
        professions = input.professions

        if first_name is not None:
            if executer.first_name != first_name:
                executer.first_name = first_name
                flag_break_status = True
        if second_name is not None:
            if executer.second_name != second_name:
                executer.second_name = second_name
                flag_break_status = True

        if middle_name is not None:
            if executer.middle_name != middle_name:
                executer.middle_name = middle_name
                flag_break_status = True

        if email is not None:
            if executer.email != email:
                executer.email = email
                flag_break_status = True
        if input.birthday:
            if executer.birthday != input.birthday.date():
                executer.birthday = date_normalize(input.birthday)
                flag_break_status = True
        # block of update professions
        if len(professions) >= 0:
            executer.professions.clear()
            executer.professions.add(*Profession.objects.filter(id__in=professions))
        executer.gender = input.gender
        executer.about = input.about
        executer.kind = input.kind
        executer.save()
        if flag_break_status:
            executer.break_status()
        notify = Notification(
            type=Notification.TypeNotification.ACCOUNT,
            id_instance=executer.pk,
            role="executer",
            read=False,
            text="Вы произвели изменение профиля",
        )
        notify.save()
        ok = True
        return UpdateExecuter(ok=ok, executer=executer)


class UpdateAvatarExecuter(graphene.Mutation):
    class Arguments:
        input = InputAvatar(required=True)

    executer = graphene.Field(ExecuterType)
    ok = graphene.Boolean()

    @staticmethod
    def mutate(root, info, input):
        token = isAuth(info)
        executer = Executer.objects.get(id=getID(token))

        if input.avatar:
            old_fileInfo = executer.profile_pic

            if (
                old_fileInfo is not None
                and old_fileInfo.fileName == input.avatar[0].fileName
                and old_fileInfo.timeStamp == input.avatar[0].timeStamp
                and old_fileInfo.fileSize == input.avatar[0].fileSize
            ):
                pass
            else:
                new_fileInfo = FileInfo(
                    fileName=input.avatar[0].fileName,
                    fileSize=input.avatar[0].fileSize,
                    height=input.avatar[0].height,
                    width=input.avatar[0].width,
                    mimeType=input.avatar[0].mimeType,
                    timeStamp=input.avatar[0].timeStamp,
                    url=input.avatar[0].url,
                )
                new_fileInfo.save()
                executer.profile_pic = new_fileInfo
                if old_fileInfo is not None:
                    server = SH.minioDocuments()
                    server.deleteFile(old_fileInfo.url)
                    old_fileInfo.delete()
        else:
            old_fileInfo = executer.profile_pic
            if old_fileInfo is not None:
                server = SH.minioDocuments()
                server.deleteFile(old_fileInfo.url)
                executer.profile_pic = None
                old_fileInfo.delete()
        executer.save()
        return UpdateExecuter(executer=executer)


class executerCreatePayment(graphene.Mutation):
    """
    Проведение акцепта офферты Исполнителем
    """

    class Arguments:
        input = CreatePaymentInput(required=True)

    url = graphene.String(required=True, description="Ссылка на форму оплаты банка")

    @staticmethod
    def mutate(root, info, input):
        token = isAuth(info)
        executer = Executer.objects.get(id=getID(token))
        # проверка правил на запрос подписания офферты
        executer.request_create_payment
        # получение паспорта
        pp = PassportData.objects.filter(executer=executer.id).first()
        # проверка наличия паспортных данных
        assert pp is not None, "Ошибка: заполните паспортные данные"
        # если не резидент РФ
        if pp.citizenship != "Российская Федерация":
            # проверяем разрешение на работу
            if executer.work_expiration is None:
                raise EH.customError("Ошибка", "укажите дату окончания регистрации")
            assert executer.work_expiration > timezone.now(), "Регистрация истекла"
        # создаем оплату в БД
        payment_orm = PaymentWithCard.objects.create(executer=executer)
        # создаем объект интерфейса для TinkoffPay
        payment = TinkoffPayment()
        # создаем оплату в Tinkoff
        payment.create(
            full_name=executer.full_name,
            order_id=payment_orm.id,
            phone=executer.phone_number,
            email=executer.email,
            success_url=info.context.headers.get("origin"),
            success_path=input.success_path,
        )
        # записываем тело операции в БД
        payment_orm.dict_payment = payment.payment_dict
        payment_orm.save()
        # проводим операцию и записываем результат в бд
        data = payment.send()
        payment_orm.status = json.dumps(data)
        payment_orm.save()
        # проверяем статус создания оплаты
        # если не успешно
        if not data["Success"] is True:
            # делаем запись в лог с уникальным идентификатором
            uuid_str = uuid.uuid4()
            logger.error(f"{uuid_str}: {data}")
            raise ValueError(f"Внутренняя ошибка построения платежа. Код ошибки: {uuid_str}")
        # в случае успеха - отправляем ссылку для редиректа на форму оплаты банка
        return executerCreatePayment(url=data["PaymentURL"])


class ExecuterConfirmBankPaymentByOrderID(graphene.Mutation):
    executer = graphene.Field(ExecuterType, required=True)

    class Arguments:
        payment_id = graphene.String(required=True)

    @staticmethod
    def mutate(root, info, payment_id):
        token = isAuth(info)
        executer = Executer.objects.prefetch_related("paymentwithcard_set").get(id=getID(token))
        payment_with_bank = executer.paymentwithcard_set.filter(id=payment_id).last()
        assert payment_with_bank, "Подтверждение платежа не успешно, обратитесь в техническую поддержку"
        payment_tinkoff = TinkoffPayment()
        payment_with_bank.status_cancel = payment_tinkoff.cancel_by_payment_id(payment_with_bank.payment_id)
        payment_with_bank.dict_cancel = payment_tinkoff.payment_dict
        payment_with_bank.save()
        executer.to_wait_verify()
        executer.save()
        return ExecuterConfirmBankPaymentByOrderID(executer=executer)


class executerUpsertPermints(graphene.Mutation):
    class Arguments:
        input = inputPermints(required=True)

    permints = graphene.NonNull(ExecuterPermintsType)

    @staticmethod
    def mutate(root, info, input):
        token = isAuth(info)
        id_o, role = getIDRole(token)
        if str(role) != "2":
            raise EH.customError("Ошибка", "нет прав доступа")
        executer = Executer.objects.get(id=id_o)
        if input.work_expiration:
            executer.work_expiration = date_normalize(input.work_expiration, offset=0)
        executer.medical_book_expiration = date_normalize(input.medical_book_expiration, offset=0)
        executer.save()
        res = ExecuterPermintsType()
        res.work_expiration = input.work_expiration
        res.medical_book_expiration = input.medical_book_expiration
        return executerUpsertPermints(permints=res)


class executerValidatePhone(graphene.Mutation):
    class Arguments:
        input = executerInputValidatePhone(required=True)

    ok = graphene.Boolean()

    @staticmethod
    def mutate(root, info, input):
        phone_code = PhoneCode.objects.filter(**input).first()
        if phone_code is None:
            raise PermissionError("Код подтверждения неверный")
        phone_code.is_valid_number = True
        phone_code.save()
        return executerValidatePhone(ok=True)


class executerSendCode(graphene.Mutation):
    class Arguments:
        input = InputForSendCode(required=True)

    ok = graphene.Boolean(required=True)

    @staticmethod
    def mutate(root, info, input):
        executer = Executer.objects.filter(phone_number=input.phonenumber, is_active=True).first()
        if input.is_request_for_recovery_password:
            assert executer is not None, "Пользователь с таким номером телефона отсутствует!"
        else:
            assert executer is None, "Пользователь с таким номером телефона уже существует!"

        code, _ = PhoneCode.objects.get_or_create(phonenumber=input.phonenumber)
        code.new_code()
        if settings.DEBUG is False:
            # send_sms_code.delay(code=code.code, phonenumber=code.phonenumber)
            send_sms_code(code=code.code, phonenumber=code.phonenumber)
        return executerSendCode(ok=True)


class executerUploadMedia(graphene.Mutation):
    class Arguments:
        input = executerInputFileInfo(required=True)

    url = graphene.String(required=True, description="URL для FileInfo")
    path = graphene.String(required=True, description="Путь для PUT")

    @staticmethod
    def mutate(root, info, input):
        token = isAuth(info)
        server = SH.minioDocuments()
        id = getID(token)
        ts = str(int(time.time()))
        if input.type == "AVATAR":
            uuid4 = str(uuid.uuid4())
            urlUpload = server.getUrlForUploadFile(f"avatars/{ts}/{uuid4}/{input.fileName}")
            path = f"avatars/{ts}/{uuid4}/{input.fileName}"
        elif input.type == "PASSPORT":
            uuid4 = str(uuid.uuid4())
            uuid42 = str(uuid.uuid4())
            urlUpload = server.getUrlForUploadFile(f"private/psrt/{ts}/{uuid4}/{uuid42}/{input.fileName}")
            path = f"private/psrt/{ts}/{uuid4}/{uuid42}/{input.fileName}"
        elif input.type == "DOCUMENT":
            uuid4 = str(uuid.uuid4())
            uuid42 = str(uuid.uuid4())
            urlUpload = server.getUrlForUploadFile(f"private/docs/{ts}/{uuid4}/{uuid42}/{input.fileName}")
            path = f"private/docs/{ts}/{uuid4}/{uuid42}/{input.fileName}"

        pre_url = f"{server.prefix}/{path}"
        return executerUploadMedia(path=pre_url, url=path)


class AddFavoriteHotel(graphene.Mutation):
    class Arguments:
        input = inputIDHotel(required=True)

    executer = graphene.Field(ExecuterType, required=True)

    @staticmethod
    def mutate(root, info, input):
        token = isAuth(info)
        id, role = getIDRole(token)

        if str(role) != "2":
            raise EH.customError("Ошибка", "нет прав доступа (ошибка роли)")
        executer = Executer.objects.get(id=id)
        favorite_hotel = Hotel.objects.get(id=input.id)
        executer.favourites_hotel.add(favorite_hotel)
        executer.save()

        return AddFavoriteHotel(executer=executer)


class RemoveFavoriteHotel(graphene.Mutation):
    class Arguments:
        input = inputIDHotel(required=True)

    executer = graphene.Field(ExecuterType, required=True)

    @staticmethod
    def mutate(root, info, input):
        token = isAuth(info)
        id, role = getIDRole(token)

        if str(role) != "2":
            raise EH.customError("Ошибка", "нет прав доступа (ошибка роли)")
        executer = Executer.objects.get(id=id)
        favorite_hotel = Hotel.objects.get(id=input.id)
        executer.favourites_hotel.remove(favorite_hotel)
        executer.save()
        return RemoveFavoriteHotel(executer=executer)


class ClearFavoriteHotel(graphene.Mutation):
    executer = graphene.Field(ExecuterType, required=True)

    @staticmethod
    def mutate(root, info):
        token = isAuth(info)
        id, role = getIDRole(token)
        if str(role) != "2":
            raise EH.customError("Ошибка", "нет прав доступа (ошибка роли)")
        executer = Executer.objects.get(id=id)
        executer.favourites_hotel.clear()
        executer.save()

        return ClearFavoriteHotel(executer=executer)


class SetNewPassword(graphene.Mutation):
    class Arguments:
        input = inputSetNewPassword(required=True)

    executer = graphene.Field(ExecuterType, required=True)

    @staticmethod
    def mutate(root, info, input):
        token = isAuth(info)
        id, role = getIDRole(token)

        if str(role) != "2":
            raise EH.customError("Ошибка", "нет прав доступа (ошибка роли)")
        executer = Executer.objects.get(id=id)
        if executer.check_password(input.old_password):
            executer.set_password(input.new_password)
            executer.update_password_at = timezone.now()
            executer.save()
        else:
            raise ValueError("Старый пароль не верный")

        return SetNewPassword(executer=executer)


class RequestRecoveryPassword(graphene.Mutation):
    class Arguments:
        phonenumber = Phonenumber(required=True)

    ok = graphene.Boolean(required=True)

    @staticmethod
    def mutate(root, info, phonenumber):
        executer = Executer.objects.filter(phone_number=phonenumber, is_active=True).first()
        if not executer:
            raise ValueError("Пользователь с таким номером телефона отсутствует!")
        code, _ = PhoneCode.objects.get_or_create(phonenumber=phonenumber)
        code.new_code()
        if settings.DEBUG is False:
            send_sms_code(code=code.code, phonenumber=code.phonenumber)
        return RequestRecoveryPassword(ok=True)


class RecoveryPassword(graphene.Mutation):
    class Arguments:
        input = InputForRecoveryPassword(required=True)

    token = graphene.String(required=True)

    @staticmethod
    def mutate(root, info, input):
        code = PhoneCode.objects.filter(phonenumber=input.phonenumber, code=input.code).first()
        assert code is not None, "Неверные данные подтверждения"
        executer = Executer.objects.filter(phone_number=input.phonenumber, is_active=True).first()
        assert executer is not None, "Неверные данные подтверждения"
        executer.set_password(input.password)
        executer.save()
        code.delete()
        return RecoveryPassword(token=executer.token)


class DeleteAccountExecuter(graphene.Mutation):
    ok = graphene.Boolean(required=True)

    @staticmethod
    def mutate(root, info):
        token = isAuth(info)
        id, role = getIDRole(token)
        if str(role) != "2":
            raise EH.customError("Ошибка", "нет прав доступа (ошибка роли)")
        executer = Executer.objects.get(id=id)
        executer.is_active = False
        executer.save()
        Notification(
            type=Notification.TypeNotification.ACCOUNT,
            id_instance=executer.pk,
            role="executer",
            read=False,
            text=f"Ваш аккаунт деактивирован.",
        ).save(notification=True)

        return DeleteAccountExecuter(ok=True)


class RequestDeleteExecutorAccount(graphene.Mutation):

    ok = graphene.Boolean(required=True)

    @staticmethod
    def mutate(root, info):
        id_executer = isExecuter(isAuth(info))
        executer = Executer.objects.filter(id=id_executer).first()
        code, _ = PhoneCode.objects.get_or_create(phonenumber=executer.phone_number)
        code.new_code()
        # if settings.DEBUG is False:
        send_sms_code(code=code.code, phonenumber=code.phonenumber)
        return RequestDeleteExecutorAccount(ok=True)


class DeleteAccountExecuterWithCode(graphene.Mutation):
    ok = graphene.Boolean(required=True)

    class Arguments:
        input = InputCode(required=True)

    @staticmethod
    def mutate(root, info, input):
        id_executer = isExecuter(isAuth(info))
        executer = Executer.objects.get(id=id_executer)
        code = PhoneCode.objects.filter(phonenumber=executer.phone_number, code=input.code).first()
        assert code is not None, "Неверный код подтверждения"
        executer.is_active = False
        executer.save()
        Notification(
            type=Notification.TypeNotification.ACCOUNT,
            id_instance=executer.pk,
            role="executer",
            read=False,
            text="Ваш аккаунт деактивирован.",
        ).save(notification=True)

        return DeleteAccountExecuterWithCode(ok=True)


class MutationExecuter(graphene.ObjectType):
    executer_authenticate = AuthenticateExecuter.Field(required=True)
    executer_create = CreateExecuter.Field(required=True)
    executer_update = UpdateExecuter.Field(required=True)
    executer_update_avatar = UpdateAvatarExecuter.Field(required=True)
    executer_send_code = executerSendCode.Field(required=True)
    executer_upload_media = executerUploadMedia.Field(required=True)
    executer_create_payment = executerCreatePayment.Field(required=True)
    executer_confirm_bank_payment_by_order_id = ExecuterConfirmBankPaymentByOrderID.Field(required=True)
    executer_upsert_permints = executerUpsertPermints.Field(required=True)

    executer_add_favorite_hotel = AddFavoriteHotel.Field(required=True)
    executer_remove_favorite_hotel = RemoveFavoriteHotel.Field(required=True)
    executer_clear_favorite_hotel = ClearFavoriteHotel.Field(required=True)

    executer_set_new_password = SetNewPassword.Field(required=True)
    # executer_delete_account = DeleteAccountExecuter.Field(required=True)
    executer_request_to_delete_account = RequestDeleteExecutorAccount.Field(required=True)
    executer_delete_account_with_code = DeleteAccountExecuterWithCode.Field(required=True)
    executer_request_to_recovery_password_by_phone = RequestRecoveryPassword.Field(required=True)
    executer_recovery_password_by_phone_and_code = RecoveryPassword.Field(required=True)
