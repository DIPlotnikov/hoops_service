import logging
import os
from dataclasses import dataclass
from datetime import datetime

import pdfkit
from django.db.models import Count
from hotels.utils.invoice import round_value_for_hoops

from .nds_handler import calc_tax, calc_cost_without_tax
from ..config import bucket as bucket
from ..config import core as core
from ..models import Profession
from ..scripts import server_handler as SH

logger = logging.getLogger(__name__)


@dataclass
class RowForInvoice:
    """
    Данные для одной строки акта
    """
    hotel_name: str
    number: int
    tasks: str
    # объем работы
    volume: float
    volume_str: str

    # сумма для hoops
    hoops_cost: float
    # сумма для исполнителей
    executer_cost: float

    # коды океи
    okei_code: str
    okei_name: str

    # поля для платежек
    rent_str: str
    hoops_without_tax_str: str
    tax_str: str
    rent_for_executer: str
    nds: str
    remuneration: str
    remuneration_without_tax_str: str
    hoops_cost_without_remuneration: str
    remuneration_tax_str: str
    remuneration_rent_str: str
    hoops_cost_without_remuneration_without_tax_str: str
    hoops_cost_without_remuneration_tax_str: str
    hoops_cost_without_remuneration_rent_str: str

    @property
    def text_for_hoops(self):
        return f"Стоимость Услуг HOOPS Service по заявкам {self.tasks}"

    @property
    def text_for_remuneration(self):
        return f"Вознаграждение за исполнение поручения по заявкам {self.tasks}"

    @property
    def text_for_executer(self):
        return (
            "Оплата HOOPS для выплаты исполнителям согласно раздела 4 договора оферты от {DATE_OFFER} за оказанные услуги по заявкам  "
            + self.tasks
        )

    @staticmethod
    def get_str_with_format(value) -> str:
        """
        Преобразование элемента в строку в формате для акта
        @param value: элемент преобразования
        """
        value = round(value, 2)
        return "{:.2f}".format(value)

    @property
    def get_tuple_with_data_for_row_bill_hoops(self):
        """
        Кортеж данных для счета - строка для оплаты услуг HOOPS
        """
        return (
            self.text_for_hoops,
            self.hoops_cost_without_remuneration,
            self.volume_str,
            self.hoops_cost_without_remuneration_rent_str,
        )

    @property
    def get_tuple_with_data_for_row_bill_hoops_remuneration(self):
        """
        Кортеж данных для счета - строка для оплаты услуг HOOPS
        """
        return self.text_for_remuneration, self.remuneration, self.volume_str, self.remuneration_rent_str

    @property
    def get_tuple_with_data_for_row_bill_executer(self):
        """
        Кортеж данных для счета - строка для оплаты услуг Исполнителей
        """
        return self.text_for_executer, self.executer_cost, self.volume_str, self.rent_for_executer

    @property
    def get_tuple_with_data_for_remuneration(self):
        """
        Кортеж данных для счета - строка для оплаты услуг Исполнителей
        """
        return self.text_for_remuneration, self.remuneration

    @property
    def get_tuple_with_data_for_row_diadok_row(self) -> tuple:
        """
        Получение кортежа данных для строки диадока
        """
        return (
            int(self.number),
            self.tasks,
            self.okei_code,
            self.volume_str,
            self.hoops_cost_without_remuneration_rent_str,
            self.hoops_cost_without_remuneration_without_tax_str,
            self.hoops_cost_without_remuneration,
            self.hoops_cost_without_remuneration_tax_str,
            self.okei_name,
            self.nds + "%" if self.nds else "-",
        )

    @property
    def get_tuple_with_data_for_row_diadok_row_remuneration(self) -> tuple:
        """
        Получение кортежа данных для строки диадока
        """
        return (
            int(self.number),
            self.tasks,
            self.okei_code,
            self.volume_str,
            self.remuneration_rent_str,
            self.remuneration_without_tax_str,
            self.remuneration,
            self.remuneration_tax_str,
            self.okei_name,
            self.nds + "%" if self.nds else "-",
        )


    @property
    def get_tuple_with_data_for_group_cd(self) -> tuple:
        """
        Получение кортежа данных для строки закрывающих документов (группы компаний)
        """
        # Значения фиксированы для данного отчета.
        okei = '769'
        okei_name = 'шт'
        volume = '1'

        return (
            int(self.number),
            self.hotel_name,
            okei,
            volume,
            self.hoops_cost_without_remuneration_without_tax_str, # объем фиксирован, сумма не меняется.
            self.hoops_cost_without_remuneration_without_tax_str,
            self.hoops_cost_without_remuneration,
            self.hoops_cost_without_remuneration_tax_str,
            okei_name,
            self.nds + "%" if self.nds else "-",
        )

    @property
    def get_tuple_with_data_for_group_cd_remuneration(self) -> tuple:
        """
        Получение кортежа данных для строки закрывающих документов (группы компаний)
        """
        # Значения фиксированы для данного отчета.
        okei = '769'
        okei_name = 'шт'
        volume = '1'
        return (
            int(self.number),
            self.hotel_name,
            okei,
            volume,
            self.remuneration_without_tax_str, # объем фиксирован, сумма не меняется.
            self.remuneration_without_tax_str,
            self.remuneration,
            self.remuneration_tax_str,
            okei_name,
            self.nds + "%" if self.nds else "-",
        )

    @property
    def get_tuple_with_data_for_row_act_first_row(self) -> tuple:
        """
        Получение кортежа данных для первой строки акта
        """
        return (
            self.tasks,
            self.volume_str,
            self.hoops_cost_without_remuneration_rent_str,
            self.hoops_cost_without_remuneration_without_tax_str,
            self.hoops_cost_without_remuneration_tax_str,
            self.hoops_cost_without_remuneration,
        )

    @property
    def get_tuple_with_data_for_row_act_remenuration(self) -> tuple:
        """
        Получение кортежа данных для первой строки акта
        """
        return (
            self.remuneration_rent_str,
            self.remuneration_without_tax_str,
            self.remuneration_tax_str,
            self.remuneration,
        )

    @property
    def get_tuple_with_data_for_row_act_second_row(self) -> tuple:
        """
        Получение кортежа данных для первой строки акта
        """
        return self.rent_for_executer, "{:.2f}".format(self.executer_cost), self.okei_name


def format_executers_states_to_invoice_format(executor_states, nds=20.0, remuneration_percent=0, hotel=None) -> tuple:
    """
    Получение списка дата классов с данными для счет-фактуры
    @param remuneration_percent: процент вознаграждения
    @param nds: ставка НДС
    @param executor_states: Статусы исполнителей
    @return: список RowForInvoice
    """
    number_row = 1
    total_price = 0.0
    total_sum_for_executer = 0.0
    total_tax = 0.0
    # по профессиям - их имена и океи коды
    res_hoops = []
    for name, okei in Profession.okei.items():
        # статусы текущей профессии
        current_executer_states = executor_states.filter(task__profession__numerate=name)
        # множество уникальных ставок статусов
        list_of_distinct_rent = set(
            current_executer_states.values_list("task__rent", flat=True).annotate(count=Count("task__rent"))
        )

        # для каждой уникальной ставки текущих статусов
        for rent in list_of_distinct_rent:
            # количество часов
            worktime_in_current_tasks_hours = 0
            # сумма получаемая hoops
            hoops_cost = 0.0
            executer_cost = 0.0
            # список заявок
            tasks = []

            for executor_state in current_executer_states.filter(task__rent=rent):
                if executor_state.status != "STOP":
                    raise ValueError(
                        f"В заявке {executor_state.task.id} у "
                        f"{executor_state.task.manager.hotel} исполнитель #{executor_state.executer.id} "
                        f"{executor_state.executer.middle_name} {executor_state.executer.first_name} "
                        f"{executor_state.executer.second_name} не закончил работать!"
                    )
                if not executor_state.is_check_in_finance:
                    continue

                worktime_in_current_tasks_hours += executor_state.get_work_time_in_hours
                hoops_cost += executor_state.get_sum_for_hoops
                executer_cost += executor_state.get_sum_for_pay
                tasks.append(executor_state.task.id)

            if worktime_in_current_tasks_hours:
                worktime_in_current_tasks_hours = round_value_for_hoops(worktime_in_current_tasks_hours)
                tax = calc_tax(hoops_cost, nds)

                current_remuneration = round(hoops_cost / 100 * remuneration_percent, 2)
                hoops_cost_without_remuneration = hoops_cost - current_remuneration

                current_remuneration_without_tax = RowForInvoice.get_str_with_format(
                    calc_cost_without_tax(current_remuneration, nds)
                )
                remuneration_tax_str = RowForInvoice.get_str_with_format(calc_tax(current_remuneration, nds))
                remuneration_rent_str = RowForInvoice.get_str_with_format(
                    current_remuneration / worktime_in_current_tasks_hours
                )

                hoops_cost_without_remuneration_rent_str = RowForInvoice.get_str_with_format(
                    hoops_cost_without_remuneration / worktime_in_current_tasks_hours
                )

                res_hoops.append(
                    RowForInvoice(
                        hotel_name=hotel.nameHotel if hotel else '',
                        number=number_row,
                        tasks=", ".join(str(x) for x in set(tasks)),
                        volume=worktime_in_current_tasks_hours,
                        volume_str=RowForInvoice.get_str_with_format(worktime_in_current_tasks_hours),
                        hoops_cost=round(hoops_cost, 2),
                        hoops_cost_without_remuneration=round(hoops_cost_without_remuneration, 2),
                        hoops_cost_without_remuneration_without_tax_str=RowForInvoice.get_str_with_format(
                            calc_cost_without_tax(hoops_cost_without_remuneration, nds)
                        ),
                        hoops_cost_without_remuneration_tax_str=RowForInvoice.get_str_with_format(
                            calc_tax(hoops_cost_without_remuneration, nds)
                        ),
                        executer_cost=round(executer_cost, 2),
                        okei_code=okei.get("code"),
                        okei_name=okei.get("num"),
                        rent_str=RowForInvoice.get_str_with_format(hoops_cost / 1.2 / worktime_in_current_tasks_hours),
                        rent_for_executer=RowForInvoice.get_str_with_format(
                            executer_cost / worktime_in_current_tasks_hours
                        ),
                        hoops_without_tax_str=RowForInvoice.get_str_with_format(
                            calc_cost_without_tax(hoops_cost, nds)
                        ),
                        tax_str=RowForInvoice.get_str_with_format(tax),
                        nds=str(nds),
                        remuneration=current_remuneration,
                        remuneration_without_tax_str=current_remuneration_without_tax,
                        remuneration_tax_str=remuneration_tax_str,
                        remuneration_rent_str=remuneration_rent_str,
                        hoops_cost_without_remuneration_rent_str=hoops_cost_without_remuneration_rent_str,
                    )
                )

                total_price += hoops_cost
                total_sum_for_executer += executer_cost
                number_row += 1
                total_tax += tax

    return res_hoops, total_price, total_sum_for_executer, total_tax


def invoice_creator(
    *,
    executor_states,
    number,
    offer_date,
    accepted_at,
    total_price,
    total_tax,
    requisites,
    closing_date=None,
):
    """
    Создание счёт-фактуры
    @param total_tax: налоговая сумма
    @param total_price: общая стоимость
    @param executor_states: отклики Исполнителей
    @param number: Номер счет-фактуры
    @param offer_date: Дата Оферты
    @param closing_date: Дата закрытия документов
    """
    logger.info("Создание счет фактуры html")

    if closing_date is None:
        closing_date = datetime.now()

    file = "SAMPLE_INVOICE.html"

    rows_for_1_task = """
    <tr>
      <td style="border-right:2px solid #000"> </td>
      <td>{0}</td>
      <td>Стоимость Услуг HOOPS Service по заявкам № {1}</td>
      <td> </td>
      <td>{2}</td>
      <td>{8}</td>
      <td>{3}</td>
      <td>{4}</td>
      <td>{5}</td>
      <td></td>
      <td>{9}</td>
      <td>{7}</td>
      <td>{6:.2f}</td>
      <td> </td>
      <td> </td>
      <td> </td>
    </tr>
    """
    rows_for_remenuration = """
    <tr>
      <td style="border-right:2px solid #000"> </td>
      <td>{0}</td>
      <td>Вознаграждение за исполнение поручения по заявкам № {1}</td>
      <td> </td>
      <td>{2}</td>
      <td>{8}</td>
      <td>{3}</td>
      <td>{4}</td>
      <td>{5}</td>
      <td></td>
      <td>{9}</td>
      <td>{7}</td>
      <td>{6:.2f}</td>
      <td> </td>
      <td> </td>
      <td> </td>
    </tr>
    """

    rows_for_all_task = ""

    server = SH.minioDocuments()
    path_return = f"/closing_documents/{requisites.owner.id}/{closing_date.year}/{closing_date.month}/{number}.html"
    path_suffix = f"{bucket}{path_return}"
    path_out = f"/usr/local/share/minio/" + path_suffix
    os.makedirs(os.path.dirname(path_out), exist_ok=True)
    # copyfile(f"./{core}/scripts/sample/{file}", path_out)

    sample_path = f"./{core}/scripts/sample/{file}"
    with open(sample_path, "r", encoding="utf-8") as file:
        data = file.read()
    data = data.replace("{CODE_UPD}", str(number))
    number_row = 0

    for executer_state in executor_states:
        number_row += 1
        rows_for_all_task += rows_for_1_task.format(
            number_row, *executer_state.get_tuple_with_data_for_row_diadok_row[1:]
        )
        number_row += 1
        rows_for_all_task += rows_for_remenuration.format(
            number_row, *executer_state.get_tuple_with_data_for_row_diadok_row_remuneration[1:]
        )

    data = data.replace("{CODE_UPD}", str(number))
    data = data.replace("{DATE}", closing_date.date().strftime("%d.%m.%y"))
    data = data.replace("{DATE_OFFER}", offer_date)
    data = data.replace("{ACCEPTED_AT}", accepted_at)
    data = data.replace("{CLIENT_NAME}", requisites.owner.nameLegalEntity)
    data = data.replace(
        "{CLIENT_INN_KPP}",
        f"{requisites.innBank}/{requisites.kpp}",
    )
    data = data.replace("{CLIENT_ADDRESS}", requisites.legal_address)

    data = data.replace("{TABLE_CONTENT}", rows_for_all_task)

    data = data.replace("{FINISH}", RowForInvoice.get_str_with_format(total_price))
    data = data.replace("{SUM}", RowForInvoice.get_str_with_format(total_price - total_tax))
    data = data.replace("{TAX}", RowForInvoice.get_str_with_format(total_tax))
    data = data.replace(
        "{UDP_REQ}", f'№ {str(number)} п/п 1-{len(executor_states)} от {closing_date.date().strftime("%d.%m.%y")}'
    )

    pdfkit.from_string(
        data,
        os.path.splitext(path_out)[0] + ".pdf",
        options={
            "page-size": "Letter",
            "margin-top": "0.2in",
            "margin-right": "0.75in",
            "margin-bottom": "0.2in",
            "margin-left": "0.75in",
        },
    )

    path_out = os.path.splitext(path_out)[0] + ".pdf"
    path_return = os.path.splitext(path_return)[0] + ".pdf"
    server.getUrlForFile(path_out)

    return path_return


def invoice_creator_for_group_cd(
    *,
    executor_states,
    number,
    offer_date,
    accepted_at,
    total_price,
    total_tax,
    requisites,
    closing_date=None,
    date_start=None,
    date_stop=None,
):
    """
    Создание счёт-фактуры для группы организаций.
    @param total_tax: налоговая сумма
    @param total_price: общая стоимость
    @param executor_states: отклики Исполнителей
    @param number: Номер счет-фактуры
    @param offer_date: Дата Оферты
    @param closing_date: Дата закрытия документов
    """
    logger.info("Создание счет фактуры html")

    if closing_date is None:
        closing_date = datetime.now()

    file = "SAMPLE_INVOICE.html"

    rows_for_1_task = """
    <tr>
      <td style="border-right:2px solid #000"> </td>
      <td>{0}</td>
      <td>{1} Оплата услуг HOOPS Service за период {FORMATED_DATE}</td>
      <td> </td>
      <td>{2}</td>
      <td>{8}</td>
      <td>{3}</td>
      <td>{4}</td>
      <td>{5}</td>
      <td></td>
      <td>{9}</td>
      <td>{7}</td>
      <td>{6:.2f}</td>
      <td> </td>
      <td> </td>
      <td> </td>
    </tr>
    """
    rows_for_remenuration = """
    <tr>
      <td style="border-right:2px solid #000"> </td>
      <td>{0}</td>
      <td>{1} Вознаграждение за исполнение поручения за период {FORMATED_DATE}</td>
      <td> </td>
      <td>{2}</td>
      <td>{8}</td>
      <td>{3}</td>
      <td>{4}</td>
      <td>{5}</td>
      <td></td>
      <td>{9}</td>
      <td>{7}</td>
      <td>{6:.2f}</td>
      <td> </td>
      <td> </td>
      <td> </td>
    </tr>
    """

    rows_for_all_task = ""

    server = SH.minioDocuments()
    path_return = f"/closing_documents/{requisites.owner.id}/{closing_date.year}/{closing_date.month}/{number}.html"
    path_suffix = f"{bucket}{path_return}"
    path_out = f"/usr/local/share/minio/" + path_suffix
    os.makedirs(os.path.dirname(path_out), exist_ok=True)
    # copyfile(f"./{core}/scripts/sample/{file}", path_out)

    sample_path = f"./{core}/scripts/sample/{file}"
    with open(sample_path, "r", encoding="utf-8") as file:
        data = file.read()
    data = data.replace("{CODE_UPD}", str(number))
    number_row = 0

    # Формируем строку периода один раз (человекочитаемо на русском)
    def _to_datetime(value):
        """Приводит значение к datetime, если это строка — пробует распарсить ISO или %Y-%m-%d."""
        if isinstance(value, datetime):
            return value
        if isinstance(value, str):
            # Пробуем несколько форматов без жёстких зависимостей
            for fmt in ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
                try:
                    return datetime.strptime(value.split("+")[0], fmt)
                except Exception:
                    continue
        return None

    def _format_date_ru(dt: datetime) -> str:
        """Форматирует дату как '10 сентября 2025 года'."""
        months = {
            1: "января", 2: "февраля", 3: "марта", 4: "апреля", 5: "мая", 6: "июня",
            7: "июля", 8: "августа", 9: "сентября", 10: "октября", 11: "ноября", 12: "декабря",
        }
        return f"{dt.day} {months.get(dt.month, '')} {dt.year} года"

    def _format_period_ru(start_dt, end_dt) -> str:
        """Возвращает строку вида: 'с 10 сентября 2025 года по 13 сентября 2025 года'.
        Если даты отсутствуют или не распаршены — вернёт пустую строку."""
        sd = _to_datetime(start_dt)
        ed = _to_datetime(end_dt)
        if not sd or not ed:
            return ""
        return f"с {_format_date_ru(sd)} по {_format_date_ru(ed)}"

    formatted_period = _format_period_ru(date_start, date_stop)

    for executer_state in executor_states:
        number_row += 1
        rows_for_all_task += rows_for_1_task.format(
            number_row,
            *executer_state.get_tuple_with_data_for_group_cd[1:],
            FORMATED_DATE=formatted_period,
        )
        number_row += 1
        rows_for_all_task += rows_for_remenuration.format(
            number_row,
            *executer_state.get_tuple_with_data_for_group_cd_remuneration[1:],
            FORMATED_DATE=formatted_period,
        )

    data = data.replace("{CODE_UPD}", str(number))
    data = data.replace("{DATE}", closing_date.date().strftime("%d.%m.%y"))
    data = data.replace("{DATE_OFFER}", offer_date)
    data = data.replace("{ACCEPTED_AT}", accepted_at)
    data = data.replace("{CLIENT_NAME}", requisites.owner.nameLegalEntity)
    data = data.replace(
        "{CLIENT_INN_KPP}",
        f"{requisites.innBank}/{requisites.kpp}",
    )
    data = data.replace("{CLIENT_ADDRESS}", requisites.legal_address)

    data = data.replace("{TABLE_CONTENT}", rows_for_all_task)

    data = data.replace("{FINISH}", RowForInvoice.get_str_with_format(total_price))
    data = data.replace("{SUM}", RowForInvoice.get_str_with_format(total_price - total_tax))
    data = data.replace("{TAX}", RowForInvoice.get_str_with_format(total_tax))
    data = data.replace(
        "{UDP_REQ}", f'№ {str(number)} п/п 1-{len(executor_states)} от {closing_date.date().strftime("%d.%m.%y")}'
    )

    pdfkit.from_string(
        data,
        os.path.splitext(path_out)[0] + ".pdf",
        options={
            "page-size": "Letter",
            "margin-top": "0.2in",
            "margin-right": "0.75in",
            "margin-bottom": "0.2in",
            "margin-left": "0.75in",
        },
    )

    path_out = os.path.splitext(path_out)[0] + ".pdf"
    path_return = os.path.splitext(path_return)[0] + ".pdf"
    server.getUrlForFile(path_out)

    return path_return