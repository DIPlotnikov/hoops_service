import json
import random
import uuid
from datetime import datetime, timedelta
from enum import Enum
from random import randint

import jwt
from closing_documents.models import ClosingDocument
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from graphene import Enum as GEnum
from settings.models import get_remuneration

from .tasks import send_push
from .utils.invoice import round_value_for_hoops

if not settings.DEV:
    from django.contrib.auth.base_user import BaseUserManager

    class UserManager(BaseUserManager):
        """
        Кастомный класс менеджера пользователей
        """

        def create_user(self, email, password=None, **kwargs):
            """Создает и возвращает пользователя с email, паролем и именем."""

            print(kwargs)
            if email is None:
                raise TypeError("Users must have an email address.")

            user = self.model(email=self.normalize_email(email))
            user.set_password(password)
            user.save()

            return user

        def create_superuser(self, email, password, **kwargs):
            """Создает и возвращает пользователя с привилегиями супер админа."""
            if password is None:
                raise TypeError("Superusers must have a password.")

            user = self.create_user(email, password, **kwargs)

            user.save()

            return user

    class User(AbstractBaseUser, PermissionsMixin):
        email = models.EmailField(db_index=True, unique=True, default="")

        USERNAME_FIELD = "email"
        REQUIRED_FIELDS = []
        is_staff = models.BooleanField(default=True)
        objects = UserManager()

        def __str__(self):
            """Строковое представление модели (отображается в консоли)"""
            return self.email

else:
    from .schemas.notification.subscription import MySubscription


class BaseEmojiField:

    def is_ascii(self, s):
        return all(ord(c) < 128 for c in s)

    def to_python(self, value):
        if isinstance(value, str) or value is None:
            if value is None:
                return value
            else:
                encoded_string = str(value).encode("unicode_escape")
                return encoded_string
        return str(value)

    def from_db_value(self, value, *args, **kwargs):
        if str(value).startswith("b'"):
            value = bytes(str(value).replace("b'", "")[0:-1].replace("\\\\", "\\"), "utf-8").decode("unicode_escape")
        elif self.is_ascii(str(value)):
            value = bytes(str(value), "utf-8").decode("unicode_escape")
            return value
        return value


class CustomEmojiCharField(BaseEmojiField, models.CharField):
    pass


class CustomEmojiTextField(BaseEmojiField, models.TextField):
    pass


class Token(models.Model):
    """
    Код выпуска токена
    """

    def expired_at_datetime(self, delta=30):
        return timezone.now() + timedelta(days=delta)

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    expired_at = models.DateTimeField(default=expired_at_datetime)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class PhoneCode(models.Model):
    """
    Код для подтверждения
    """

    phonenumber = models.CharField(max_length=11, default="", unique=True)
    code = models.IntegerField(default=0)
    count = models.IntegerField(default=0)
    is_valid = models.BooleanField(default=False)

    def new_code(self):
        assert self.count < 50, "Отправка кода не возможна, обратитесь в поддержку!"
        if settings.DEBUG is True:
            new_code = 1111
        else:
            new_code = randint(1000, 9999)
        self.code = new_code
        self.count += 1
        self.save()


class Coordinates(models.Model):
    """
    Модель координат
    """

    zoom = models.IntegerField(default=0, help_text="Зум")
    latitude = models.FloatField(default=0.0, help_text="Долгота")
    longitude = models.FloatField(default=0.0, help_text="Широта")
    address = models.CharField(max_length=255, default="", help_text="Адрес (255 символов)")
    label = models.CharField(max_length=255, default="", help_text="Label (255 символов)")

    def __str__(self):
        return f"Координаты №{self.pk}"

    class Meta:
        verbose_name = "Координаты"
        verbose_name_plural = "Координаты"


class Address(models.Model):
    """
    Модель адреса
    """

    # executer = models.CharField(max_length=255, null=False, default='')
    zoom = models.IntegerField(default=0, help_text="Зум")
    latitude = models.FloatField(default=0.0, help_text="Долгота")
    longitude = models.FloatField(default=0.0, help_text="Широта")
    address = models.CharField(max_length=255, default="", help_text="Адрес (255 символов)")
    # postalCode = models.IntegerField(default=0, help_text='Индекс почтовый')
    label = models.CharField(max_length=255, default="", help_text="Label (255 символов)")

    def __str__(self):
        return f"Адрес №{self.id} исполнителя {self.address}"

    class Meta:
        verbose_name = "Адрес исполнителя"
        verbose_name_plural = "Адреса исполнителей"


class Profession(models.Model):
    """
    Профессия
    """

    okei = {"HOUR": {"code": "356", "num": "ч"}, "SUIT": {"code": "902", "num": "н"}}

    class Numerates(models.TextChoices):
        HOUR = "HOUR", _("Час")
        SUIT = "SUIT", _("Номер")

    NumeratesEnum = GEnum.from_enum(Numerates, description="Тип счисления")

    name = models.CharField(max_length=200, verbose_name="Наименование услуги", help_text="Наименование")
    description = models.CharField(
        max_length=200,
        null=False,
        blank=True,
        default="",
        verbose_name="Описание услуг",
        help_text="мыть,носить и тд...",
    )
    rate_max = models.IntegerField(
        default=0, verbose_name="Максимальная ставка", help_text="Максимальная ставка тарифа"
    )
    rate_min = models.IntegerField(default=0, verbose_name="Минимальная ставка", help_text="Минимальная ставка тарифа")
    rate_step = models.IntegerField(default=0, verbose_name="Шаг ставки", help_text="Шаг ставки тарифа")
    percent = models.IntegerField(
        default=0, null=False, verbose_name="Процент", help_text="получает HOOPS в процентах"
    )

    numerate = models.CharField(
        max_length=5,
        choices=Numerates.choices,
        default=Numerates.HOUR,
        verbose_name="Система Счислений",
        help_text="Код ОКЕИ в другом месте",
    )

    # multiplier = models.IntegerField(default=100, null=False, verbose_name='Множитель',
    #                                  help_text='Ставка * (1 - коэффициент / 100) - получает HOOPS')
    @property
    def volume(self):
        """
        Флаг возможности указать Объем выполненных работ
        """
        return self.numerate != self.Numerates.HOUR

    @property
    def multiplier(self):
        return 100 - self.percent

    def save(self, *args, **kwargs):
        assert self.rate_min < self.rate_max, "Минимальная ставка должна быть меньше максимальной"
        super(Profession, self).save(*args, **kwargs)

    def calculate_rate(self, cost: int, calculate_cost_for_executer: bool) -> float:
        """
        Получение расчёта стоимости для Исполнителя или для Гостиницы
        """
        # стоимость от которой отталкиваемся
        cost = cost
        # множитель профессии
        multiplier = self.multiplier
        # если надо рассчитать сколько получит Исполнитель если гостиница заплатит cost
        if calculate_cost_for_executer:
            # Исполнитель получит cost на множитель профессии
            res = cost * multiplier / 100
        # рассчитать сколько должна заплатить гостиница при выплате Исполнителю cost
        else:
            # cost = выплата Исполнителю, поэтому она делится на множитель и *100 и получаем полную выплату Гостиницей
            res = cost / multiplier * 100
        return round(res, 2)

    def __str__(self):
        return f"Профессия №{self.id} {self.name}"

    class Meta:
        verbose_name = "Профессия"
        verbose_name_plural = "Профессии"


class FileInfo(models.Model):
    """
    Модель загружаемого файла
    """

    fileName = models.CharField(null=False, default="", max_length=255)
    fileSize = models.IntegerField(null=False, default=0)
    height = models.IntegerField(null=False, default=0)
    width = models.IntegerField(null=False, default=0)
    mimeType = models.CharField(null=False, default="", max_length=255)
    timeStamp = models.CharField(null=False, default="", max_length=255)
    url = models.CharField(unique=True, default="", max_length=255)

    def __str__(self):
        return self.url

    class Meta:
        verbose_name = "Информация о файле"
        verbose_name_plural = "Информация о файле"


class Hotel(models.Model):
    """
    Гостиница
    """

    class Statuses(models.TextChoices):
        STEP_1_REGISTERED = "STEP_1_REGISTERED", _("Зарегистрирован")
        STEP_2_WAITING_FOR_VERIFICATION = "STEP_2_WAITING_FOR_VERIFICATION", _("Ожидает подтверждения")
        STEP_3_VERIFIED = "STEP_3_VERIFIED", _("Подтвержден")
        STEP_3_VERIFICATION_DECLINED = "STEP_3_VERIFICATION_DECLINED", _("Отклонен")

    StatusesEnum = GEnum.from_enum(Statuses, description="Статусы Гостиниц")

    class PaymentPeriodToHoops(models.TextChoices):
        ONCE_A_MONTH = "ONCE_A_MONTH", _("Один раз в месяц")
        TWICE_A_MONTH = "TWICE_A_MONTH", _("Два раза в месяц")

    PaymentPeriodToHoopsEnum = GEnum.from_enum(PaymentPeriodToHoops, description="Период оплаты Гостиниц")

    class PaymentPeriodToExecutor(models.TextChoices):
        ONCE_A_WEEK = "ONCE_A_WEEK", _("Один раз в неделю")
        TWICE_A_MONTH = "TWICE_A_MONTH", _("Два раза в месяц")

    PaymentPeriodToExecutorEnum = GEnum.from_enum(PaymentPeriodToExecutor, description="Период выплат Исполнителям")

    email = models.EmailField(db_index=True, default="", verbose_name="Email гостиницы", help_text="Email гостиницы")
    inn = models.BigIntegerField(
        db_index=True, unique=True, verbose_name="ИНН", help_text="ИНН для входа главного Менеджера"
    )
    postalAddress = models.CharField(
        max_length=50, default="", blank=True, verbose_name="Почтовый адрес", help_text="почтовый адрес"
    )
    nameLegalEntity = models.CharField(
        max_length=50,
        default="",
        blank=True,
        verbose_name="Юридическое наименование",
        help_text="Юридическое наименование",
    )
    nameHotel = models.CharField(
        max_length=255,
        default="",
        blank=True,
        verbose_name="Наименование гостиницы",
        help_text="Наименование гостиницы",
    )
    undergroundStation = models.CharField(
        max_length=50, default=None, null=True, blank=True, verbose_name="Станция метро", help_text="Станция метро"
    )
    phone_number = models.CharField(max_length=13, verbose_name="Контактный номер", help_text="Контактный номер")
    profile_pic = models.OneToOneField(
        FileInfo,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Фото профиля",
        help_text="Фото профиля",
    )
    logo = models.OneToOneField(
        "Logo", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Логотип", help_text="Логотип"
    )
    coordinates = models.OneToOneField(
        Coordinates,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="hotel_fact_address",
        verbose_name="Координаты",
        help_text="Координаты",
    )
    status = models.CharField(
        max_length=31,
        choices=Statuses.choices,
        default=Statuses.STEP_1_REGISTERED,
        verbose_name="Статус Гостиницы",
        help_text="Статус Гостинце",
    )

    auto_approve_tasks = models.BooleanField(
        default=True, verbose_name="Авто подтверждение", help_text="Флаг указатель на авто подтверждение заявок"
    )
    is_allow_to_use_basic_profession = models.BooleanField(
        default=True,
        verbose_name="Базовые профессии в заявках",
        help_text="Флаг указатель на использование менеджерами базовых профессий в заявках",
    )
    is_active = models.BooleanField(
        default=True, verbose_name="Активный профиль", help_text="Флаг, что профиль не удален"
    )
    is_verify = models.BooleanField(default=False, verbose_name="Признак верификации", help_text="Признак верификации")
    is_test = models.BooleanField(
        default=False, help_text="Признак тестового аккаунта", verbose_name="Тестовый аккаунт"
    )
    fcm_token = models.CharField(default=None, null=True, blank=True, max_length=255)
    max_count_of_personal_profession = models.IntegerField(
        default=10,
        null=False,
        verbose_name="Максимальное количество персональных профессий",
        help_text="Максимальное количество персональных профессий",
    )

    payment_period_to_hoops = models.CharField(
        max_length=13,
        choices=PaymentPeriodToHoops.choices,
        default=PaymentPeriodToHoops.TWICE_A_MONTH,
        verbose_name="Период оплат Гостиниц",
        help_text="Период оплат Гостиниц",
    )

    payment_period_to_executor = models.CharField(
        max_length=13,
        choices=PaymentPeriodToExecutor.choices,
        default=PaymentPeriodToExecutor.ONCE_A_WEEK,
        verbose_name="Период выплат Исполнителям",
        help_text="Период выплат Исполнителям",
    )

    may_use_additional_in_tasks = models.BooleanField(
        default=False,
        verbose_name="Использовать дополнительные профессии в Заявках",
        help_text="Использовать дополнительные профессий в Заявках",
    )

    accepted_at = models.DateTimeField(
        default=None, null=True, blank=True, verbose_name="Дата подтверждения", help_text="Подтверждение платежа"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def payment_period_to_hoops_ru(self):
        return str(self.PaymentPeriodToHoops(self.payment_period_to_hoops).label)

    @property
    def payment_period_to_executor_ru(self):
        return str(self.PaymentPeriodToExecutor(self.payment_period_to_executor).label)

    @property
    def get_admin(self):
        return self.manager_set.filter(is_admin=True).first()

    def go_to_start(self):
        """
        Скинуть статус Гостинице
        """
        # скидываем статус гостинице
        self.status = self.Statuses.STEP_1_REGISTERED
        # сохраняем
        self.save()

    def accept(self, accepted_at: datetime = None):
        assert self.status != "STEP_1_REGISTERED", "заказчик отозвал проверку реквизитов"
        self.status = "STEP_3_VERIFIED"
        self.accepted_at = accepted_at or timezone.now()
        self.save()

    def __str__(self):
        return f"Гостиница №{self.id} {self.nameHotel}"

    class Meta:
        verbose_name = "Гостиница"
        verbose_name_plural = "Гостиницы"
        unique_together = ("email", "inn")


class StatusExecuter(Enum):
    STEP_1_REGISTERED = "STEP_1_REGISTERED"
    STEP_2_WAITING_FOR_VERIFICATION = "STEP_2_WAITING_FOR_VERIFICATION"
    STEP_3_VERIFIED = "STEP_3_VERIFIED"
    STEP_3_VERIFICATION_DECLINED = "STEP_3_VERIFICATION_DECLINED"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)


StatusExecuterEnum = GEnum.from_enum(StatusExecuter)


class GenderExecuter(Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)


Genders = GEnum.from_enum(GenderExecuter)


class Executer(AbstractBaseUser):
    """
    Исполнитель
    """

    USERNAME_FIELD = "phone_number"

    GENDERS = (
        ("MALE", "Мужской"),
        ("FEMALE", "Женский"),
    )
    STATUSES = (
        ("STEP_1_REGISTERED", "Зарегистрирован"),
        ("STEP_2_WAITING_FOR_VERIFICATION", "Отправил запрос на подтверждение"),
        ("STEP_3_VERIFIED", "Подтвержден"),
        ("STEP_3_VERIFICATION_DECLINED", "Отказ в подтверждении"),
    )

    TYPES = (
        ("unknown", "не установлен"),
        ("IP", "ИП"),
        ("self-e", "самозанятый"),
    )

    profile_pic = models.OneToOneField(
        FileInfo, on_delete=models.SET_NULL, null=True, verbose_name="Аватарка", blank=True, help_text="Аватарка"
    )
    first_name = models.CharField(max_length=100, default="", blank=True, verbose_name="Имя", help_text="Имя")
    second_name = models.CharField(
        max_length=100, default="", blank=True, null=True, verbose_name="Отчество", help_text="Отчество"
    )
    middle_name = models.CharField(max_length=100, default="", blank=True, verbose_name="Фамилия", help_text="Фамилия")
    birthday = models.DateField(
        verbose_name="Дата рождения", help_text="Дата рождения", null=False, default=timezone.now
    )
    gender = models.CharField(
        choices=GENDERS, max_length=20, default=GENDERS[0][0], verbose_name="Пол", help_text="Пол"
    )
    work_expiration = models.DateTimeField(
        null=True, default=None, blank=True, verbose_name="Разрешение на работу", help_text="Разрешение на работу"
    )
    medical_book_expiration = models.DateTimeField(
        null=True, default=None, blank=True, verbose_name="Медицинская книжка", help_text="Медицинская книжка"
    )
    phone_number = models.CharField(max_length=13, verbose_name="Номер телефона", help_text="Номер телефона без 7")
    email = models.EmailField(default="", verbose_name="e-mail", help_text="e-mail")
    status = models.CharField(
        choices=STATUSES, max_length=31, default=STATUSES[0][0], verbose_name="Статус", help_text="Статус"
    )
    professions = models.ManyToManyField(Profession, verbose_name="Профессии", blank=True, help_text="Профессии")
    kind = models.CharField(
        choices=TYPES, max_length=20, default=TYPES[0][0], verbose_name="Тип юридический", help_text="Тип юридический"
    )
    favourites_hotel = models.ManyToManyField(
        Hotel, blank=True, verbose_name="Список избранных Гостиниц", help_text="Список избранных Гостиниц"
    )

    other = models.TextField(max_length=100, default="Описание", verbose_name="", blank=True, help_text="Описание")
    about = models.CharField(
        max_length=255, default="", blank=True, help_text="Описание исполнителя", verbose_name="Описание исполнителя"
    )

    score = models.IntegerField(
        default=0, help_text="Рейтинг пользователя в баллах", verbose_name="Рейтинг пользователя в баллах"
    )
    count_work_with_rating = models.IntegerField(
        default=0, help_text="Количество работ с оценками", verbose_name="Количество работ с оценками"
    )

    is_valid_number = models.BooleanField(
        default=False, verbose_name="Флаг на проверку номера", help_text="Флаг на проверку номера"
    )
    is_active = models.BooleanField(
        default=True, help_text="Булевый указатель на живой аккаунт", verbose_name="Живой аккаунт"
    )
    is_test = models.BooleanField(
        default=False, help_text="Булевый указатель на тестовый аккаунт", verbose_name="Тестовый аккаунт"
    )
    agreement_datetime = models.DateField(
        null=True, blank=True, verbose_name="Дата договора", help_text="Дата договора"
    )
    update_password_at = models.DateTimeField(
        null=True, blank=True, help_text="Дата и время последней смены пароля", verbose_name="Последняя смена пароля"
    )
    created_at = models.DateTimeField(auto_now_add=True, help_text="Дата создания", verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, help_text="Дата обновления", verbose_name="Дата обновления")

    def check_tasks_by_task(self, task):

        # проверка рядом стоящих принятых заявок
        other_tasks = Task.objects.filter(
            start_at__range=(
                task.start_at - timedelta(hours=26),
                (task.start_at + timedelta(hours=(task.duration + 3))),
            ),
            executers__executer__id=self.id,
        ).exclude(status="DELETED")
        for other_task in other_tasks:
            if (
                (other_task.start_at - timedelta(hours=3)).timestamp()
                < task.start_at.timestamp()
                < (other_task.start_at + timedelta(hours=(other_task.duration + 3))).timestamp()
            ):
                raise ValueError(f"Данная дата занята заявкой # {other_task.id}")
            # # до начала заявки должно быть 3 часа от окончания другой
            if (
                (other_task.start_at - timedelta(hours=3)).timestamp()
                < (task.start_at + timedelta(hours=task.duration)).timestamp()
                < (other_task.start_at + timedelta(hours=(other_task.duration + 3))).timestamp()
            ):
                raise ValueError(f"Данная дата занята заявкой # {other_task.id}")
        # окончание проверки рядом стоящих заявок

        return True

    @property
    def count_day_for_last_task(self):
        last_executer_state = (
            self.executerstate_set.prefetch_related("task_set").filter(task__start_at__lte=timezone.now()).last()
        )
        if last_executer_state:
            return (timezone.now() - last_executer_state.task.start_at).days

    @property
    def count_day_for_end_registration(self):
        """
        Количество дней до окончания регистрации Исполнителя
        :return: количество дней
        """
        return (self.work_expiration - timezone.now()).days if self.work_expiration else None

    @property
    def count_day_for_end_medical_book(self):
        """
        Количество дней до окончания медицинской книжки Исполнителя
        :return: количество дней
        """
        return (self.medical_book_expiration - timezone.now()).days if self.medical_book_expiration else None

    @property
    def validate(self):
        """
        Валидация аккаунта - может ли посещать сайт
        :return: None
        """
        assert self.is_active is True, "Удаленный аккаунт"
        return True

    @property
    def request_create_payment(self):
        self.raise_if_verified()
        # проверка аватара
        assert self.profile_pic is not None, "Необходимо разместить фотографию профиля"
        # проверка реквизитов
        assert self.simplerequisite is not None, "Не заполнены реквизиты для оплат!"
        # проверка медицинской книжки
        assert self.medical_book_expiration > timezone.now(), "Срок действия медицинской книжки истёк"
        return True

    @property
    def phone_number_international_format(self):
        return f"+7{self.phone_number}"

    @property
    def inn(self):
        if hasattr(self, "simplerequisite"):
            return self.simplerequisite.inn.zfill(12)
        return "ИНН отсутствует"

    def break_status(self):
        if self.status in ["STEP_3_VERIFIED", "STEP_3_VERIFICATION_DECLINED"]:
            self.to_wait_verify()

    def to_wait_verify(self):
        self.status = "STEP_2_WAITING_FOR_VERIFICATION"
        self.save()
        notification = Notification(
            type=Notification.TypeNotification.ACCOUNT,
            id_instance=self.pk,
            role="executer",
            read=False,
            text="Ваш аккаунт деактивирован",
        )
        notification.save(notification=True)

    @property
    def is_verified(self):
        return self.status == "STEP_3_VERIFIED"

    def raise_if_verified(self):
        assert self.is_verified is not True, "Ваш аккаунт уже подтвержден"

    @property
    def full_name(self):
        return f"{self.middle_name} {self.first_name} {self.second_name}"

    @property
    def can_work(self):
        if self.work_expiration:
            assert self.work_expiration > timezone.now(), "Истек срок временной регистрации"

        if self.medical_book_expiration:
            assert self.medical_book_expiration > timezone.now(), "Истек срок действия медицинской книжки"

        if self.status:
            assert self.status == "STEP_3_VERIFIED", "Ваш статус не позволяет продолжить действие"
        return True

    @property
    def token_notification_array(self):
        return self.fcmtoken_set.all().values_list("token", flat=True)

    @property
    def rating(self):
        if bool(self.count_work_with_rating):
            return round(self.score / self.count_work_with_rating, 2)
        else:
            return 5.0

    @property
    def token(self):
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        """
        У исполнителя другой токен
        """
        # жизнь токена
        # dt = datetime.now() + timedelta(days=60)

        token = jwt.encode(
            {"type": type(self).__name__, "id": self.pk, "role": 2, "inn": self.inn},
            settings.SECRET_KEY,
            algorithm="HS256",
        )

        return token

    def token_for_admin(self, read: bool = False) -> str:
        """
        Получение токена для Администратора
        :param read: Флаг-разрешение на только чтение
        :return: Токен доступа для Администратора с временем на 15 минут и проверкой на чтение/запись
        """
        # формирование временной метки жизни токена
        dt = int((datetime.now() + timedelta(minutes=15)).timestamp())
        # возвращаем токен
        return self._generate_jwt_token_exp(dt, read)

    def _generate_jwt_token_exp(self, dt: int, read: bool = False):
        """
        Генерация токена с указанием прав и времени жизни
        :param dt: Метка жизни токена
        :param read: Флаг-разрешение на только чтение
        :return: Токен доступа с параметрами
        """
        token = jwt.encode(
            {"role": 2, "type": type(self).__name__, "id": self.pk, "inn": self.inn, "exp": dt, "read": read},
            settings.SECRET_KEY,
            algorithm="HS256",
        )

        return token

    @staticmethod
    def get_technical_account():
        e = Executer.objects.filter(id=177).first()
        return e.id if e else None

    def save(self, *args, **kwargs):
        # orig = self.__class__.objects.filter(id=self.id).first()
        # if orig and orig.password != self.password:
        #     self.set_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{'✅' if self.is_active else '❌'} {self.id} {self.full_name} | {self.phone_number[-4:]}"

    class Meta:
        verbose_name = "Исполнитель"
        verbose_name_plural = "Исполнители"
        unique_together = ("phone_number", "is_active", "created_at")
        ordering = ["-id"]


class ExecuterFiles(models.Model):
    """
    Файл исполнителя
    """

    CHOICES = (
        ("MEDICAL_BOOK", "MEDICAL_BOOK"),
        ("REGISTRATION", "REGISTRATION"),
    )

    file = models.ForeignKey(FileInfo, on_delete=models.CASCADE, help_text="Файл исполнителя", null=True, blank=True)
    executer = models.ForeignKey(Executer, on_delete=models.CASCADE, help_text="Исполнитель", null=True, blank=True)
    type = models.CharField(choices=CHOICES, max_length=12, default=CHOICES[0][0], help_text="Тип файла")

    def __str__(self):
        return f"Файл исполнителя {self.executer} №{self.id}"

    class Meta:
        verbose_name = "Файл исполнителя"
        verbose_name_plural = "Файлы исполнителя"


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return "users/user_{0}/{1}".format(instance.user.id, filename)


class Requisites(models.Model):
    """
    Реквизиты банковские
    """

    owner = models.OneToOneField(
        Hotel, on_delete=models.CASCADE, verbose_name="указатель гостиницы", null=True, blank=True
    )
    executer = models.OneToOneField(
        Executer, on_delete=models.CASCADE, verbose_name="указатель исполнителя", null=True, blank=True
    )
    paymentBill = models.CharField(default="0", max_length=20, verbose_name="расчетный счет")
    correctBill = models.CharField(default=None, max_length=20, verbose_name="коррекционный счет", null=True)
    kpp = models.CharField(max_length=9, verbose_name="КПП", null=True, blank=True)
    innBank = models.CharField(default="0", max_length=12, verbose_name="ИНН банка")
    bik = models.CharField(default="0", max_length=9, verbose_name="БИК")
    name = models.CharField(max_length=255, default="", verbose_name="наименование банка")
    ogrn = models.CharField(max_length=15, verbose_name="ОГРН", null=True, blank=True)
    legal_address = models.CharField(
        max_length=1000, null=False, default="Не заполнено", blank=True, help_text="Юридический адрес"
    )
    signer = models.CharField(max_length=255, default="", verbose_name="Подписант", help_text="Имя подписанта")

    REQUIRED_FIELDS = ["paymentBill", "BIK"]

    def __str__(self):
        return f"Реквизиты №{self.pk} {str(self.owner) if self.owner else str(self.executer)}"

    class Meta:
        verbose_name = "Реквизиты Гостиницы"
        verbose_name_plural = "Реквизиты Гостиниц"


class SimpleRequisite(models.Model):
    """
    Реквизиты исполнителя
    """

    executer = models.OneToOneField(
        Executer,
        on_delete=models.CASCADE,
        verbose_name="Указатель исполнителя",
        null=True,
        help_text="Реквизиты Исполнителя",
        blank=True,
    )
    inn = models.CharField(max_length=12, default=None, verbose_name="ИНН")
    card_number = models.CharField(max_length=20, default=None, null=True, verbose_name="Номер банковской карты")
    bank_name = models.CharField(max_length=255, default=None, null=True, verbose_name="Наименование банка")

    def __str__(self):
        return f"{self.executer} простой реквизит"

    class Meta:
        verbose_name = "Реквизиты Исполнителя"
        verbose_name_plural = "Реквизиты Исполнителей"


class Manager(AbstractBaseUser):
    """
    Менеджер
    """

    class Meta:
        verbose_name = "Менеджер"
        verbose_name_plural = "Менеджеры"
        unique_together = ("email", "hotel")

    class Status(Enum):
        SEND_INVITE = "SEND_INVITE"
        CANCEL_INVITE = "CANCEL_INVITE"
        INVITED = "INVITED"
        ADMIN = "ADMIN"

        @classmethod
        def choices(cls):
            return tuple((i.name, i.value) for i in cls)

    StatusEnum = GEnum.from_enum(Status)

    USERNAME_FIELD = "email"
    CHOICES = ((0, "send invite"), (1, "cancel invate"), (2, "invited"), (3, "Администоратор гостиницы"))

    email = models.EmailField(default="", help_text="E-mail заказчика", verbose_name="Email")
    first_name = models.CharField(max_length=100, default="", verbose_name="Имя", blank=True)
    second_name = models.CharField(max_length=100, default="", verbose_name="Отчество", blank=True)
    middle_name = models.CharField(max_length=100, default="", verbose_name="Фамилия", blank=True)
    hotel = models.ForeignKey(
        Hotel,
        on_delete=models.CASCADE,
        help_text="Гостиница, с которой связан менеджер",
        verbose_name="Гостиница",
        null=True,
        blank=True,
        db_index=True,
    )
    is_admin = models.BooleanField(
        default=False, help_text="Булевый указатель на администратора гостиницы", verbose_name="Главный"
    )
    is_active = models.BooleanField(
        default=True, help_text="Булевый указатель на работоспособность записи", verbose_name="Живой"
    )
    status = models.IntegerField(
        choices=CHOICES, default="0", help_text="Статус профиля менеджера", verbose_name="Статус"
    )
    update_password_at = models.DateTimeField(
        null=True, help_text="Дата и время последней смены пароля", verbose_name="Смена пароля", blank=True
    )
    favourite_executers = models.ManyToManyField(
        "Executer", help_text="Избранные исполнители", blank=True, verbose_name="Исполнители"
    )

    admin = models.ForeignKey(
        "Admin",
        on_delete=models.SET_NULL,
        verbose_name="Координатор",
        null=True,
        help_text="Ответственный администратор",
        related_name="managers",
    )

    @property
    def validate(self):
        """
        Валидация аккаунта - может ли посещать сайт
        :return: None
        """
        assert self.is_active is True, "Удаленный аккаунт"
        assert self.status in [2, 3], "Не активированный профиль"
        return True

    def __str__(self):
        return (
            f"{self.id} {self.middle_name} {self.first_name} {self.second_name} "
            f"гостиницы {self.hotel} {'главный' if self.is_admin else ''} "
        )

    def save(self, *args, **kwargs):
        if self.id is None:
            super(Manager, self).save(*args, **kwargs)
        tech_executer = Executer.get_technical_account()
        if tech_executer not in self.favourite_executers.all().values_list("id", flat=True):
            self.favourite_executers.add(tech_executer)
        orig = self.__class__.objects.filter(id=self.id).first()
        if orig and orig.password != self.password:
            pass
            # self.set_password(self.password)
        if orig and orig.email != self.email and self.is_admin:
            hotel = self.hotel
            hotel.email = self.email
            hotel.save()
        super(Manager, self).save(*args, **kwargs)

    @property
    def fullname(self):
        return f"{self.middle_name} {self.first_name} {self.second_name}"

    @property
    def token(self):
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        """
        У менеджера другой токен
        """
        # жизнь токена
        # dt = datetime.now() + timedelta(days=60)

        token = jwt.encode(
            {
                "role": 1,
                "type": type(self).__name__,
                "id": self.pk,
                "hotels": self.hotel.id,
                "admin": self.is_admin,
            },
            settings.SECRET_KEY,
            algorithm="HS256",
        )

        return token

    def token_for_admin(self, read: bool = False) -> str:
        """
        Получение токена для Администратора
        :param read: Флаг-разрешение на только чтение
        :return: Токен доступа для Администратора с временем на 15 минут и проверкой на чтение/запись
        """
        # формирование временной метки жизни токена
        dt = int((datetime.now() + timedelta(minutes=15)).timestamp())
        # возвращаем токен
        return self._generate_jwt_token_exp(dt, read)

    def _generate_jwt_token_exp(self, dt: int, read: bool = False):
        """
        Генерация токена с указанием прав и времени жизни
        :param dt: Метка жизни токена
        :param read: Флаг-разрешение на только чтение
        :return: Токен доступа с параметрами
        """
        # жизнь токена
        # dt = int((datetime.now() + timedelta(minutes=10, hours = 3)).timestamp())
        # print(dt)
        token = jwt.encode(
            {
                "role": 1,
                "type": type(self).__name__,
                "id": self.pk,
                "hotels": self.hotel.id,
                "admin": self.is_admin,
                "exp": dt,
                "read": read,
            },
            settings.SECRET_KEY,
            algorithm="HS256",
        )

        return token

    @property
    def metka(self):
        return self._generate_metka()

    def _generate_metka(self):
        temp_string = TempString.objects.filter(first_field=self.email)
        if temp_string is not None:
            temp_string.delete()
        temp_string = TempString(first_field=self.email, second_field=str(random.randint(1000000, 9999999)))
        temp_string.save()
        return temp_string.second_field

    def filter_for_mutation_task(self, role):
        if role in self.roles.values_list("role", flat=True):
            return Q(manager__hotel__manager=self)
        else:
            return Q(manager=self)

    def filter_for_query_task(self, role):
        if role in self.roles.values_list("role", flat=True):
            return Q(manager__hotel=self.hotel)
        else:
            return Q(manager=self)

    def filter_for_query_executor_states(self, role):
        if role in self.roles.values_list("role", flat=True):
            return Q(task__manager__hotel=self.hotel)
        else:
            return Q(task__manager=self)


class Request(models.Model):
    pass


class Status(models.Model):
    # name = models.CharField(default='', max_length='50', null=False)
    pass


class PersonalProfession(models.Model):
    """
    Эксклюзивная профессия
    """

    name = models.CharField(
        default="",
        max_length=200,
        null=False,
        help_text="Наименование эксклюзивной профессии",
        verbose_name="Наименование",
    )
    owner = models.ForeignKey(
        Hotel,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="Идентификатор владельца аналоговой профессии",
        verbose_name="Указатель на гостиницу",
    )
    analog = models.ForeignKey(
        Profession,
        null=False,
        on_delete=models.CASCADE,
        help_text="Идентификатор аналоговой профессии",
        verbose_name="Указатель на основную профессию",
    )
    rent = models.FloatField(default=0, help_text="Ставка эксклюзивной профессии", verbose_name="Ставка")
    active = models.BooleanField(default=True, verbose_name="Флаг на существование")

    @property
    def without_tax(self):
        return (self.rent * (self.analog.multiplier / 100)) + (self.rent * (1 - (self.analog.multiplier / 100))) / 1.2

    @property
    def for_hoops(self):
        return self.rent * (self.analog.percent / 100)

    @property
    def for_hoops_without_tax(self):
        return self.for_hoops / 1.2

    def __str__(self):
        return f" №{self.id} {self.name} | {self.owner}"

    class Meta:
        verbose_name = "Эксклюзивная профессия"
        verbose_name_plural = "Эксклюзивные профессии"


class Admin(AbstractBaseUser):
    """
    Администратор HOOPS
    """

    class Permission(models.TextChoices):
        FULL_ACCESS = "FULL_ACCESS", _("Полный доступ")
        MANAGER = "MANAGER", _(
            "Полный доступ-Профессии-Выплаты-Документы-Администраторы-Отчеты-Мутации в профилях пользователей"
        )
        MANAGER_REPORT_USERS_PROFILE = "MANAGER_REPORT_USERS_PROFILE", _(
            "Менеджер админ + Отчеты + Мутации в чужих профилях"
        )
        NEWS = "NEWS", _("Только новости")

    PermissionEnum = GEnum.from_enum(Permission, description="Права Администратора")

    USERNAME_FIELD = "name"
    name = models.CharField(
        default="",
        max_length=100,
        unique=True,
        verbose_name="Имя администратора",
        help_text="100 символов максимум и уникальность",
    )
    is_active = models.BooleanField(default=True, verbose_name="Активный", help_text="Флаг указатель на активность")
    permissions = models.CharField(
        max_length=28,
        choices=Permission.choices,
        default=Permission.FULL_ACCESS,
        verbose_name="Права доступа",
        help_text="Права доступа",
    )

    role = models.CharField(
        default="", max_length=100, verbose_name="Роль администратора", help_text="Роль администратора"
    )

    surname = models.CharField(default="", max_length=100, verbose_name="Фамилия", help_text="Фамилия")
    first_name = models.CharField(default="", max_length=100, verbose_name="Имя администратора", help_text="Имя")
    middle_name = models.CharField(
        default="", max_length=100, verbose_name="Отчество администратора", help_text="Отчество"
    )

    percent = models.FloatField(
        default=0.0, verbose_name="Процент", help_text="Количество процентов, получаемых от продаж"
    )

    @property
    def full_name(self) -> str:
        """
        Полное имя Администратора
        :return: полное имя
        """
        return f"{self.surname} {self.first_name} {self.middle_name}"

    @property
    def validate(self):
        """
        Валидация аккаунта - может ли посещать сайт
        :return: None
        """
        assert self.is_active is True, "Удаленный аккаунт"
        return True

    def get_permission_for_only_read_in_other_profiles(self, user: str) -> bool:
        """
        Получение флага read для токена
        :return: True - когда разрешено только чтение, False - разрешены мутации
        """
        # из описания прав доступа - только FULL_ACCESS для изменений в чужих профилях
        roles = self.roleadmin_set.values_list("role", flat=True)
        map_ = {
            "EXECUTER": "EXECUTER_AUTH_EDIT",
            "MANAGER": "CUSTOMER_AUTH_EDIT",
        }
        user = getattr(user, "value", user)

        if map_.get(user.upper(), "----") in roles:
            return False
        # остальные не имеют права на мутации
        return True

    @staticmethod
    def get_main_admin():
        """
        Получение id главного админа
        :return: Идентификатор Администратора главного
        """
        return Admin.objects.get(id=1).id

    @property
    def token(self):
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        # dt = datetime.now() + timedelta(days=60)
        token = jwt.encode(
            {
                "type": type(self).__name__,
                "role": -1,
                "id": self.pk,
                "meta": {"permissions": self.permissions},
                "name": self.name,
                "exp": int((datetime.now() + timedelta(days=15)).timestamp()),
            },
            settings.SECRET_KEY,
            algorithm="HS256",
        )

        return token

    def __str__(self):
        return f"Админ {self.name} | {self.permissions}"

    class Meta:
        verbose_name = "Админ HOOPS"
        verbose_name_plural = "Админы HOOPS"


class RoleAdmin(models.Model):
    class Roles(models.TextChoices):
        SEO = "SEO", _("доступ к новостям, помощи, лендинг")
        REPORT = "REPORT", _("доступ к отчетам")
        REPORT_MONEY = "REPORT_MONEY", _("Доступ к денежному отчету")
        EXECUTER = "EXECUTER", _("доступ к исполнителям")
        EXECUTER_TEST = "EXECUTER_TEST", _("доступ к тестовым кнопкам у исполнителей")
        EXECUTER_VERIFICATION = "EXECUTER_VERIFICATION", _("доступ к верификационным кнопкам исполнителя")
        EXECUTER_AUTH = "EXECUTER_AUTH", _("доступ к авторизации исполнителя")
        EXECUTER_AUTH_EDIT = "EXECUTER_AUTH_EDIT", _("доступ к редактированию в авторизации исполнителя")
        CUSTOMER = "CUSTOMER", _("доступ к заказчикам")
        CUSTOMER_TEST = "CUSTOMER_TEST", _("доступ к тестовым кнопкам заказчика")
        CUSTOMER_AUTH = "CUSTOMER_AUTH", _("доступ к авторизации заказчика")
        CUSTOMER_AUTH_EDIT = "CUSTOMER_AUTH_EDIT", _("доступ к редактированию в авторизации заказчика")
        CUSTOMER_SET_ADMIN = "CUSTOMER_SET_ADMIN", _("установка админа менеджерам")
        TASK = "TASK", _("доступ к заявкам")
        TASK_ARCHIVE = "TASK_ARCHIVE", _("доступ архивации заявки")
        DOCUMENT = "DOCUMENT", _("доступ к документам")
        PAYMENTS = "PAYMENTS", _("доступ к выплатам")
        SETTINGS = "SETTINGS", _("доступ к настройкам")

    RolesEnum = GEnum.from_enum(Roles, description="Роли Администратора")
    role = models.CharField(
        max_length=28,
        choices=Roles.choices,
        default=Roles.SEO.value,
        verbose_name="Роли доступа",
        help_text="Роли доступа",
    )

    admin = models.ForeignKey(Admin, on_delete=models.CASCADE, null=False, help_text="Админ", verbose_name="Админ")

    created_at = models.DateTimeField(auto_now_add=True, help_text="Время создания")
    updated_at = models.DateTimeField(auto_now=True, help_text="Время последнего обновления")


class RoleManager(models.Model):
    """
    Роли доступа для Менеджера Гостиницы
    """

    class RolesManager(models.TextChoices):
        HOTEL = "HOTEL", _("доступ к профилю организации")
        HOTEL_EDIT = "HOTEL_UPDATE", _("доступ к профилю организации и его редактирование")
        TASK = "TASK", _("доступ к заявкам")
        TASK_ARCHIVE = "TASK_ARCHIVE", _("доступ к заявкам и их архивация")
        TASK_EDIT = "TASK_EDIT", _("доступ к заявкам и их архивация и модификация")
        FAVORITE = "FAVORITE", _("доступ к избранному")
        FAVORITE_EDIT = "FAVORITE_EDIT", _("доступ к избранному и редактирование")
        SETTINGS_EDIT = "SETTINGS_EDIT", _("доступ к настройкам и редактирование")
        DOCUMENTS = "DOCUMENTS", _("доступ к документам")
        REPORTS = "REPORTS", _("доступ к отчетам")

    RolesManagerEnum = GEnum.from_enum(RolesManager, description="Роли менеджера")
    role = models.CharField(
        max_length=28,
        choices=RolesManager.choices,
        default=RolesManager.HOTEL.value,
        verbose_name="Роли доступа",
        help_text="Роли доступа",
    )

    manager = models.ForeignKey(
        Manager,
        on_delete=models.CASCADE,
        related_name="roles",
        null=False,
        help_text="Менеджер",
        verbose_name="Менеджер",
    )

    created_at = models.DateTimeField(auto_now_add=True, help_text="Время создания")


class TempString(models.Model):
    first_field = models.CharField(default="", unique=True, max_length=100, db_index=True, null=False)
    second_field = models.CharField(default="", max_length=100, null=False)

    def __str__(self):
        return f"Строка для {self.first_field} "


class StatDoc(models.Model):
    """
    Отчет для менеджера
    """

    TYPES = (
        ("TABLE", "сводная таблица"),
        ("LIST_EXECUTERS", "список исполнителей"),
        ("STANDART_REPORT", "стандартный отчет"),
        ("BY_TYPE", "отчет по типам"),
        ("MANAGERS_REPORT", "отчет по менеджерам"),
        ("HISTORY_AND_FORECAST", "история и прогноз"),
        ("MANAGEMENT_REPORT", "управленческий отчет"),
        ("EXECUTORS_LIST", "список исполнителей"),
    )

    owner = models.ForeignKey(Manager, on_delete=models.CASCADE, null=True, blank=True)
    path = models.CharField(default="", unique=True, max_length=100, db_index=True, null=False)
    type = models.CharField(choices=TYPES, max_length=20, default=TYPES[0][0], help_text="Типы документов")
    date_update = models.DateTimeField(auto_now=True, help_text="Время последнего обновления")

    def __str__(self):
        return f"Файл статистики №{self.id} менеджера {self.owner}"

    class Meta:
        verbose_name = "Файл с отчетом менеджера"
        verbose_name_plural = "Файлы с отчетами менеджеров"


class ExecuterStatDoc(models.Model):
    """
    Отчет для исполнителя
    """

    TYPES = (
        ("STANDART_REPORT", "стандартный отчет"),
        ("BY_TYPE", "отчет по типам"),
        ("FINANCIAL", "сводный финансовый отчет"),
        ("DIFFERENCE_REPORT", "отчет по корректировкам"),
    )

    owner = models.ForeignKey(Executer, on_delete=models.CASCADE, null=True, blank=True)
    path = models.CharField(default="", unique=True, max_length=100, db_index=True, null=False)
    type = models.CharField(choices=TYPES, max_length=17, default=TYPES[0][0], help_text="Типы документов")
    date_update = models.DateTimeField(auto_now=True, help_text="Время последнего обновления")

    def __str__(self):
        return f"Файл статистики исполнителя №{self.id} {self.owner} "

    class Meta:
        verbose_name = "Файл с отчетом для исполнителя"
        verbose_name_plural = "Файлы с отчетами исполнителей"


class AdminStatDoc(models.Model):
    """
    Отчет для Администратора
    """

    class TypeAdminReport(models.TextChoices):
        STANDART = "STANDART", _("Стандартный")
        ACTIVITY = "ACTIVITY", _("Об активности")
        COMPARATIVE = "COMPARATIVE", _("Сравнительный отчет")
        PAYMENT_FOR_COORDINATORS = "PAYMENT_FOR_COORDINATORS", _("Выплаты координаторам")
        ADMIN_STATISTIC = "ADMIN_STATISTIC", _("Статистика администратору")
        EXECUTER_STANDART = "EXECUTER_STANDART", _("Стандартный отчет по исполнителю")

    TypeAdminReportEnum = GEnum.from_enum(TypeAdminReport)
    owner = models.ForeignKey(Admin, on_delete=models.CASCADE, null=True, blank=True)
    path = models.CharField(default="", unique=True, max_length=100, db_index=True, null=False)
    type = models.CharField(
        choices=TypeAdminReport.choices, max_length=24, default=TypeAdminReport.STANDART, help_text="Тип отчёта"
    )

    date_update = models.DateTimeField(auto_now=True, help_text="Время последнего обновления")

    def __str__(self):
        return f"Файл статистики №{self.id} для {self.owner}"

    class Meta:
        verbose_name = "Файл с отчетом администратора"
        verbose_name_plural = "Файлы с отчетами администратора"


class ExecuterState(models.Model):
    """
    Статус исполнителя в заявке
    """

    STATE = (
        ("REPLY", "откликнулся на заявку"),
        ("CONFIRMED", "подтвержден заказчиком"),
        ("START", "СТАРТ работы"),
        ("STOP", "СТОП работы"),
        ("CANCEL_BY_CUSTOMER", "отказ заказчиком"),
        ("CANCEL_YOURSELF", "отказ самостоятельный"),
    )

    PAYMENT_STATUSES = (
        (None, "нет статуста"),
        ("create_payment", "счет сформирован"),
        ("paid_payment", "счет оплачен"),
    )

    executer = models.ForeignKey(
        Executer, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Исполнитель", db_index=True
    )
    status = models.CharField(
        choices=STATE,
        max_length=40,
        default=STATE[0][0],
        help_text="Статус исполнителя относительно заявке",
        verbose_name="Статус",
    )
    start_at = models.DateTimeField(
        null=True, blank=True, verbose_name="Старт", help_text="Время старта работы", db_index=True
    )
    stop_at = models.DateTimeField(
        null=True, blank=True, verbose_name="Стоп", help_text="Время завершения работ", db_index=True
    )

    volume_of_the_work = models.FloatField(
        null=True, blank=True, verbose_name="Объем", help_text="Количество номеров или штук", db_index=True
    )
    correction_comment = models.CharField(
        null=True,
        max_length=100,
        default=None,
        verbose_name="Комментарий",
        help_text="Корректировка относительно Исполнителя",
        blank=True,
    )

    payment_status = models.CharField(
        choices=PAYMENT_STATUSES,
        max_length=40,
        default=None,
        null=True,
        blank=True,
        verbose_name="Статус оплаты",
        help_text="Статус оплаты заявки",
    )

    payment = models.ForeignKey(
        "Payment", on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Платеж", help_text="Платеж"
    )

    def set_volume(self, volume):
        assert self.can_set_volume is True, "Нельзя указать объем работ"
        assert self.volume_of_the_work is None, f"Объем работ уже указан ({self.volume_of_the_work})"
        self.volume_of_the_work = volume
        self.status = "STOP"
        self.save()

    def set_duration(self):
        if not all((self.start_at, self.stop_at)):
            return
        time_delta = self.stop_at - self.start_at
        self.duration_in_hours = round(time_delta.total_seconds() / 3600, 2)
        self.save()

    @property
    def can_set_volume(self):
        """
        Флаг возможности указать Объем работ
        """
        return self.task.profession.volume

    @property
    def task(self):
        """
        Получение Заявки
        """
        return self.task_set.last()

    @property
    def task_info(self):
        """
        Получение текстовой информации о Заявке
        """
        return f"{self.task.id} | {self.task.start_at.date()}" if self.task else ""

    @property
    def get_work_time(self):
        """
        Получение времени в работе в секундах (реальное - если есть старт и стоп или предполагаемое)
        """
        start_time = self.start_at_real_or_task
        end_time = self.stop_at_real_or_task
        absolute_time = abs((end_time - start_time).total_seconds())
        return absolute_time

    @property
    def get_work_time_real(self):
        """
        Получение времени в работе в секундах РЕАЛЬНОЕ
        """
        if self.start_at is None or self.stop_at is None:
            return 0
        return abs((self.stop_at - self.start_at).total_seconds())

    @property
    def get_work_time_in_hours_real(self):
        # FIXME
        return self.volume_of_the_work or round_value_for_hoops(self.get_work_time_real / 3600)

    @property
    def get_work_time_in_hours(self):
        # FIXME
        return self.volume_of_the_work or round_value_for_hoops(self.get_work_time / 3600)

    @property
    def is_check_in_finance(self):
        # FIXME учитывать в финансовых документах по объему
        return self.stop_at != self.start_at or bool(self.volume_of_the_work)

    @property
    def get_sum_full(self):
        return round(self.task.rent * (self.volume_of_the_work or self.get_work_time_in_hours), 2)

    @property
    def get_sum_for_pay(self):
        return round(self.get_sum_full * (self.task.profession.multiplier / 100), 2)

    @property
    def get_sum_for_hoops(self):
        return round(self.get_sum_full * (1 - (self.task.profession.multiplier / 100)), 2)

    @property
    def get_sum_for_hoops_for_remuneration(self):
        return round(self.get_sum_for_hoops / 100 * get_remuneration(), 2)

    @property
    def get_sum_for_hoops_without_remuneration(self):
        return round(self.get_sum_for_hoops - self.get_sum_for_hoops_for_remuneration, 2)

    @property
    def stop_at_real_or_task(self):
        if self.task:
            return self.stop_at if self.stop_at is not None else self.task.stop_at
        else:
            return 0

    @property
    def start_at_real_or_task(self):
        if self.task:
            return self.start_at if self.start_at is not None else self.task.start_at
        else:
            return 0

    @property
    def problem(self):
        # FIXME что писать в отчеты
        if self.volume_of_the_work:
            return self.correction_comment
        problem0 = "Не согласована" if self.task.is_approved is False else None
        problem1 = "Не было старта работы" if self.start_at is None else None
        problem2 = "Не было стопа работы" if self.stop_at is None else None
        return problem0 or problem1 or problem2 or self.correction_comment

    def __str__(self):
        return f"Статус {self.executer} заявка #{self.task.id if self.task else '--'}"

    class Meta:
        verbose_name = "2.Статус исполнителя"
        verbose_name_plural = "2.Статусы исполнителей"


class ApprovedStatus(Enum):
    WAITING = "WAITING"
    APPROVED = "APPROVED"
    FORBIDDEN = "FORBIDDEN"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)


ApprovedStatusEnum = GEnum.from_enum(ApprovedStatus)


class AdditionalTask(models.Model):
    """
    Дополнительные описания у Заявок
    """

    datetime = models.DateTimeField()
    description = models.CharField(blank=False, null=False, default="", max_length=255)


class Task(models.Model):
    """
    Заявка
    """

    STATUSES = (
        ("STEP_1_CREATED", "заявка создана"),
        ("STEP_2_WAITING", "появились исполнители"),
        ("STEP_3_COLLECT", "список исполнителей набран"),
        ("STEP_4_CONFIRMED", "список исполнителей подтвержден"),
        ("STEP_5_START", "старт задачи"),
        ("STEP_6_DONE", "заявка выполнена"),
        ("DELETED", "заявка удалена"),
        # ('ARCHIVED','заявка в архиве'),
    )

    PAYMENT_STATUSES = (
        (None, "нет статуста"),
        ("create_payment", "счет сформирован"),
        ("paid_payment", "счет оплачен"),
    )

    # customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    manager = models.ForeignKey(
        Manager, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Менеджер", db_index=True
    )

    profession = models.ForeignKey(
        Profession, on_delete=models.PROTECT, null=True, blank=True, verbose_name="Профессия", db_index=True
    )
    personal_profession = models.ForeignKey(
        PersonalProfession, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Эксклюзивная профессия"
    )
    personal_profession_name = models.CharField(
        default=None, null=True, max_length=255, help_text="Наименование персональной профессии"
    )
    count_executers = models.IntegerField(
        default=1, help_text="Количество исполнителей", verbose_name="Количество Исполнителей"
    )
    rent = models.FloatField(default=0, help_text="Оплата за единицу объема", verbose_name="Ставка")
    start_at = models.DateTimeField(
        help_text="Время начала работы, формат: ISO 8601", verbose_name="Старт работ", db_index=True
    )
    duration = models.IntegerField(
        default=6, help_text="Время выполнения от 6 до 24 часов", verbose_name="Объем заявки"
    )
    comment = models.CharField(
        default="", max_length=255, help_text="Описание заявки (255 символов)", verbose_name="Комментарий"
    )

    executers = models.ManyToManyField(ExecuterState, verbose_name="Исполнители", db_index=True)
    min_rating = models.IntegerField(default=0, null=False, help_text="Минимальный рейтинг", verbose_name="Рейтинг")
    status = models.CharField(
        choices=STATUSES,
        max_length=40,
        default=STATUSES[0][0],
        help_text="Статус заявки",
        verbose_name="Статус заявки",
    )
    payment_status = models.CharField(
        choices=PAYMENT_STATUSES,
        max_length=40,
        default=None,
        null=True,
        help_text="Статус оплаты заявки",
        verbose_name="Статус оплаты заявки",
    )
    for_favorite = models.BooleanField(default=False, help_text="Флаг сперва избранным", verbose_name="Избранные")
    is_approved = models.BooleanField(
        default=True, help_text="Флаг на одобрение заявки главным менеджером", verbose_name="Подтверждение"
    )
    is_archived = models.BooleanField(default=False, help_text="Флаг на архив", verbose_name="Архив")
    is_archived_for_admin = models.BooleanField(
        default=False, help_text="Флаг на архив администратора", verbose_name="Архив у Администратора"
    )

    additional = models.OneToOneField(
        AdditionalTask,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Дополнительная информация",
        help_text="Дополнительная информация",
    )

    created_at = models.DateTimeField(auto_now_add=True, help_text="Время создания")
    updated_at = models.DateTimeField(auto_now=True, help_text="Время последнего обновления")

    def to_transfer(self, to_date):
        payments_with_current_period = ClosingDocument.objects.filter(
            start_date__lte=self.start_at,
            end_date__gte=self.start_at,
            is_block=True,
            tasks__manager__hotel=self.manager.hotel,
        ).count()

        assert payments_with_current_period == 0, f"Заявка #{self.id} находится в заблокированном периоде"

        payments_with_block_period = ClosingDocument.objects.filter(
            start_date__lte=to_date, end_date__gte=to_date, is_block=True, tasks__manager__hotel=self.manager.hotel
        ).count()

        assert payments_with_block_period == 0, f"Невозможно перенести заявку #{self.id} - " "период заблокирован"
        self.start_at = to_date
        self.save()

    @property
    def is_block_to_modify(self):
        payments_with_current_period = ClosingDocument.objects.filter(
            start_date__lte=self.start_at,
            end_date__gte=(self.start_at - timedelta(days=1)),
            is_block=True,
            tasks__manager__hotel=self.manager.hotel,
        ).count()

        assert payments_with_current_period == 0, f"Заявка #{self.id} находится в заблокированном периоде"
        assert (
            self.payment_set.filter(status_executers="paid_payment").count() == 0
        ), f"Заявка #{self.id} имеет выплату"
        assert self.start_at.date() >= timezone.now().date(), f"Нельзя - заявка в прошлом периоде"
        return True

    @property
    def without_tax(self):
        return (self.rent * (self.profession.multiplier / 100)) + (
            self.rent * (1 - (self.profession.multiplier / 100))
        ) / 1.2

    @property
    def for_hoops(self):
        return self.rent * (self.profession.percent / 100)

    @property
    def for_hoops_without_tax(self):
        return self.for_hoops / 1.2

    @property
    def is_closed(self):
        return bool(timezone.now() > self.start_at) or bool(self.executers.all().count() == self.count_executers)

    @property
    def rent_for_executer(self):
        return float(self.rent) * float(self.profession.multiplier / 100)

    @property
    def stop_at(self):
        return self.start_at + timedelta(hours=self.duration)

    @property
    def finish_name(self):
        return self.profession.name if self.personal_profession is None else self.personal_profession.name

    @property
    def full_work_time(self):
        return sum(x.get_work_time_in_hours for x in self.executers.all())

    @property
    def full_work_time_real(self):
        return sum(x.get_work_time_in_hours_real for x in self.executers.all())

    @property
    def full_pay_real(self):
        return self.full_work_time_real * self.rent

    def __str__(self):
        return f"Заявка №{self.id} "

    class Meta:
        verbose_name = "1.Заявка"
        verbose_name_plural = "1.Заявки"
        ordering = ["-id"]


class CommentOfTask(models.Model):
    """
    Комментарий к заявке для подтверждения
    """

    tasks = models.ManyToManyField(Task, blank=True, help_text="Заявки, к которым применим текущий комментарий")
    text = models.CharField(null=True, max_length=2000, help_text="Текст комментария (2000 символов)", blank=True)

    created_at = models.DateTimeField(auto_now_add=True, help_text="Время создания")
    updated_at = models.DateTimeField(auto_now=True, help_text="Время последнего обновления")


class MetaInformationNotification(models.Model):
    """
    Мета Информация для Уведомлений (для ссылок и тд)
    """

    task_id = models.IntegerField(null=True, default=None, help_text="Номер заявки", verbose_name="Номер заявки")


class Notification(models.Model):
    """
    Уведомления об изменениях
    """

    class TypeNotification(models.TextChoices):
        ACCOUNT = "ACCOUNT", _("Уведомление об аккаунте")
        TASK = "TASK", _("Уведомление о заявке")
        FINANCE = "FINANCE", _("Уведомление о финансах")
        OTHER = "OTHER", _("Уведомление")

    TypeNotificationEnum = GEnum.from_enum(TypeNotification)

    ROLES = (
        ("manager", "менеджер"),
        ("executer", "исполнитель"),
    )
    type = models.CharField(
        choices=TypeNotification.choices, max_length=20, default=TypeNotification.TASK, help_text="Тип уведомления"
    )
    role = models.CharField(choices=ROLES, max_length=40, default=ROLES[0][0], help_text="роль объекта получателя")
    id_instance = models.CharField(max_length=12, default="", help_text="ID получателя")
    text = models.CharField(max_length=255, default="", help_text="Текст сообщения")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Дата создания")
    read = models.BooleanField(default=False, help_text="Статус сообщения")
    meta = models.OneToOneField(
        MetaInformationNotification,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Мета информация",
        help_text="Мета информация",
    )

    def __str__(self):
        return f"Уведомление №{self.id} для {self.role} #{self.id_instance}"

    def save(
        self, notification: bool = False, url: str = "notifications", task_id: int = None, *args, **kwargs
    ) -> None:
        """
        Сохранение Уведомления с кастомными параметрами
        @param notification: булевый указатель на отправку пуш уведомления
        @param url: ссылка для пуша Уведомления
        @param task_id: идентификатор Заявки для мета информации
        @param args:
        @param kwargs:
        """
        # если есть указатель на заявку
        if task_id:
            # создаем объект мета информации
            meta = MetaInformationNotification.objects.create(task_id=task_id)
            # присваиваем мета информацию Уведомлению
            self.meta = meta
        # вызываем родительский метод save
        super(Notification, self).save(*args, **kwargs)
        try:
            # если флаг на отправку push есть
            if notification:
                # проверяем что получатель это Исполнитель
                if self.role == self.ROLES[1][0]:
                    # получаем все токены FCM
                    fcm_tokens = list(
                        set(FCMToken.objects.filter(executer_id=self.id_instance).values_list("token", flat=True))
                    )
                    send_push.delay(text=self.text, url=url, fcm_tokens=fcm_tokens)

                else:
                    if settings.DEV:
                        # MySubscription.broadcast(self.text)
                        MySubscription.new_message(id_instance=str(self.id_instance), text=self.text)
        except Exception as e:
            print(f"Ошибка отправки пуш уведомления: {e}")

    class Meta:
        verbose_name = "Уведомление"
        verbose_name_plural = "Уведомления"


class FeedbackExecuter(models.Model):
    """
    Отзыв исполнителя о заявке
    """

    executer = models.ForeignKey(Executer, on_delete=models.CASCADE, help_text="Исполнитель работы")
    task = models.ForeignKey(Task, on_delete=models.CASCADE, help_text="Выполненная работа")
    rating = models.IntegerField(default=0, help_text="Оценка по пятибалльной шкале")
    comment = models.CharField(max_length=255, null=True, blank=True, help_text="Текст сообщения")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Время создания")
    updated_at = models.DateTimeField(auto_now=True, help_text="Время последнего обновления")

    def __str__(self):
        return f"{self.executer} о {self.task}"

    class Meta:
        verbose_name = "Отзывы исполнителей о заявках"
        verbose_name_plural = "Отзывы исполнителей о заявках"


class FeedbackManager(models.Model):
    """
    Отзыв менеджера об исполнителе
    """

    manager = models.ForeignKey(Manager, on_delete=models.CASCADE, help_text="Менеджер работы")
    executer = models.ForeignKey(Executer, on_delete=models.CASCADE, help_text="Исполнитель работы")
    task = models.ForeignKey(Task, on_delete=models.CASCADE, help_text="Выполненная работа")
    rating = models.IntegerField(default=5, help_text="Оценка по пятибалльной шкале")
    comment = models.CharField(max_length=255, null=True, blank=True, help_text="Текст сообщения")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Время создания")
    updated_at = models.DateTimeField(auto_now=True, help_text="Время последнего обновления")

    def __str__(self):
        return f"{self.manager} о {self.executer}"

    class Meta:
        verbose_name = "Отзывы менеджеров об исполнителях"
        verbose_name_plural = "Отзывы менеджеров об исполнителях"


class AdminDoc(models.Model):
    """
    Документ об оплате для админа
    """

    TYPES = (
        ("CUSTOMER_PAYMENT", "счет для заказчиков"),
        ("EXECUTER_PAYMENT", "реестр оплат для исполнителей"),
    )

    path = models.CharField(default="", unique=True, max_length=100, db_index=True, null=False)
    type = models.CharField(choices=TYPES, max_length=17, default=TYPES[0][0], help_text="Тип документа")
    date_update = models.DateTimeField(auto_now=True, help_text="Время последнего обновления")

    def __str__(self):
        return f"Файл администратора №{self.id} "

    class Meta:
        verbose_name = "Файл администратора"
        verbose_name_plural = "Файлы администратора"


class Payment(models.Model):
    """
    Документ об оплате
    """

    PAYMENT_STATUSES = (
        ("create_payment", "счет сформирован"),
        ("paid_payment", "счет оплачен"),
    )

    TYPES = (("primary", "primary"), ("correction", "correction"))

    admin = models.ForeignKey(Admin, default=Admin.get_main_admin, on_delete=models.SET_DEFAULT, help_text="Админ")
    type = models.CharField(choices=TYPES, max_length=20, default=TYPES[0][0], help_text="Тип платежки")

    tasks = models.ManyToManyField(Task, blank=True)

    start_date = models.DateTimeField(null=False, default=timezone.now)
    end_date = models.DateTimeField(null=False, default=timezone.now)

    status_executers = models.CharField(
        choices=PAYMENT_STATUSES,
        max_length=17,
        default=PAYMENT_STATUSES[0][0],
        help_text="Статус платежа исполнителям",
    )
    file_path_executer = models.CharField(max_length=255, default="", null=False, blank=True)

    create_at = models.DateTimeField(auto_now_add=True, help_text="Время создания")
    update_at = models.DateTimeField(auto_now=True, help_text="Время последнего обновления")
    log_data = models.TextField(null=True, blank=True, help_text="Лог исполнения", verbose_name="Лог исполнения")
    is_busy = models.BooleanField(default=False, help_text="Выполняется", verbose_name="Выполняется")
    is_archive = models.BooleanField(default=False, help_text="Архив", verbose_name="Архив")
    is_individual = models.BooleanField(default=False, help_text="Мобильная выплата", verbose_name="Мобильная выплата")

    @property
    def period_str(self):
        return (
            f'{(self.start_date + timedelta(hours=12)).date().strftime("%d.%m.%Y")} - '
            f'{(self.end_date + timedelta(hours=12)).date().strftime("%d.%m.%Y")}'
        )

    @property
    def can_delete(self):
        """
        Свойство на возможность удаления
        :return:  Истина если можно удалять
        """
        # если есть чеки со статусом не СОЗДАН - удалять нельзя
        return not bool(self.paymentjumpfinance_set.all().exclude(status=PaymentJumpFinance.STATUSES[0][0]))

    def __str__(self):
        return f"Выплата №{self.id} "

    class Meta:
        verbose_name = "Выплата"
        verbose_name_plural = "Выплаты"


class PaymentWithCard(models.Model):
    """
    Оплата через Тинькофф
    """

    class Meta:
        verbose_name = "Платеж Tinkoff"
        verbose_name_plural = "Платежи Tinkoff"

    executer = models.ForeignKey(Executer, null=True, on_delete=models.CASCADE, help_text="Исполнитель")
    dict_payment = models.CharField(max_length=2000, default=None, null=True, blank=True)
    status = models.CharField(max_length=1000, default=None, null=True, blank=True)
    dict_cancel = models.CharField(max_length=2000, default=None, null=True, blank=True)
    status_cancel = models.CharField(max_length=1000, default=None, null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True, help_text="Время создания")
    update_at = models.DateTimeField(auto_now=True, help_text="Время последнего обновления")

    @property
    def payment_id(self):
        try:
            payment_dict = json.loads(self.status)
            return payment_dict["PaymentId"]
        except json.decoder.JSONDecodeError:
            return -1
        except KeyError:
            return 0

    def __str__(self):
        return f"Банковская оплата {self.executer} №{self.id}"


class ExecutorJumpFinance(models.Model):
    """
    Исполнитель в JumpFinance
    """

    executer = models.OneToOneField(
        Executer, null=True, on_delete=models.CASCADE, verbose_name="Исполнитель", help_text="Исполнитель"
    )
    id_contractor = models.IntegerField(
        default=None,
        null=True,
        blank=True,
        verbose_name="ID JumpFinance",
        help_text="Идентификатор исполнителя в JumpFinance",
    )

    is_verified = models.BooleanField(
        default=False,
        verbose_name="Привязан к компании",
        help_text="Получено подтверждение из налоговой," " что исполнитель привязан к компании",
    )
    is_can_pay_taxes = models.BooleanField(
        default=False,
        verbose_name="Разрешил уплату налогов",
        help_text="Получено подтверждение из налоговой," " что самозанятый разрешил компании уплачивать налог",
    )
    has_company_agrees_pay_taxes = models.BooleanField(
        default=False,
        verbose_name="Включена уплата налогов",
        help_text="В настройках исполнителя включена опция," " что компания уплачивает налог за исполнителя",
    )
    has_warning = models.BooleanField(
        default=False,
        verbose_name="Нехватка разрешений",
        help_text="Не хватает каких-либо разрешений со стороны самозанятого",
    )

    last_message = models.CharField(
        null=True, max_length=255, blank=True, verbose_name="Сообщение", help_text="Последнее сообщение от JumpFinance"
    )

    create_at = models.DateTimeField(auto_now_add=True, help_text="Время создания")
    update_at = models.DateTimeField(auto_now=True, help_text="Время последнего обновления")

    def __str__(self):
        return f"{self.executer}"

    class Meta:
        verbose_name = "Исполнитель JumpFinance"
        verbose_name_plural = "Исполнители JumpFinance"


class PaymentJumpFinance(models.Model):
    """
    Оплата через JumpFinance
    """

    STATUSES = (
        ("CREATED", "cоздан в системе HOOPS"),
        ("PAID", "оплачен (без возможности дальнейших действий)"),
        ("REFUSED", "отклонён (без возможности дальнейших действий)"),
        ("IN_PROCESSING", "в обработке (ждём проведение через платежные системы)"),
        ("WAIT_APPROVE", "ожидает подтверждения (требуется подтверждение выплаты в ЛК)"),
        (
            "ERROR",
            "ошибка выплаты (с возможностью повторить действие,"
            "отменить выплату или зачислить средства на баланс исполнителя)",
        ),
    )

    contractor = models.ForeignKey(
        ExecutorJumpFinance, null=True, on_delete=models.CASCADE, help_text="Исполнитель JumpFinance"
    )
    payment = models.ForeignKey(Payment, null=True, on_delete=models.CASCADE, help_text="Платежка HOOPS")

    id_payment = models.IntegerField(
        default=None, null=True, blank=True, help_text="Идентификатор платежа в системе JumpFinance"
    )
    amount = models.FloatField(default=None, null=True, blank=True, help_text="Сумма заявки на выплату")
    amount_paid = models.FloatField(
        default=None,
        null=True,
        blank=True,
        help_text="Сумма фактической выплаты (после вычета комиссии с исполнителя и удержаний на уплату налога)",
    )
    comission = models.FloatField(
        default=None, null=True, blank=True, help_text="Удержанная с исполнителя сумма комиссии"
    )
    comission_bank = models.FloatField(
        default=None, null=True, blank=True, help_text="Сумма комиссии, удержанная банком при проведении выплаты"
    )
    tax_amount = models.FloatField(
        default=None, null=True, blank=True, help_text="Удержанная с исполнителя сумма на уплату налога самозанятых"
    )
    purpose = models.CharField(max_length=1000, default=None, null=True, blank=True, help_text="Фраза для чека")
    status = models.CharField(choices=STATUSES, max_length=13, default=STATUSES[0][0], help_text="Статус")
    fns_key = models.CharField(max_length=100, default=None, null=True, blank=True, help_text="Внутренний ключ ФНС")
    fns_url = models.URLField(null=True, default=None, blank=True, help_text="Ссылка на актуальный чек от ФНС")
    saved_url = models.URLField(
        null=True, default=None, blank=True, help_text="Ссылка на чек, сохраненный локально в момент его получения"
    )
    is_final = models.BooleanField(default=False, help_text="Указывает, является ли статус выплаты финальным")
    create_at = models.DateTimeField(auto_now_add=True, help_text="Время создания")
    update_at = models.DateTimeField(auto_now=True, help_text="Время последнего обновления")

    def __str__(self):
        return f"{self.contractor.executer}"

    class Meta:
        verbose_name = "Платеж JumpFinance"
        verbose_name_plural = "Платежи JumpFinance"


class FCMToken(models.Model):
    """
    Токен FIreBase
    """

    executer = models.ForeignKey(Executer, null=True, on_delete=models.CASCADE, help_text="Владелец токена")
    token = models.CharField(null=False, default="", max_length=255, help_text="токен firebase")

    def __str__(self):
        return f"FCMToken {self.executer}"

    class Meta:
        verbose_name = "FCM токен"
        verbose_name_plural = "FCM токены"

    def send_push(self, text, url="home"):
        send_push.delay(text=text, url=url, fcm_tokens=self.token)


class TypeDocument(Enum):
    OFFER = "OFFER"
    LICENSE_AGREEMENT = "LICENSE_AGREEMENT"
    PERSONAL_DATA_AGREEMENT = "PERSONAL_DATA_AGREEMENT"
    USER_AGREEMENT = "USER_AGREEMENT"
    NOTICE = "NOTICE"
    POST = "POST"
    INFO_BLOCK = "INFO_BLOCK"
    EXECUTER_NOTICE = "EXECUTER_NOTICE"
    LOGO = "LOGO"
    LANDING_POST = "LANDING_POST"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)


TypeDocumentEnum = GEnum.from_enum(TypeDocument)


class TypeAgreement(Enum):
    OFFER = "OFFER"
    LICENSE_AGREEMENT = "LICENSE_AGREEMENT"
    PERSONAL_DATA_AGREEMENT = "PERSONAL_DATA_AGREEMENT"
    USER_AGREEMENT = "USER_AGREEMENT"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)


TypeAgreementEnum = GEnum.from_enum(TypeAgreement)


class Agreement(models.Model):
    """
    Документы и соглашения
    """

    type = models.CharField(
        max_length=255, choices=TypeAgreement.choices(), default=TypeAgreement.OFFER.value, help_text="Тип документа"
    )
    is_actual = models.BooleanField(default=True, help_text="Маркер актуальности")
    file = models.ForeignKey(FileInfo, on_delete=models.CASCADE, help_text="Файл", null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True, help_text="Время создания")

    def __str__(self):
        return f"Документы {self.type}"

    class Meta:
        verbose_name = "Документ"
        verbose_name_plural = "Документы"


class Notice(models.Model):
    """
    Уведомляющие документы
    """

    admin = models.ForeignKey(Admin, default=Admin.get_main_admin, on_delete=models.SET_DEFAULT, help_text="Админ")
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, null=True, help_text="Гостиница")
    files = models.ManyToManyField(FileInfo, blank=True, help_text="Файлы уведомления")
    subject = models.CharField(max_length=255, default="", null=False, blank=True, help_text="Уведомление")
    is_archive = models.BooleanField(default=False)
    is_sent = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True, help_text="Время создания")

    def __str__(self):
        return f"Уведомление {self.hotel}"

    class Meta:
        verbose_name = "Уведомление"
        verbose_name_plural = "Уведомления"
        ordering = ["-id"]


class ExecuterNotice(models.Model):
    """
    Уведомляющие документы исполнителя
    """

    admin = models.ForeignKey(Admin, default=Admin.get_main_admin, on_delete=models.SET_DEFAULT, help_text="Админ")
    executer = models.ForeignKey(Executer, on_delete=models.CASCADE, null=True, help_text="Исполнитель")
    files = models.ManyToManyField(FileInfo, blank=True, help_text="Файлы уведомления")
    create_at = models.DateTimeField(auto_now_add=True, help_text="Время создания")
    is_auto_generate = models.BooleanField(default=False, help_text="Флаг на сгенерированный документ")

    def __str__(self):
        return f"Уведомление {self.executer}"

    class Meta:
        verbose_name = "Уведомление Исполнителя"
        verbose_name_plural = "Уведомления Исполнителей"
        ordering = ["-id"]


class TypeVisible(Enum):
    ALL = "ALL"
    EXECUTOR = "EXECUTOR"
    MANAGER = "MANAGER"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)


TypeVisibleEnum = GEnum.from_enum(TypeVisible)


class Post(models.Model):
    """
    Новость
    """

    admin = models.ForeignKey(Admin, default=Admin.get_main_admin, on_delete=models.SET_DEFAULT, help_text="Админ")
    title = CustomEmojiCharField(max_length=1000, default="", null=False, blank=True, help_text="Заголовок")
    content = CustomEmojiTextField(max_length=4000, null=False, blank=True, help_text="Тело поста")
    file = models.ForeignKey(
        FileInfo, blank=True, null=True, default=None, on_delete=models.SET_NULL, help_text="Файл"
    )
    visible = models.CharField(
        max_length=255, choices=TypeVisible.choices(), default=TypeVisible.ALL, help_text="Область видимости"
    )
    is_public = models.BooleanField(default=False, help_text="Доступен для всех")
    create_at = models.DateTimeField(auto_now_add=True, help_text="Время создания")
    update_at = models.DateTimeField(auto_now=True, help_text="Время последнего обновления")

    def __str__(self):
        return f"Новостной пост {self.admin}"

    class Meta:
        verbose_name = "Новостной пост"
        verbose_name_plural = "Новостные посты"


class PostLanding(models.Model):
    """
    Новость для лендинга
    """

    admin = models.ForeignKey(Admin, default=Admin.get_main_admin, on_delete=models.SET_DEFAULT, help_text="Админ")
    title = CustomEmojiCharField(max_length=255, default="", null=False, blank=True, help_text="Заголовок")
    content = CustomEmojiTextField(max_length=2000, null=False, blank=True, help_text="Тело поста")
    file = models.ForeignKey(
        FileInfo, blank=True, null=True, default=None, on_delete=models.SET_NULL, help_text="Файл"
    )
    hashtag = models.CharField(max_length=255, default="", null=False, blank=True, help_text="Хештег")
    url = models.CharField(
        max_length=255, default=uuid.uuid4, null=False, blank=True, help_text="Путь к посту", unique=True
    )
    is_public = models.BooleanField(default=False, help_text="Доступен для всех")
    create_at = models.DateTimeField(auto_now_add=True, help_text="Время создания")
    update_at = models.DateTimeField(auto_now=True, help_text="Время последнего обновления")

    def __str__(self):
        return f"Лендинг пост {self.admin}"

    class Meta:
        verbose_name = "Лендинг пост"
        verbose_name_plural = "Лендинг посты"


class Logo(models.Model):
    """
    Логотипы на главную страницу
    """

    admin = models.ForeignKey(
        Admin, default=Admin.get_main_admin, on_delete=models.SET_DEFAULT, help_text="Админ", verbose_name="Админ"
    )
    description = models.CharField(
        max_length=255, default="", null=True, blank=True, help_text="Описание", verbose_name="Описание"
    )
    file = models.ForeignKey(
        FileInfo, blank=True, null=True, default=None, on_delete=models.SET_NULL, help_text="Файл", verbose_name="Файл"
    )
    is_visible = models.BooleanField(default=True, help_text="Видимость", verbose_name="Видимость")
    create_at = models.DateTimeField(auto_now_add=True, help_text="Время создания")
    update_at = models.DateTimeField(auto_now=True, help_text="Время последнего обновления")

    def __str__(self):
        return f"Логотип {self.description} {self.admin}"

    class Meta:
        verbose_name = "Логотип"
        verbose_name_plural = "Логотипы"


class InfoBlock(models.Model):
    """
    Справка
    """

    admin = models.ForeignKey(Admin, default=Admin.get_main_admin, on_delete=models.SET_DEFAULT, help_text="Админ")
    category = models.CharField(max_length=255, default="", null=False, blank=True, help_text="Категория")
    title = models.CharField(max_length=255, default="", null=False, blank=True, help_text="Заголовок")
    content = models.TextField(max_length=2000, null=False, blank=True, help_text="Тело поста")
    files = models.ManyToManyField(FileInfo, help_text="Медиа файлы")
    weight = models.IntegerField(default=0, help_text="Вес информационного блока")
    visible = models.CharField(
        max_length=255, choices=TypeVisible.choices(), default=TypeVisible.ALL.value, help_text="Область видимости"
    )
    is_public = models.BooleanField(default=False, help_text="Доступен для всех")
    create_at = models.DateTimeField(auto_now_add=True, help_text="Время создания")
    update_at = models.DateTimeField(auto_now=True, help_text="Время последнего обновления")

    def __str__(self):
        return f"Информационный блок {self.title}"

    class Meta:
        verbose_name = "Помощь"
        verbose_name_plural = "Блоки Помощь"


class AdminJournal(models.Model):
    class TypeJournal(models.TextChoices):
        TASK = "TASK", _("Журнал действий над заявками")

    TypeJournalEnum = GEnum.from_enum(TypeJournal)

    ROLES = (
        ("manager", "менеджер"),
        ("executer", "исполнитель"),
    )
    type = models.CharField(
        choices=TypeJournal.choices,
        max_length=4,
        default=TypeJournal.TASK,
        help_text="Тип журнала",
        verbose_name="Тип",
    )
    admin = models.ForeignKey(
        Admin,
        default=Admin.get_main_admin,
        on_delete=models.SET_DEFAULT,
        help_text="Админ",
        verbose_name="Администратор",
    )
    text = models.TextField(blank=True, help_text="Описание действия", verbose_name="Текст")

    create_at = models.DateTimeField(auto_now_add=True, help_text="Время создания", verbose_name="Дата")
    update_at = models.DateTimeField(auto_now=True, help_text="Время последнего обновления")

    def save(self, *args, **kwargs) -> None:
        super().save(*args, **kwargs)
        # logger.info(self.text)

    def __str__(self):
        return f"Запись о {self.admin} о {self.type}"

    class Meta:
        verbose_name = "Журнал действий Администратора"
        verbose_name_plural = "Журналы действий Администраторов"
