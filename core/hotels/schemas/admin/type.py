import graphene
from graphene import ObjectType, relay
from graphene_django.types import DjangoObjectType

from passports.models import PassportData
from passports.type import PassportDataType
from ..enums import PaymentEnum
from ..executer.type import ExecuterType
from ..notice_executer.type import ExecuterNoticeType
from ..pagination import ExtendedConnection
from ..schema_address import AddressType
from ..schema_fileinfo import FileInfoType
from ..scheme_requisites import SimpleRequisiteType
from ...models import (
    Admin,
    Executer,
    Hotel,
    Manager,
    Payment,
    PaymentJumpFinance,
    RoleAdmin,
    StatusExecuterEnum,
)


class JumpFinanceContractor(ObjectType):
    id_contractor = graphene.Int(
        required=False, default_value=0, description="Идентификатор исполнителя в JumpFinance"
    )

    is_verified = graphene.Boolean(
        required=True, description="Получено подтверждение из налоговой," "что исполнитель привязан к компании"
    )
    is_can_pay_taxes = graphene.Boolean(
        required=True,
        description="Получено подтверждение из налоговой," "что самозанятый разрешил компании уплачивать налог",
    )
    has_company_agrees_pay_taxes = graphene.Boolean(
        required=True,
        description="В настройках исполнителя включена опция," "что компания уплачивает налог за исполнителя",
    )
    has_warning = graphene.Boolean(
        required=True, description="Не хватает каких-либо разрешений со стороны самозанятого"
    )

    last_message = graphene.String(required=False, description="Последнее сообщение от JumpFinance")

    create_at = graphene.DateTime(required=True, description="Время создания")
    update_at = graphene.DateTime(required=False, description="Время последнего обновления")


class adminAuthType(DjangoObjectType):
    class Meta:
        model = Admin
        exclude = (
            "password",
            "payment_set",
            "closingdocument_set",
            "notice_set",
            "post_set",
            "infoblock_set",
            "roleadmin_set",
            "permissions",
        )

    token = graphene.String(required=True)
    roles = graphene.List(graphene.NonNull(RoleAdmin.RolesEnum), required=True, description="Роли Админа")

    def resolve_token(self, info):
        return Admin.objects.get(id=self.id).token

    def resolve_roles(self, info):
        return self.roleadmin_set.all().values_list("role", flat=True)


class adminType(DjangoObjectType):
    class Meta:
        model = Admin
        exclude = (
            "password",
            "logo_set",
            "post_set",
            "executernotice_set",
            "managers",
            "roleadmin_set",
            "payment_set",
            "closingdocument_set",
            "notice_set",
            "infoblock_set",
            "permissions",
        )
        interfaces = (relay.Node,)
        connection_class = ExtendedConnection

    id = graphene.ID(required=True)
    roles = graphene.List(graphene.NonNull(RoleAdmin.RolesEnum), required=True, description="Роли Админа")

    def resolve_id(self, info):
        return self.pk

    def resolve_roles(self, info):
        return self.roleadmin_set.all().values_list("role", flat=True)


class hotelForAdmin(DjangoObjectType):
    class Meta:
        model = Hotel
        interfaces = (relay.Node,)
        connection_class = ExtendedConnection

    inn = graphene.String(required=True)

    id = graphene.ID(required=True)
    rating = graphene.Float(required=True)
    main_manager_full_name = graphene.String(required=True)

    def resolve_rating(self, info):
        return 4.99

    def resolve_inn(self, info):
        inn = str(self.inn)
        if inn == "0":
            return ""
        return inn.zfill(10)

    def resolve_id(self, info):
        return self.pk

    def resolve_main_manager_full_name(self, info):
        return self.manager_set.filter(is_admin=True).first().fullname


class managerForAdmin(DjangoObjectType):
    class Meta:
        model = Manager
        exclude = ("password",)

        interfaces = (relay.Node,)
        connection_class = ExtendedConnection

    id = graphene.ID(required=True)
    token = graphene.String(required=True)

    def resolve_token(self, info):
        return self.token_for_admin

    def resolve_id(self, info):
        return self.pk

    hotel = graphene.NonNull(hotelForAdmin)

    def resolve_hotel(self, info):
        return self.hotel


class adminForAdmin(DjangoObjectType):
    class Meta:
        model = Admin
        exclude = (
            "password",
            "logo_set",
            "post_set",
            "executernotice_set",
            "payment_set",
            "closingdocument_set",
            "notice_set",
            "infoblock_set",
            "managers",
        )
        interfaces = (relay.Node,)
        connection_class = ExtendedConnection

    id = graphene.ID(required=True)

    def resolve_id(self, info):
        return self.pk


class executerForAdmin(DjangoObjectType):
    class Meta:
        model = Executer
        exclude = (
            "password",
            "favourites_hotel",
            "executerfiles_set",
            "executerstate_set",
            "requisites",
            "executerstatdoc_set",
            "feedbackmanager_set",
            "manager_set",
            "feedbackexecuter_set",
        )

        interfaces = (relay.Node,)
        connection_class = ExtendedConnection

    id = graphene.ID(required=True, description="ID Исполнителя")
    status = graphene.NonNull(StatusExecuterEnum, description="Статус Исполнителя")
    simplerequisite = graphene.NonNull(SimpleRequisiteType, description="Реквизиты Исполнителя")

    count_day_for_last_task = graphene.Int(required=False, description="Количество дней от последней заявки")
    count_day_for_end_registration = graphene.Int(
        required=False, description="Количество дней до окончания регистрации"
    )
    count_day_for_end_medical_book = graphene.Int(
        required=False, description="Количество дней до окончания медицинской книжки"
    )
    executernotice_set = graphene.List(
        graphene.NonNull(ExecuterNoticeType), required=True, description="Уведомления Исполнителя"
    )
    token = graphene.String(required=True, description="Токен доступа для Адмнистратора")
    inn = graphene.String(required=True, description="ИНН Исполнителя")
    profile_pic = graphene.List(graphene.NonNull(FileInfoType), required=True, description="Аватар Исполнителя")
    passportData = graphene.Field(PassportDataType, required=False, description="Паспорт Исполнителя")
    address = graphene.Field(AddressType, description="Адрес Исполнителя")
    is_admin_can_send_push = graphene.Boolean(required=True, description="Флаг возможности отправки push уведомления")
    jump_finance = graphene.Field(JumpFinanceContractor, description="Профиль JumpFinance")

    citizenship = graphene.String(required=True, description="Гражданство")
    notice = graphene.Field(ExecuterNoticeType, required=False, description="Уведомление (не РФ)")

    def resolve_id(self, info):
        return self.pk

    def resolve_count_day_for_last_task(self, info):
        return self.count_day_for_last_task

    def resolve_count_day_for_end_registration(self, info):
        return self.count_day_for_end_registration

    def resolve_count_day_for_end_medical_book(self, info):
        return self.count_day_for_end_medical_book

    def resolve_executernotice_set(self, info):
        return self.executernotice_set.all()

    def resolve_token(self, info):
        return self.token_for_admin

    def resolve_inn(self, info):
        if hasattr(self, "simplerequisite"):
            return self.simplerequisite.inn.zfill(12)
        return "ИНН отсутсвует"

    def resolve_profile_pic(self, info):
        return [self.profile_pic] if self.profile_pic is not None else []

    def resolve_passportData(self, info):
        return PassportData.objects.filter(executer=self.id).first()

    def resolve_is_admin_can_send_push(self, info):
        return bool(self.fcmtoken_set.all())

    def resolve_jump_finance(self, info):
        return getattr(self, "executorjumpfinance", None)

    def resolve_citizenship(self, info):
        passport = PassportData.objects.filter(executer=self.id).first()
        if passport:
            return passport.citizenship
        return ""

    def resolve_notice(self, info):
        return self.executernotice_set.exclude(is_auto_generate=True).first()


class PaymentJumpFinanceType(DjangoObjectType):
    class Meta:
        model = PaymentJumpFinance
        interfaces = (relay.Node,)
        connection_class = ExtendedConnection
        exclude = ("payment",)
        description = "Выплата JumpFinance"

    id = graphene.ID(required=True)
    executer = graphene.NonNull(ExecuterType, description="Исполнитель")

    def resolve_id(self, info):
        return self.pk

    def resolve_executer(self, info):
        return self.contractor.executer

    def resolve_executer(self, info):
        return self.contractor.executer


class PaymentType(DjangoObjectType):
    class Meta:
        model = Payment
        interfaces = (relay.Node,)
        connection_class = ExtendedConnection
        exclude = ("tasks", "paymentjumpfinance_set")

    id = graphene.ID(required=True)
    hotel = graphene.Field(hotelForAdmin, required=True)
    type = graphene.NonNull(PaymentEnum)
    receipts = graphene.List(graphene.NonNull(PaymentJumpFinanceType), required=True)
    can_delete = graphene.Boolean(required=True, description="Флаг на удаление")

    sum_for_pay_with_tax = graphene.Float(required=True, description="Сумма на оплату")
    sum_paid = graphene.Float(required=True, description="Сумма оплаченная")
    count_sent_receipts = graphene.Int(required=True, description="Количество отправленных чеков в JumpFinance")
    tasks_id = graphene.List(graphene.NonNull(graphene.ID), required=True, description="Список id Заявок")

    def resolve_id(self, info):
        return self.pk

    def resolve_hotel(self, info):
        return self.tasks.first().manager.hotel

    def resolve_receipts(self, info):
        return self.paymentjumpfinance_set.all()

    def resolve_can_delete(self, info):
        return self.can_delete

    def resolve_sum_for_pay_with_tax(self, info):
        return sum(self.paymentjumpfinance_set.values_list("amount", flat=True))

    def resolve_sum_paid(self, info):
        return sum(self.paymentjumpfinance_set.exclude(amount_paid=None).values_list("amount_paid", flat=True))

    def resolve_count_sent_receipts(self, info):
        return self.paymentjumpfinance_set.exclude(status=PaymentJumpFinance.STATUSES[0][0]).count()

    def resolve_tasks_id(self, info):
        return list(self.tasks.all().values_list("id", flat=True))
