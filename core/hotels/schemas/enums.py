import graphene


def get_value(value):
    return getattr(value, "value", value)


class TypeMedia(graphene.Enum):
    PASSPORT = "PASSPORT"
    AVATAR = "AVATAR"
    DOCUMENT = "DOCUMENT"

    @property
    def description(self):
        return self.value


class TypeReportDoc(graphene.Enum):
    # TABLE = 'TABLE'
    STANDART_REPORT = "STANDART_REPORT"
    HISTORY_AND_FORECAST = "HISTORY_AND_FORECAST"
    BY_TYPE = "BY_TYPE"
    MANAGERS_REPORT = "MANAGERS_REPORT"
    DIFFERENCE_REPORT = "DIFFERENCE_REPORT"
    MANAGEMENT_REPORT = "MANAGEMENT_REPORT"
    EXECUTORS_LIST = "EXECUTORS_LIST"

    @property
    def description(self):
        # if self == TypeReportDoc.TABLE:
        #      return 'Табличный отчет'
        if self == TypeReportDoc.STANDART_REPORT:
            return "Стандартный отчет"
        elif self == TypeReportDoc.HISTORY_AND_FORECAST:
            return "История и прогноз"
        elif self == TypeReportDoc.BY_TYPE:
            return "По типам услуг"
        elif self == TypeReportDoc.MANAGERS_REPORT:
            return "Отчет по менеджерам"
        elif self == TypeReportDoc.DIFFERENCE_REPORT:
            return "Отчет по корректировкам"
        elif self == TypeReportDoc.MANAGEMENT_REPORT:
            return "Управленческий отчет"
        elif self == TypeReportDoc.EXECUTORS_LIST:
            return "Список исполнителей"

    def __str__(self):
        return self.value


class TypeExecutersDoc(graphene.Enum):

    STANDART_REPORT = "STANDART_REPORT"
    BY_TYPE = "BY_TYPE"
    FINANCIAL = "FINANCIAL"
    DIFFERENCE_REPORT = "DIFFERENCE_REPORT"

    @property
    def description(self):
        if self == TypeExecutersDoc.STANDART_REPORT:
            return "Стандартный отчет"
        elif self == TypeExecutersDoc.BY_TYPE:
            return "По типам услуг"
        elif self == TypeExecutersDoc.FINANCIAL:
            return "Сводный финансовый"
        elif self == TypeExecutersDoc.DIFFERENCE_REPORT:
            return "Отчет по корректировкам"


class SortFields(graphene.Enum):
    start_at = "start_at"
    rent = "rent"


class Sort(graphene.Enum):
    ASC = "ASC"
    DESC = "DESC"

    @property
    def description(self):
        return self.value

    def __repr__(self):
        return self.value


class Genders(graphene.Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"

    @property
    def description(self):
        if self == Genders.MALE:
            return "MALE"
        return "FEMALE"


class EnumCitizenShip(graphene.Enum):
    RUSSIA = "Российская Федерация"
    OTHER = "Иное"

    @property
    def description(self):
        if self == EnumCitizenShip.RUSSIA:
            return "Российская Федерация"
        return "Иное"


class PaymentStatus(graphene.Enum):
    create_payment = "create_payment"
    paid_payment = "paid_payment"

    @property
    def description(self):
        if self == PaymentStatus.create_payment:
            return "create_payment"
        return "paid_payment"


class PaymentEnum(graphene.Enum):
    primary = "primary"
    correction = "correction"

    @property
    def description(self):
        if self == PaymentEnum.primary:
            return "primary"
        return "correction"
