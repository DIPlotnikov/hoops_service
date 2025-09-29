import uuid

import graphene

from ...models import Coordinates, FileInfo, Hotel, Manager, Notification, RoleManager, Task
from ...scripts import exception_handler as EH
from ...scripts import server_handler as SH
from ...scripts.bill_ver_create import BillCreator
from ..schema_handler import getIDRoleAdmin, is_manager, isAuth
from .input import inputForCreateHotel, inputForUpdateHotel, inputForUploadFile
from .types import HotelType


def checkAdmin(info):
    id_o, role, _ = getIDRoleAdmin(isAuth(info))
    if role != 1:
        raise EH.customError("Ошибка", "нет прав доступа")

    manager = Manager.objects.filter(id=id_o, is_admin=True).first()
    if manager is None:
        raise EH.customError("Ошибка", "not hotels")
    return manager


class HotelCreate(graphene.Mutation):
    class Arguments:
        input = inputForCreateHotel(required=True)

    token = graphene.String(required=True)

    @staticmethod
    def mutate(root, info, input):
        if Hotel.objects.filter(inn=input.inn).exists():
            raise EH.customError("Ошибка", "данный ИНН уже зарегистрирован")

        hotel = Hotel(
            email=input.email,
            inn=input.inn,
            nameLegalEntity=input.nameLegalEntity,
            nameHotel=input.nameHotel,
            undergroundStation=input.undergroundStation,
        )

        hotel.save()
        coord = Coordinates(**input.coordinates)
        coord.save()
        hotel.coordinates = coord
        hotel.save()

        manager = Manager(email=input.email, hotel=hotel, is_admin=True, status=3)
        manager.set_password(input.password)
        manager.save()
        for role in RoleManager.RolesManager.choices:
            RoleManager.objects.create(manager=manager, role=role[0])
        return HotelCreate(token=manager.token)


class HotelUpdate(graphene.Mutation):
    class Arguments:
        input = inputForUpdateHotel(required=True)

    hotel = graphene.NonNull(HotelType)

    @staticmethod
    def mutate(root, info, input):
        manager = is_manager(info=info, permission=["HOTEL_UPDATE"])
        hotel = manager.hotel

        if hotel.status == "STEP_3_VERIFIED":
            if hotel.nameLegalEntity != input.nameLegalEntity:
                hotel.status = "STEP_1_REGISTERED"
            if hotel.nameHotel != input.nameHotel:
                hotel.status = "STEP_1_REGISTERED"
            hotel.save()

        email = input.email
        nameLegalEntity = input.nameLegalEntity
        postalAddress = input.postalAddress
        nameHotel = input.nameHotel
        undergroundStation = input.undergroundStation
        profile_pic = input.profile_pic

        if email is not None:
            hotel.email = email
            manager = hotel.get_admin
            manager.email = email
            manager.save()
        if nameLegalEntity is not None:
            hotel.nameLegalEntity = nameLegalEntity
        if postalAddress is not None:
            hotel.postalAddress = postalAddress
        if nameHotel is not None:
            hotel.nameHotel = nameHotel
        if undergroundStation is not None:
            hotel.undergroundStation = undergroundStation
        if input.inn is not None:
            hotel.inn = input.inn

        if profile_pic is not None and len(profile_pic) > 0:
            old_fileInfo = hotel.profile_pic

            if (
                old_fileInfo is not None
                and old_fileInfo.fileName == profile_pic[0].fileName
                and old_fileInfo.timeStamp == profile_pic[0].timeStamp
                and old_fileInfo.fileSize == profile_pic[0].fileSize
            ):
                pass
            else:

                new_fileInfo = FileInfo(
                    fileName=profile_pic[0].fileName,
                    fileSize=profile_pic[0].fileSize,
                    height=profile_pic[0].height,
                    width=profile_pic[0].width,
                    mimeType=profile_pic[0].mimeType,
                    timeStamp=profile_pic[0].timeStamp,
                    url=profile_pic[0].url,
                )
                new_fileInfo.save()
                hotel.profile_pic = new_fileInfo
                if old_fileInfo is not None:
                    server = SH.minioDocuments()
                    server.deleteFile(old_fileInfo.url)
                    old_fileInfo.delete()
        else:
            old_fileInfo = hotel.profile_pic
            if old_fileInfo is not None:
                server = SH.minioDocuments()
                server.deleteFile(old_fileInfo.url)
                hotel.profile_pic = None
                old_fileInfo.delete()

        if input.coordinates is not None:
            if hotel.coordinates is None:
                coord = Coordinates(**input.coordinates)
                coord.save()
                hotel.coordinates = coord
            elif hotel.coordinates is not None:
                coord = Coordinates.objects.filter(id=hotel.coordinates.id)
                coord.update(**input.coordinates)

        else:
            if hotel.coordinates is not None:
                coord = Coordinates.objects.get(id=hotel.coordinates.id)
                coord.delete()
                hotel.coordinates = None

        ###
        # конец обработки координат
        ###
        hotel.save()
        notify = Notification(
            type=Notification.TypeNotification.ACCOUNT,
            id_instance=manager.pk,
            role="manager",
            read=False,
            text="Вы произвели изменение профиля гостиницы",
        )
        notify.save()
        return HotelUpdate(hotel=hotel)


class HotelUploadMedia(graphene.Mutation):
    class Arguments:
        input = inputForUploadFile(required=True)

    url = graphene.String(required=True, description="URL для FileInfo")
    path = graphene.String(required=True, description="Путь для PUT")

    def mutate(root, info, input):
        manager = is_manager(info=info, permission=["HOTEL_UPDATE"])
        server = SH.minioDocuments()

        uuid4 = str(uuid.uuid4())
        server.getUrlForUploadFile(f"avatars/{manager.hotel.pk}/{uuid4}/{input.fileName}")
        # pre_path = 'https://api.hotelsgo.work:9000/my-bucket-hotel/'
        path = f"avatars/{manager.hotel.pk}/{uuid4}/{input.fileName}"
        pre_url = f"{server.prefix}/{path}"

        return HotelUploadMedia(path=pre_url, url=path)


class HotelCreatePayment(graphene.Mutation):
    hotel = graphene.Field(HotelType, required=True)

    def mutate(root, info):
        manager = is_manager(info=info, permission=["HOTEL_UPDATE"])
        if hasattr(manager.hotel, "requisites") is False:
            raise EH.customError("Ошибка", "нет реквизитов")
        if not hasattr(manager.hotel, "coordinates"):
            raise EH.customError("Ошибка", "не указан адрес")

        bill = BillCreator(
            number=str(manager.hotel.id),
            email=manager.hotel.email,
            ur_name=manager.hotel.nameLegalEntity,
            adress=manager.hotel.requisites.legal_address,
            inn=str(manager.hotel.inn),
            kpp=manager.hotel.requisites.kpp,
            phone=manager.hotel.phone_number,
        )
        bill.send_bill_for_verification(
            url=info.context.headers.get("Origin"),
            nds=0.17,
        )
        manager.hotel.save()
        return HotelCreatePayment(hotel=manager.hotel)


class HotelVerificationRequest(graphene.Mutation):
    hotel = graphene.Field(HotelType, required=True)

    def mutate(root, info):
        manager = is_manager(info=info, permission=["HOTEL_UPDATE"])
        manager.hotel.status = "STEP_2_WAITING_FOR_VERIFICATION"
        manager.hotel.save()
        return HotelVerificationRequest(hotel=manager.hotel)


class HotelChangeAutoApproveTasks(graphene.Mutation):
    hotel = graphene.Field(HotelType, required=True)

    def mutate(root, info):
        manager = is_manager(info=info, permission=["HOTEL_UPDATE"])
        manager.hotel.auto_approve_tasks = not manager.hotel.auto_approve_tasks
        manager.hotel.save()
        if manager.hotel.auto_approve_tasks:
            tasks = Task.objects.filter(manager__hotel=manager.hotel, is_approved=False).exclude(status="DELETED")
            tasks.update(is_approved=True)
        return HotelChangeAutoApproveTasks(hotel=manager.hotel)


class HotelChangeAllowToUseBasicProfession(graphene.Mutation):
    """
    Мутация изменения флага использования базовых профессий в заявках
    """

    hotel = graphene.Field(HotelType, required=True)

    def mutate(root, info):
        manager = is_manager(info=info, permission=["SETTINGS_EDIT"])
        manager.hotel.is_allow_to_use_basic_profession = not manager.hotel.is_allow_to_use_basic_profession
        manager.hotel.save()
        return HotelChangeAutoApproveTasks(hotel=manager.hotel)


class MutationHotel(graphene.ObjectType):
    manager_create_hotel = HotelCreate.Field(required=True)
    manager_update_hotel = HotelUpdate.Field(required=True)
    manager_upload_media = HotelUploadMedia.Field(required=True)
    manager_create_payment = HotelCreatePayment.Field(required=True)
    manager_validate_requisites = HotelVerificationRequest.Field(required=True)
    manager_change_auto_approve_tasks = HotelChangeAutoApproveTasks.Field(required=True)
    manager_change_allow_to_use_basic_professions = HotelChangeAllowToUseBasicProfession.Field(required=True)
