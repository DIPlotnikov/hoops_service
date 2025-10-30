import logging
import os
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional

import pdfkit
from django.db.models import Count
from hotels.utils.invoice import round_money_4_5, round_value_for_hoops, round_volume_by_spec

from .nds_handler import calc_tax, calc_cost_without_tax
from ..config import bucket as bucket
from ..config import core as core
from ..models import Profession
from ..scripts import server_handler as SH
from .utils.date_utils import (
    format_period_ru
)

logger = logging.getLogger(__name__)


@dataclass
class RowForInvoice:
    """
    Данные для одной строки акта сдачи-приемки (договор-оферта).
    
    Класс содержит все необходимые данные для формирования трех типов строк в акте:
    1. "Оплата услуг HOOPS Service" - основная услуга с НДС 20%
    2. "Вознаграждение за исполнение поручения" - вознаграждение с НДС 20%
    3. "Услуги Исполнителей" - услуги исполнителей без НДС
    
    Столбцы акта сдачи-приемки:
    1. Номер по порядку
    2. Наименование работы(услуг) 
    3. Единица измерения
    4. Кол-во
    5. Цена (тариф) за единицу
    6. Стоимость работ (услуг) всего без налога
    7. Сумма налога
    8. Сумма с учетом налога
    """
    # Базовые данные
    hotel_name: str                    # Название гостиницы
    number: int                        # Номер строки (столбец 1)
    tasks: str                         # Номера заявок для наименования (столбец 2)
    
    # Объем работ
    volume: float                      # Количество часов (столбец 4)
    volume_str: str                    # Форматированное количество

    # Суммы для HOOPS (основная услуга)
    hoops_cost: float                  # Общая сумма HOOPS (столбец 8 для основной строки)
    hoops_cost_without_remuneration: float  # Сумма без вознаграждения (столбец 6 для основной строки)
    
    # Суммы для исполнителей (услуги исполнителей - без НДС)
    executer_cost: float               # Сумма услуг исполнителей (столбец 6 для строки исполнителей)

    # ОКЕИ коды (столбец 3)
    okei_code: str                     # Код единицы измерения
    okei_name: str                     # Название единицы измерения

    # Цены за единицу (столбец 5)
    rent_str: str                      # Цена основной услуги за час
    rent_for_executer: str             # Цена услуг исполнителей за час
    
    # НДС и налоги (столбец 7)
    hoops_without_tax_str: str         # HOOPS без НДС (столбец 6)
    tax_str: str                       # НДС основной услуги (столбец 7)
    nds: str                          # Ставка НДС
    
    # Данные вознаграждения
    remuneration: float                # Сумма вознаграждения (столбец 8 для строки вознаграждения)
    remuneration_without_tax_str: str  # Вознаграждение без НДС (столбец 6 для строки вознаграждения)
    remuneration_tax_str: str         # НДС вознаграждения (столбец 7 для строки вознаграждения)
    remuneration_rent_str: str        # Цена вознаграждения за единицу (столбец 5 для строки вознаграждения)
    
    # Дополнительные расчеты для основной услуги
    hoops_cost_without_remuneration_without_tax_str: str  # Основная услуга без НДС (столбец 6)
    hoops_cost_without_remuneration_tax_str: str         # НДС основной услуги (столбец 7)
    hoops_cost_without_remuneration_rent_str: str        # Цена основной услуги за единицу (столбец 5)

    # Дополнительные поля (опциональны для совместимости с одиночным режимом)
    date_start: Optional[str] = ""     # Дата начала периода
    date_end: Optional[str] = ""       # Дата окончания периода

    @property
    def text_for_hoops(self):
        """
        Текст для основной строки акта: "Оплата услуг HOOPS Service"
        Используется в столбце 2 (Наименование работы(услуг))
        """
        return f"Стоимость Услуг HOOPS Service по заявкам {self.tasks}"

    @property
    def text_for_remuneration(self):
        """
        Текст для строки вознаграждения: "Вознаграждение за исполнение поручения"
        Используется в столбце 2 (Наименование работы(услуг))
        """
        return f"Вознаграждение за исполнение поручения по заявкам {self.tasks}"

    @property
    def text_for_executer(self):
        """
        Текст для строки услуг исполнителей: "Услуги Исполнителей"
        Используется в столбце 2 (Наименование работы(услуг))
        """
        return (
            "Оплата HOOPS для выплаты исполнителям согласно раздела 4 договора оферты от {DATE_OFFER} за оказанные услуги по заявкам  "
            + self.tasks
        )

    @property
    def text_for_hoops_gcd(self):
        return (f"{self.hotel_name} "
                f"Оплата Услуг HOOPS Service за период "
                f"{format_period_ru(self.date_start, self.date_end)}")

    @property
    def text_for_remuneration_gcd(self):
        return (f"{self.hotel_name} "
                f"Вознаграждение за исполнение поручения за период "
                f"{format_period_ru(self.date_start, self.date_end)}")

    @property
    def text_for_executer_gcd(self):
        return (f"{self.hotel_name} "
                f"Оплата HOOPS для выплаты исполнителям за период "
                f"{format_period_ru(self.date_start, self.date_end)}")


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
    def get_tuple_with_data_for_row_bill_hoops_group_cd(self):
        """
        Кортеж данных для счета - строка для оплаты услуг HOOPS
        """
        volume = '1'
        return (
            self.text_for_hoops_gcd,
            self.hoops_cost_without_remuneration,
            volume,
            self.hoops_cost_without_remuneration,
        )


    @property
    def get_tuple_with_data_for_row_bill_hoops_remuneration_for_group_cd(self):
        """
        Кортеж данных для счета - строка для оплаты услуг HOOPS
        """
        volume = '1'
        return (self.text_for_remuneration_gcd,
                self.remuneration,
                volume,
                self.remuneration)

    @property
    def get_tuple_with_data_for_row_bill_executer_for_group_cd(self):
        """
        Кортеж данных для счета - строка для оплаты услуг Исполнителей
        """
        volume = '1'
        return (self.text_for_executer_gcd,
                self.executer_cost,
                volume,
                self.executer_cost)

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
        Данные для основной строки акта: "Оплата услуг HOOPS Service"
        
        Возвращает кортеж для заполнения строки акта:
        - tasks: номера заявок (столбец 2)
        - volume_str: количество часов (столбец 4) 
        - hoops_cost_without_remuneration_rent_str: цена за час (столбец 5)
        - hoops_cost_without_remuneration_without_tax_str: сумма без НДС (столбец 6)
        - hoops_cost_without_remuneration_tax_str: НДС (столбец 7)
        - hoops_cost_without_remuneration: сумма с НДС (столбец 8)
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
        Данные для строки вознаграждения: "Вознаграждение за исполнение поручения"
        
        Возвращает кортеж для заполнения строки акта:
        - remuneration_rent_str: цена за час (столбец 5)
        - remuneration_without_tax_str: сумма без НДС (столбец 6)
        - remuneration_tax_str: НДС (столбец 7)
        - remuneration: сумма с НДС (столбец 8)
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
        Данные для строки услуг исполнителей: "Услуги Исполнителей"
        
        Возвращает кортеж для заполнения строки акта:
        - rent_for_executer: цена за час (столбец 5)
        - executer_cost: сумма без НДС (столбец 6) - услуги исполнителей без НДС
        - okei_name: единица измерения (столбец 3)
        """
        return self.rent_for_executer, "{:.2f}".format(self.executer_cost), self.okei_name

    @property
    def get_tuple_with_data_for_row_act_first_row_gcd(self) -> tuple:
        """
        Данные для основной строки группового акта: "Оплата услуг HOOPS Service"
        
        Для групповых документов количество всегда = 1 (шт)
        Возвращает кортеж для заполнения строки акта:
        - hotel_name: название гостиницы (столбец 2)
        - volume: количество = 1 (столбец 4)
        - hoops_cost_without_remuneration_without_tax_str: сумма без НДС (столбец 6)
        - hoops_cost_without_remuneration_without_tax_str: цена за единицу (столбец 5)
        - hoops_cost_without_remuneration_tax_str: НДС (столбец 7)
        - hoops_cost_without_remuneration: сумма с НДС (столбец 8)
        """
        volume = '1'
        return (
            self.hotel_name,
            volume,
            self.hoops_cost_without_remuneration_without_tax_str,
            self.hoops_cost_without_remuneration_without_tax_str,
            self.hoops_cost_without_remuneration_tax_str,
            self.hoops_cost_without_remuneration,
        )

    @property
    def get_tuple_with_data_for_row_act_second_row_gcd(self) -> tuple:
        """
        Данные для строки услуг исполнителей в групповом акте: "Услуги Исполнителей"
        
        Возвращает кортеж для заполнения строки акта:
        - executer_cost: сумма без НДС (столбец 6) - услуги исполнителей без НДС
        - executer_cost: цена за единицу (столбец 5) - для групповых документов цена = сумме
        - okei_name: единица измерения = "шт" (столбец 3)
        """
        okei_name = 'шт'
        return (
            "{:.2f}".format(self.executer_cost), # стоимость работ всего (без налога)
            "{:.2f}".format(self.executer_cost),
            okei_name
        )

    @property
    def get_tuple_with_data_for_row_act_remenuration_gcd(self) -> tuple:
        """
        Данные для строки вознаграждения в групповом акте: "Вознаграждение за исполнение поручения"
        
        Возвращает кортеж для заполнения строки акта:
        - remuneration_without_tax_str: сумма без НДС (столбец 6)
        - remuneration_without_tax_str: цена за единицу (столбец 5) - для групповых документов цена = сумме без НДС
        - remuneration_tax_str: НДС (столбец 7)
        - remuneration: сумма с НДС (столбец 8)
        """
        return (
            self.remuneration_without_tax_str,
            self.remuneration_without_tax_str,
            self.remuneration_tax_str,
            self.remuneration,
        )




def format_executers_states_to_invoice_format(
        executor_states,
        nds=20.0,
        remuneration_percent=0,
        hotel=None,
        date_start=None,
        date_end=None,
) -> tuple:
    """
    Формирование данных для акта сдачи-приемки (договор-оферта) из статусов исполнителей.
    
    Функция группирует статусы исполнителей по профессиям и ставкам, рассчитывает суммы
    для трех типов строк в акте:
    1. "Оплата услуг HOOPS Service" - основная услуга с НДС 20%
    2. "Вознаграждение за исполнение поручения" - вознаграждение с НДС 20% 
    3. "Услуги Исполнителей" - услуги исполнителей без НДС
    
    Столбцы акта сдачи-приемки:
    - Номер по порядку (1)
    - Наименование работы(услуг) (2) 
    - Единица измерения (3)
    - Кол-во (4)
    - Цена (тариф) за единицу (5)
    - Стоимость работ (услуг) всего без налога (6)
    - Сумма налога (7)
    - Сумма с учетом налога (8)
    
    @param executor_states: Статусы исполнителей для обработки
    @param nds: ставка НДС (по умолчанию 20.0%)
    @param remuneration_percent: процент вознаграждения от суммы HOOPS
    @param hotel: объект гостиницы для получения названия
    @param date_start: дата начала периода
    @param date_end: дата окончания периода
    @return: кортеж (список RowForInvoice, общая_сумма_hoops, общая_сумма_исполнителей, общий_ндс)
    """
    # Счетчик строк для нумерации в акте
    number_row = 1
    # Итоговые суммы для акта
    total_price = 0.0          # Общая сумма к оплате (столбец 8)
    total_sum_for_executer = 0.0  # Сумма услуг исполнителей без НДС
    total_tax = 0.0            # Общий НДС (столбец 7)
    
    # Результирующий список строк для акта
    res_hoops = []
    
    # ОБРАБОТКА ПО ПРОФЕССИЯМ
    # Группируем статусы по профессиям (официант, бармен, хостес и т.д.)
    # Каждая профессия имеет свой ОКЕИ код для единиц измерения
    for name, okei in Profession.okei.items():
        # Получаем все статусы исполнителей текущей профессии
        current_executer_states = executor_states.filter(task__profession__numerate=name)
        
        # ГРУППИРОВКА ПО СТАВКАМ
        # В рамках одной профессии могут быть разные ставки оплаты
        # Группируем по уникальным ставкам (rent) для корректного расчета
        list_of_distinct_rent = set(
            current_executer_states.values_list("task__rent", flat=True).annotate(count=Count("task__rent"))
        )

        # ОБРАБОТКА КАЖДОЙ ГРУППЫ СТАВОК
        for rent in list_of_distinct_rent:
            # Накопительные переменные для текущей группы ставок
            worktime_in_current_tasks_hours = 0  # Общее время работы (столбец 4)
            hoops_cost = 0.0                    # Сумма для HOOPS (основная услуга)
            executer_cost = 0.0                 # Сумма для исполнителей (услуги исполнителей)
            tasks = []                          # Список номеров заявок

            # АГРЕГАЦИЯ ДАННЫХ ПО СТАТУСАМ
            # Проходим по всем статусам с текущей ставкой
            for executor_state in current_executer_states.filter(task__rent=rent):
                # ПРОВЕРКА ЗАВЕРШЕННОСТИ РАБОТЫ
                # Статус должен быть "STOP" - работа завершена
                if executor_state.status != "STOP":
                    raise ValueError(
                        f"В заявке {executor_state.task.id} у "
                        f"{executor_state.task.manager.hotel} исполнитель #{executor_state.executer.id} "
                        f"{executor_state.executer.middle_name} {executor_state.executer.first_name} "
                        f"{executor_state.executer.second_name} не закончил работать!"
                    )
                
                # ПРОВЕРКА ФИНАНСОВОЙ ПРОВЕРКИ
                # Статус должен быть проверен в финансах
                if not executor_state.is_check_in_finance:
                    continue

                # НАКОПЛЕНИЕ ДАННЫХ
                # Суммируем время работы, суммы для HOOPS и исполнителей
                worktime_in_current_tasks_hours += executor_state.get_work_time_in_hours # объем. Округляем и больше не трогаем. todo еще нужно добавить округление.
                tasks.append(executor_state.task.id)

            # ОБРАБОТКА НЕНУЛЕВЫХ РЕЗУЛЬТАТОВ
            if worktime_in_current_tasks_hours:

                # считаем цены за единицу
                # процент для оплаты услуг компании
                prof_percent = Decimal(str(executor_state.task.profession.percent))
                # процент для оплаты вознаграждения
                remuneration_percent_decimal = Decimal(str(remuneration_percent))
                # Полная оплата за заявку
                rent_decimal = Decimal(str(rent))
                
                
                # Цена услуг исполнителей за единицу
                rent_for_executer = rent_decimal - (rent_decimal * prof_percent / 100)
                # Стоимость услуги HOOPS за единицу
                rent_for_hoops = (rent_decimal - rent_for_executer) * remuneration_percent_decimal / 100
                # Вознаграждение за единицу
                remuneration_for_executer = rent_decimal - rent_for_hoops - rent_for_executer

                is_correct_sum = bool(rent_for_executer + rent_for_hoops + remuneration_for_executer == rent_decimal) # todo возможно нужно логировать.

                # Округление стоимости за единицу
                rent_for_executer = round_money_4_5(rent_for_executer)
                rent_for_hoops = round_money_4_5(rent_for_hoops)
                remuneration_for_executer = round_money_4_5(remuneration_for_executer)
                
                # ОКРУГЛЕНИЕ ВРЕМЕНИ РАБОТЫ
                # Применяем специальное округление для HOOPS (объем работ)
                worktime_in_current_tasks_hours = round_volume_by_spec(worktime_in_current_tasks_hours)
                
                hoops_cost = rent_for_hoops * worktime_in_current_tasks_hours
                hoops_remuneration = remuneration_for_executer * worktime_in_current_tasks_hours
                executer_cost = rent_for_executer * worktime_in_current_tasks_hours

                # Округление полной стоимости
                hoops_cost = round_money_4_5(hoops_cost)
                hoops_remuneration = round_money_4_5(hoops_remuneration)
                executer_cost = round_money_4_5(executer_cost)

                # Расчет НДС
                nds_hoops = calc_tax(hoops_cost, nds)
                nds_remuneration = calc_tax(hoops_remuneration, nds)
                # Не облагается НДС
                nds_executer = 0

                # Расчет стоимости без НДС
                hoops_cost_without_tax = hoops_cost - nds_hoops
                hoops_remuneration_without_tax = hoops_remuneration - nds_remuneration
                executer_cost_without_tax = executer_cost - nds_executer

                # Округление полной стоимости без НДС
                hoops_cost_without_tax = round_money_4_5(hoops_cost_without_tax)
                hoops_remuneration_without_tax = round_money_4_5(hoops_remuneration_without_tax)
                executer_cost_without_tax = round_money_4_5(executer_cost_without_tax)


                # СОЗДАНИЕ ОБЪЕКТА СТРОКИ ДЛЯ АКТА
                res_hoops.append(
                    RowForInvoice(
                        # Базовые данные
                        hotel_name=hotel.nameHotel if hotel else '',  # Название гостиницы
                        number=number_row,                            # Номер строки (столбец 1)
                        tasks=", ".join(str(x) for x in set(tasks)), # Номера заявок
                        
                        # Объем работ - приводим к float и применяем округление объёмов
                        volume=float(round_volume_by_spec(worktime_in_current_tasks_hours)),  # Количество часов (столбец 4)
                        volume_str=RowForInvoice.get_str_with_format(round_volume_by_spec(worktime_in_current_tasks_hours)),
                        
                        # Суммы для HOOPS (основная услуга) - приводим к float
                        hoops_cost=float(hoops_cost + hoops_remuneration),             # Общая сумма HOOPS
                        hoops_cost_without_remuneration=float(hoops_cost),  # Без вознаграждения
                        
                        # Основная услуга без НДС (столбец 6 для основной строки) - строки
                        hoops_cost_without_remuneration_without_tax_str=hoops_cost_without_tax,
                        # НДС основной услуги (столбец 7 для основной строки) - строки
                        hoops_cost_without_remuneration_tax_str=nds_hoops,
                        
                        # Суммы для исполнителей (услуги исполнителей - без НДС) - float
                        executer_cost=float(executer_cost),      # Сумма услуг исполнителей
                        
                        # ОКЕИ коды (столбец 3) - строки
                        okei_code=okei.get("code"),                  # Код единицы измерения
                        okei_name=okei.get("num"),                   # Название единицы измерения
                        
                        # Цены за единицу (столбец 5) - строки
                        rent_str=rent_for_hoops,  # Цена основной услуги
                        rent_for_executer=rent_for_executer,  # Цена услуг исполнителей
                        
                        # Дополнительные расчеты для отчетов - строки
                        hoops_without_tax_str=hoops_cost_without_tax,  # HOOPS без НДС
                        tax_str=nds_hoops,  # НДС основной услуги
                        nds=str(nds),                               # Ставка НДС
                        
                        # Данные вознаграждения - приводим к правильным типам
                        remuneration=float(hoops_remuneration),          # Сумма вознаграждения
                        remuneration_without_tax_str=hoops_remuneration_without_tax,  # Без НДС (столбец 6)
                        remuneration_tax_str=nds_remuneration, # НДС вознаграждения (столбец 7)
                        remuneration_rent_str=remuneration_for_executer, # Цена за единицу (столбец 5)
                        hoops_cost_without_remuneration_rent_str=rent_for_hoops,  # Цена основной услуги
                        
                        # Период - строки или None
                        date_start=date_start if date_start else None,
                        date_end=date_end if date_end else None,
                    )
                )

                # НАКОПЛЕНИЕ ИТОГОВЫХ СУММ
                total_price += float(hoops_cost + hoops_remuneration)                    # Общая сумма к оплате
                total_sum_for_executer += float(executer_cost)      # Сумма услуг исполнителей
                number_row += 1                              # Следующий номер строки
                total_tax += float(nds_hoops + nds_remuneration)   # Общий НДС

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
      <td style=\"border-right:2px solid #000\"><div> </div></td>
      <td><div>{0}</div></td>
      <td><div>Стоимость Услуг HOOPS Service по заявкам № {1}</div></td>
      <td><div> </div></td>
      <td><div>{2}</div></td>
      <td><div>{8}</div></td>
      <td><div>{3}</div></td>
      <td><div>{4}</div></td>
      <td><div>{5}</div></td>
      <td><div></div></td>
      <td><div>{9}</div></td>
      <td><div>{7}</div></td>
      <td><div>{6:.2f}</div></td>
      <td><div> </div></td>
      <td><div> </div></td>
      <td><div> </div></td>
    </tr>
    """
    rows_for_remenuration = """
    <tr>
      <td style=\"border-right:2px solid #000\"><div> </div></td>
      <td><div>{0}</div></td>
      <td><div>Вознаграждение за исполнение поручения по заявкам № {1}</div></td>
      <td><div> </div></td>
      <td><div>{2}</div></td>
      <td><div>{8}</div></td>
      <td><div>{3}</div></td>
      <td><div>{4}</div></td>
      <td><div>{5}</div></td>
      <td><div></div></td>
      <td><div>{9}</div></td>
      <td><div>{7}</div></td>
      <td><div>{6:.2f}</div></td>
      <td><div> </div></td>
      <td><div> </div></td>
      <td><div> </div></td>
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
            "encoding": "UTF-8",
            "print-media-type": None,
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

    file = "SAMPLE_INVOICE_GCD.html"

    rows_for_1_task = """
    <tr>
      <td style=\"border-right:2px solid #000\"><div> </div></td>
      <td><div>{0}</div></td>
      <td><div>{1} Оплата услуг HOOPS Service за период {FORMATED_DATE}</div></td>
      <td><div> </div></td>
      <td><div>{2}</div></td>
      <td><div>{8}</div></td>
      <td><div>{3}</div></td>
      <td><div>{4}</div></td>
      <td><div>{5}</div></td>
      <td><div></div></td>
      <td><div>{9}</div></td>
      <td><div>{7}</div></td>
      <td><div>{6:.2f}</div></td>
      <td><div> </div></td>
      <td><div> </div></td>
      <td><div> </div></td>
    </tr>
    """
    rows_for_remenuration = """
    <tr>
      <td style=\"border-right:2px solid #000\"><div> </div></td>
      <td><div>{0}</div></td>
      <td><div>{1} Вознаграждение за исполнение поручения за период {FORMATED_DATE}</div></td>
      <td><div> </div></td>
      <td><div>{2}</div></td>
      <td><div>{8}</div></td>
      <td><div>{3}</div></td>
      <td><div>{4}</div></td>
      <td><div>{5}</div></td>
      <td><div></div></td>
      <td><div>{9}</div></td>
      <td><div>{7}</div></td>
      <td><div>{6:.2f}</div></td>
      <td><div> </div></td>
      <td><div> </div></td>
      <td><div> </div></td>
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

    formatted_period = format_period_ru(date_start, date_stop)

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
            "page-size": "A4",
            "orientation": "Landscape",
            "margin-top": "2cm",
            "margin-right": "2cm",
            "margin-bottom": "2cm",
            "margin-left": "2cm",
            "encoding": "UTF-8",
            "print-media-type": None,
        },
    )

    path_out = os.path.splitext(path_out)[0] + ".pdf"
    path_return = os.path.splitext(path_return)[0] + ".pdf"
    server.getUrlForFile(path_out)

    return path_return