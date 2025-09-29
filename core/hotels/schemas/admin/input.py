import graphene

from ..enums import PaymentEnum, PaymentStatus
from ..input import InputIDs
from ...models import Hotel, RoleAdmin, StatusExecuterEnum


class adminInputForAuth(graphene.InputObjectType):
    name = graphene.String(required=True, description="Имя администратора")
    password = graphene.String(required=True, description="Пароль")


class InputForUpsertAdmin(adminInputForAuth):
    """
    Инпут для создания/обновления Администратора
    """

    id = graphene.ID(required=False, description="ID Администратора")
    password = graphene.String(required=False, description="Пароль")
    role = graphene.String(required=True, description="Роль Администратора")
    percent = graphene.Float(required=True, description="Процент")
    roles = graphene.List(graphene.NonNull(RoleAdmin.RolesEnum), required=True, description="Роли Администратора")


class InputForSendPush(InputIDs):
    """
    Инпут отправки push уведомлений
    """

    text = graphene.String(required=True, description="Текст уведомления")
    send_to_technical_account = graphene.Boolean(
        required=True, descrption="Флаг на отправку уведомления техническомуц аккаунту"
    )


class adminInputForDeactivateAdmin(graphene.InputObjectType):
    name = graphene.String(required=True)


class inputEmail(graphene.InputObjectType):
    email = graphene.String(required=False)


class InputForQueryAllExecuter(inputEmail):
    """
    ИНпут запроса списка Исполнителей
    """

    id = graphene.ID(required=False, description="ID Исполнителя")
    id_profession = graphene.ID(
        required=False, description="ID Профессии", deprecation_reason="Переход к множественному фильтру"
    )
    list_of_id_profession = graphene.List(graphene.NonNull(graphene.ID), required=False, description="ID Профессии")
    status = graphene.Field(StatusExecuterEnum, description="Статус Исполнителя")
    phone = graphene.String(required=False, description="Номер телефона Исполнителя")
    full_name = graphene.String(required=False, description="Имя Исполнителя")
    inn = graphene.String(required=False, description="ИНН Исполнителя")
    is_test = graphene.Boolean(required=False, description="Флаг на тестовый аккаунт Исполнителя")
    count_day_for_last_task = graphene.Int(
        required=False, description="Количество дней после крайне заявки до сегодня"
    )
    count_day_for_end_registration = graphene.Int(
        required=False, description="Количество дней до окончания регистрации"
    )
    count_day_for_end_medical_book = graphene.Int(
        required=False, description="Количество дней до окончания медицинской книжки"
    )

    citizenship = graphene.String(required=False, description="Гражданство")
    agreement_datetime = graphene.DateTime(required=False, description="Дата подписания договора")


class InputForSendPushToExecutorsWithFilter(inputEmail):
    """
    ИНпут для отправки Push уведомления Исполнителям по фильтрам
    """

    full_name = graphene.String(required=False)
    id_profession = graphene.ID(
        required=False, description="ID Профессии", deprecation_reason="Переход к множественному фильтру"
    )
    id = graphene.ID(required=False, description="ID Исполнителя")

    list_of_id_profession = graphene.List(graphene.NonNull(graphene.ID), required=False, description="ID Профессии")

    count_day_for_last_task = graphene.Int(
        required=False, description="Количество дней после крайне заявки до сегодня"
    )
    count_day_for_end_registration = graphene.Int(
        required=False, description="Количество дней до окончания регистрации"
    )
    count_day_for_end_medical_book = graphene.Int(
        required=False, description="Количество дней до окончания медицинской книжки"
    )
    text = graphene.String(required=True, description="Текст уведомления")
    send_to_technical_account = graphene.Boolean(
        required=True, descrption="Флаг на отправку уведомления техническомуц аккаунту"
    )
    is_test = graphene.Boolean(required=False, description="Флаг на тестовый аккаунт Исполнителя")
    status = graphene.Field(StatusExecuterEnum, description="Статус Исполнителя")


class InputForQueryAllHotels(graphene.InputObjectType):
    """
    Инпут запроса всех гостиниц
    """

    id = graphene.ID(required=False, description="ID Гостиницы")
    nameHotel = graphene.String(required=False, description="Наименование Гостиницы")
    nameLegalEntity = graphene.String(required=False, description="Юридическое наименование Гостиницы")
    email = graphene.String(required=False, description="Email Гостиницы")
    inn = graphene.String(required=False, description="ИНН Гостиницы")
    is_test = graphene.Boolean(requred=False, description="Флаг-указатель тестовой Гостиницы")
    status = Hotel.StatusesEnum(required=False, description="Статус Гостиницы")


class inputEmailAndInn(graphene.InputObjectType):
    id = graphene.ID(required=False, description="ID менеджера")
    inn = graphene.String(required=False, description="ИНН гостиницы")
    manager_full_name = graphene.String(required=False, description="Имя менеджера")
    manager_email = graphene.String(required=False, description="Email менеджера")
    hotel_name = graphene.String(required=False, description="Наименование гостиницы")
    is_test = graphene.Boolean(required=False, description="Флаг тестового периода гостиницы")
    hotel_id = graphene.ID(required=False, description="Идентификатор гостиницы")


class Objects(graphene.Enum):
    executer = "executer"
    manager = "manager"


class inputForAcess(graphene.InputObjectType):
    role = graphene.NonNull(Objects)
    id = graphene.ID(required=True)


class InputId(graphene.InputObjectType):
    id = graphene.ID(required=True)


class InputForSetSettingsHotel(InputId):
    max_count_of_personal_profession = graphene.Int(required=True, description="Максимальное количество Экс профессий")
    payment_period_to_hoops = graphene.NonNull(Hotel.PaymentPeriodToHoopsEnum, description=" Период оплат гостиниц")
    payment_period_to_executor = graphene.NonNull(
        Hotel.PaymentPeriodToExecutorEnum, description=" Период выплат Исполнителям"
    )

    may_use_additional_in_tasks = graphene.Boolean(
        required=True, description="Признак разрешения использования доп информации в Заявках"
    )


class InputIdPassword(graphene.InputObjectType):
    id = graphene.ID(required=True)
    password = graphene.String(required=True)


class InputIdAndArchive(InputId):
    id = graphene.ID(required=False)
    is_archive = graphene.Boolean(required=False)
    start_date = graphene.DateTime(required=False)
    end_date = graphene.DateTime(required=False)
    status_executer = PaymentStatus(required=False)
    status_hotel = PaymentStatus(required=False)


class InputArchive(graphene.InputObjectType):
    is_archive = graphene.Boolean(required=True)


class InputIds(graphene.InputObjectType):
    ids = graphene.List(graphene.NonNull(graphene.ID), required=True)


class InputForMarkObjectsAsTest(InputIds):
    is_test = graphene.Boolean(required=True)
    datetime = graphene.DateTime(required=False)


class InputCreatePayments(graphene.InputObjectType):
    id = graphene.ID(required=True)
    start_date = graphene.DateTime(required=True)
    end_date = graphene.DateTime(required=True)
    type = PaymentEnum(required=True)


class InputCreatePaymentIndividual(graphene.InputObjectType):
    """
    Параметры создания платежки по идентификатору заявки и исполнителя
    """

    id_executer_states = graphene.List(
        graphene.NonNull(graphene.ID), required=True, description="Идентификаторы отклика Исполнителя"
    )


class inputPaymentStatus(graphene.InputObjectType):
    status = PaymentStatus(required=False)
    id = graphene.ID(required=False)
    start_date = graphene.DateTime(required=False)
    end_date = graphene.DateTime(required=False)


class inputForDenyExecuterPayment(InputId):
    text = graphene.String(required=True)


class InputNameHotel(graphene.InputObjectType):
    nameHotel = graphene.String(required=True)


class InputName(graphene.InputObjectType):
    name = graphene.String(required=True)


class InputForGetExecuterByName(graphene.InputObjectType):
    """
    Параметры поиска Исполнителя по имени
    """

    name = graphene.String(required=True, description="Имя пользователя")
    is_test = graphene.Boolean(required=False, description="Тестовый пользователь")
    status = graphene.Field(StatusExecuterEnum, description="Статус Исполнителя")


class InputNameOrInn(graphene.InputObjectType):
    nameOrInn = graphene.String(required=True)


class InputINN(graphene.InputObjectType):
    inn = graphene.String(required=True)


class InputForFilterHotels(graphene.InputObjectType):
    """
    Фильтрация Гостиниц
    """

    inn = graphene.String(required=False)
    name = graphene.String(required=False)
    id = graphene.String(required=False)
    innOrName = graphene.String(required=False)


class InputManagerIDAdminID(graphene.InputObjectType):
    """
    Инпут идентификаторов менеджера и админа
    """

    manager_id = graphene.ID(required=True, description="ID менеджер")
    admin_id = graphene.ID(required=True, description="ID админ")


class InputForSetAgreementDatetime(graphene.InputObjectType):
    id = graphene.ID(required=True, description="Исполнитель")
    agreement_datetime = graphene.DateTime(required=True, description="Дата договора")


class InputForCreatePaymentReport(graphene.InputObjectType):
    id = graphene.ID(required=True, description="Платеж")
    to_load_receipts = graphene.Boolean(required=True, description="Выгрузка чеков")
