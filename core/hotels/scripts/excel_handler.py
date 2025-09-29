import gc
import io
import os
import zipfile
from datetime import datetime, timedelta
from shutil import copyfile
from uuid import uuid4

# Dependencies overview:
# - openpyxl: core library for reading/writing/styling .xlsx files.
# - django.db.models (Count, Q): used for annotated queries in admin reports.
# - requests: imported but not used in this module (kept for parity/future use).
# - Images (stamp/signature) and .xlsx templates are expected under `./{core}/scripts/sample`.
import openpyxl
import requests
from django.db.models import Count, Q
from openpyxl.styles import Alignment, Font
from openpyxl.styles.borders import Border, Side
from ..scripts.reports.round_func import round_service_rate

from ..config import bucket as bucket
from ..config import core as core
from ..scripts import server_handler as SH


class ReportBuilder(object):
    """
    Строитель Excel-отчетов на основе шаблонов.

    Что делает:
    - Загружает .xlsx шаблон из каталога `./{core}/scripts/sample` и сохраняет итоговый файл
      в смонтированное файловое хранилище `/usr/local/share/minio/{bucket}`.
    - Заполняет листы (по типу отчета) данными из задач/исполнителей/отелей, применяет стили и
      формулы Excel (как строковые выражения, вычисляются самим Excel при открытии).

    Типы данных и форматы Excel:
    - Денежные суммы: числа (float/Decimal) с number_format "#,##0.00₽". Важно не записывать суммы строками,
      иначе Excel не будет корректно суммировать.
    - Даты: объекты date/datetime с number_format "DD.MM.YYYY".
    - Время: объекты time/datetime с number_format вида "HH:MM" в текущем коде. ВНИМАНИЕ: в Excel символы для минут — 'mm'.
      Использование 'MM' соответствует месяцу. Оставлено без изменения для сохранения текущего поведения (см. TODO в методах).
    - Часы работы: обычно десятичные часы (float) с number_format "0.0" или "0.00".

    Безопасность/окружение:
    - Конструктор перезаписывает файл результата, копируя шаблон. Директории создаются при необходимости.
    - Путь сохранения задается аргументом `path` и интерпретируется относительно `/usr/local/share/minio/{bucket}`.

    """

    dict_sample_names = {
        "STANDART_REPORT": "STANDART_REPORT.xlsx",
        "STANDART": "STANDART_REPORT.xlsx",
        "MANAGEMENT_REPORT": "MANAGEMENT_REPORT.xlsx",
        "EXECUTER_STANDART_REPORT": "EXECUTER_STANDART_REPORT.xlsx",
        "EXECUTER_STANDART": "EXECUTER_STANDART_REPORT.xlsx",
        "DIFFERENCE_REPORT": "CORRECTION.xlsx",
        "EXECUTER_DIFFERENCE_REPORT": "CORRECTION.xlsx",
        "BY_TYPE": "BY_TYPE.xlsx",
        "EXECUTER_BY_TYPE": "EXECUTER_BY_TYPE.xlsx",
        "EXECUTER_FINANCIAL": "EXECUTER_FINANCIAL.xlsx",
        "MANAGERS_REPORT": "MANAGERS_REPORT.xlsx",
        "ACTIVITY": "ACTIVITY.xlsx",
        "COMPARATIVE": "COMPARATIVE.xlsx",
        "LIST_EXECUTERS": "clear.xlsx",
        "PAYMENT_FOR_COORDINATORS": "PAYMENT_FOR_COORDINATORS.xlsx",
        "ADMIN_STATISTIC": "ADMIN_STATISTIC.xlsx",
        "EXECUTORS_LIST": "EXECUTORS_LIST.xlsx",
    }

    strings_for_footer = [
        "Дата создания отчета: {0}",
        "Отчет является Данными статистики",
        "Отчет составлен Программой HOOPS Service",
        "https://hoopsservice.ru",
        'Правообладатель ООО "Гостиничные ресурсы"',
        "ИНН/КПП 9703086470/770301001",
    ]

    # Общая тонкая рамка для ячеек (используется повсеместно для визуального отделения).
    thin_border = Border(
        left=Side(style="thin"), right=Side(style="thin"), top=Side(style="thin"), bottom=Side(style="thin")
    )
    # Номер первой строки с табличными данными (обычно после шапки/заголовков листа).
    first_text = 3

    def __init__(self, *, path: str, type_report: str, time_zone_offset: int = -180):
        """
        Инициализация строителя отчетов.

        Аргументы:
        - path: относительный путь сохранения файла в MinIO (например: 'hotels/reports/xxx.xlsx').
        - type_report: ключ типа отчета, соответствующий шаблону в dict_sample_names.
        - time_zone_offset: смещение таймзоны в минутах относительно UTC (по умолчанию -180, т.е. UTC+3).

        Примечания:
        - При инициализации происходит копирование шаблона в целевой файл, затем открывается workbook.
        - Для EXECUTORS_LIST предусмотрен ранний выход (видимо, шаблон обрабатывается иначе).
        """
        self.path = path
        self.type_report = type_report
        if type_report == "EXECUTORS_LIST":
            return
        self.time_zone_offset = time_zone_offset

        self.sample_name = self.dict_sample_names.get(type_report)

        # Абсолютный путь до каталога хранения (MinIO смонтирован в ФС контейнера/сервера)
        self.__path_storage_prefix = f"/usr/local/share/minio/{bucket}"
        # Путь до каталога с шаблонами XLSX и изображениями печати/подписи
        self.__path_sample_prefix = f"./{core}/scripts/sample"

        if os.path.isfile(os.path.join(self.__path_storage_prefix, self.path)):
            os.remove(os.path.join(self.__path_storage_prefix, self.path))
        os.makedirs(os.path.dirname(os.path.join(self.__path_storage_prefix, self.path)), exist_ok=True)
        copyfile(
            os.path.join(self.__path_sample_prefix, self.sample_name),
            os.path.join(self.__path_storage_prefix, self.path),
        )
        # Загружаем workbook из только что скопированного файла-шаблона.
        # Важно: openpyxl сам определяет типы ячеек при записи.
        self.wb = openpyxl.load_workbook(filename=self.path_storage)

    @property
    def path_storage(self):
        # Полный путь к целевому XLSX в storage (MinIO).
        return os.path.join(self.__path_storage_prefix, self.path)

    @property
    def path_sample(self):
        if self.sample_name:
            return os.path.join(self.__path_sample_prefix, self.sample_name)

    def pre_build(self):
        """
        Переинициализация файла отчета из шаблона (если нужно пересоздать документ).
        Удаляет существующий, создает директорию и копирует шаблон.
        """
        if os.path.isfile(self.path_storage):
            os.remove(self.path_storage)
        os.makedirs(os.path.dirname(self.path_storage), exist_ok=True)
        copyfile(self.path_sample, self.path_storage)

    @staticmethod
    def get_time_with_offset_with_offset(datetime_current: datetime, time_zone_offset=180) -> datetime:
        """
        Перевод времени из UTC в локальное по временному смещению (статическая версия).

        ВНИМАНИЕ: двойное "with_offset" в имени — вероятно, опечатка. Оставлено для совместимости.

        Аргументы:
        - datetime_current: момент времени в UTC.
        - time_zone_offset: смещение в минутах (например, 180 для UTC+3, либо -180 если храните локаль иначе).
        """
        return datetime_current - timedelta(minutes=time_zone_offset)

    def get_time_with_offset(self, datetime_current: datetime) -> datetime:
        """
        Перевод времени из UTC в локальное по временному смещению.

        Использует self.time_zone_offset, установленный в конструкторе.
        """
        return datetime_current - timedelta(minutes=self.time_zone_offset)

    def set_data(
        self,
        *,
        sheet,
        address,
        text,
        alignment=None,
        number_format=None,
        border=False,
        fill=None,
        italic=False,
        bold=False,
        size="12",
        indent=0,
    ):
        """
        Универсальная точка записи данных и стилей в ячейку.

        Параметры:
        - sheet: объект листа openpyxl (Workbook["SheetName"]).
        - address: адрес ячейки в A1-нотации (например, "B3").
        - text: значение для записи. Может быть числом (int/float/Decimal), датой/временем (datetime/date/time) или строкой.
          Если это строка, начинающаяся с '=', Excel воспримет как формулу.
        - alignment: выравнивание по горизонтали ('left'/'center'/'right').
        - number_format: строка формата Excel (например, "#,##0.00₽", "DD.MM.YYYY", "0.00").
          ВНИМАНИЕ: для часов в Excel минутам соответствует 'mm', а не 'MM'.
        - border: если True — применить тонкую границу thin_border ко всем сторонам.
        - fill: объект заливки openpyxl.styles.PatternFill (используется выборочно).
        - italic/bold/size/indent: параметры шрифта/отступа.

        Замечания по типам:
        - Для корректных сумм/формул избегайте записи чисел как строк.
        - Для дат/времени записывайте объекты date/time/datetime, плюс указывайте number_format.
        """
        # Применяем округление к денежным значениям (если это число и формат валютный)
        try:
            is_formula = isinstance(text, str) and text.startswith("=")
            is_number = isinstance(text, (int, float))
            is_currency = bool(number_format) and (
                "₽" in str(number_format) or "#,##0.00" in str(number_format)
            )
            if (not is_formula) and is_number and is_currency:
                text = round_service_rate(float(text))
        except Exception:
            # В случае любых проблем с приведением типов — записываем как есть
            pass

        sheet[address] = text

        if alignment:
            sheet[address].alignment = Alignment(horizontal=alignment, indent=indent)
        if border:
            sheet[address].border = self.thin_border
        if number_format:
            sheet[address].number_format = number_format
        if fill:
            sheet[address].fill = fill
        sheet[address].font = Font(italic=italic, bold=bold, size=size)

    def _round_formula(self, expr: str) -> str:
        """
        Оборачивает формулу Excel в ROUND(..., 2), если это формула и ещё не округлена.
        Принимает строку вида "=..." и возвращает "=ROUND(..., 2)".
        """
        if isinstance(expr, str) and expr.startswith("="):
            inner = expr[1:]
            if inner.strip().upper().startswith("ROUND("):
                return expr
            return f"=ROUND({inner}, 2)"
        return expr

    def footer(self, *, sheet, row: int) -> int:
        """
        Добавление нижнего блока с информацией о правообладателе/дате.

        :param sheet: страница редактирования
        :param row: с какой строки начинать
        :return: следующая доступная строка после вставленного футера
        """
        row += 2
        date_now = datetime.now().date().strftime("%d.%m.%y")
        for string_footer in self.strings_for_footer:
            self.set_data(text=string_footer.format(date_now), sheet=sheet, address=f"A{row}", alignment="left")
            row += 1
        return row

    def stamp_and_signature(self, *, anchor: str, sheet):
        """
        Проставляет изображение печати и подписи генерального директора на листе.

        :param anchor: адрес привязки верхнего левого угла изображения (например, "A1").
        :param sheet: объект листа openpyxl.

        Примечания:
        - Изображения "stamp.png" и "signature.png" ожидаются в каталоге sample.
        - Размеры масштабируются (подпись — 80%).
        """

        img = openpyxl.drawing.image.Image(f"./{core}/scripts/sample/stamp.png")
        img.anchor = anchor
        img.width = 170
        img.height = 170
        sheet.add_image(img)

        img = openpyxl.drawing.image.Image(f"./{core}/scripts/sample/signature.png")
        img.anchor = anchor
        img.width = img.width * 0.8
        img.height = img.height * 0.8

        sheet.add_image(img)

    def create_manager_standart_report(self, *, tasks=None, executers=None, period="", remuneration=10):
        """
        Формирует стандартный отчет менеджера на листе "Стандартный отчёт".

        Входные данные:
        - tasks: QuerySet/iterable задач. Каждая задача должна иметь:
          - manager.hotel.nameHotel (строка), manager.fullname (строка)
          - profession.description (строка)
          - start_at (datetime, UTC)
          - rent (число, ставка с НДС)
          - additional? (опционально: .datetime, .description)
          - properties full_pay_real (фактическая сумма), full_work_time_real (фактические часы)
          - task.executers: итерация по состояниям исполнителей, у каждого:
            - executer.full_name (строка)
            - start_at_real_or_task / stop_at_real_or_task (datetime)
            - get_work_time_in_hours (float, часы)
            - get_work_time_in_hours_real (float|0|None, фактические часы)
            - get_sum_for_hoops (float), get_sum_for_hoops_without_remuneration (float)
            - get_sum_for_pay (float), get_sum_full (float)
            - problem (строка)
            - status (строка)
        - executers: не используется в текущей реализации.
        - period: строковое описание периода (выводится в шапке).
        - remuneration: % вознаграждения (по умолчанию 10) для вычисления вознаграждения HOOPS.

        Вывод:
        - Заполняет таблицу по каждой связке задача-исполнитель и итоги.

        ВАЖНО/TODO:
        - В ячейки F/G с временем установлен number_format "HH:MM"; в Excel для минут надо использовать 'mm'.
          Сейчас оставлено как есть для сохранения текущего вида/поведения.
        - На строках заголовка есть двойная запись в B1 (имя отеля, затем период), что перезаписывает значение.
          См. строки ниже с TODO.
        """
        formulas = {
            "count_hours": r'=IF(OR(E{0}=0,F{0}=0),0,IF(F{0}>=E{0},(F{0}-E{0})*24,(("24:00"-E{0})+(F{0}-"00:00"))*24))',
            "itog_once": "=ROUND(E{0}*H{0}, 2)",
            "itog_all_hours": "=SUM(H{0}:H{1})",
            "itog_all_rub": "=ROUND(SUM(I{0}:I{1}), 2)",
            "for_executers": "=ROUND(I{0}-J{0}-K{0}, 2)",
            "for_hoops": "=ROUND(I{0}*(100-{1})/100, 2)",
        }
        flag_additional = False
        sheet = self.wb["Стандартный отчёт"]
        now = datetime.now()
        # заголовок ИМЯ ГОСТИНИЦЫ
        self.set_data(text=tasks[0].manager.hotel.nameHotel, sheet=sheet, address=f"B1", alignment="center")
        # ПЕРИОД отчета
        # TODO: Здесь period записывается в ту же ячейку B1 и перетирает имя отеля.
        # Вероятно, планировалось записать period в A1 или другую ячейку заголовка.
        self.set_data(text=period, sheet=sheet, address=f"B1", alignment="center")
        # работа с задачами
        first_text = 3
        row = first_text
        # сумма комиссий HOOPS
        summ_for_hoops = 0
        # сумма фактичеких комиссий HOOPS
        summ_for_hoops_real = 0

        # сумма оплаты
        all_pay = 0
        # сумма часов
        all_hours = 0
        for_remuneration_all = 0
        for_remuneration_all_real = 0
        for task in tasks:
            for executer in task.executers.all():

                summ_for_hoops += executer.get_sum_for_hoops_without_remuneration
                for_hoops_full = executer.get_sum_for_hoops
                for_remuneration = for_hoops_full / 100 * remuneration
                for_hoops = for_hoops_full - for_remuneration
                for_remuneration_all += for_remuneration
                if executer.get_work_time_in_hours_real:
                    summ_for_hoops_real += executer.get_sum_for_hoops_without_remuneration
                    for_remuneration_all_real += for_remuneration
                # ФИО Исполнителя
                self.set_data(
                    text=executer.executer.full_name, address=f"A{row}", sheet=sheet, border=True, alignment="left"
                )
                # наименование профессии в заявке
                self.set_data(text=task.finish_name, address=f"B{row}", sheet=sheet, border=True)
                # описание профессии
                self.set_data(text=task.profession.description, address=f"C{row}", sheet=sheet, border=True)
                # дата старта Заявки
                self.set_data(
                    text=self.get_time_with_offset(task.start_at).date(),
                    address=f"D{row}",
                    sheet=sheet,
                    number_format="DD.MM.YYYY",
                    border=True,
                )
                # ставка Заявки
                self.set_data(text=task.rent, address=f"E{row}", sheet=sheet, number_format="#,##0.00₽", border=True)
                # время старта Исполнителя в Заявке
                self.set_data(
                    text=self.get_time_with_offset(executer.start_at_real_or_task).time(),
                    address=f"F{row}",
                    sheet=sheet,
                    number_format="HH:MM",  # см. TODO по Excel: для минут — 'mm'
                    border=True,
                )
                # время стопа Исполнителя в Заявке
                self.set_data(
                    text=self.get_time_with_offset(executer.stop_at_real_or_task).time(),
                    address=f"G{row}",
                    sheet=sheet,
                    number_format="HH:MM",  # см. TODO по Excel: для минут — 'mm'
                    border=True,
                )
                # отображение в отчете времени работы
                self.set_data(
                    text=executer.get_work_time_in_hours,
                    address=f"H{row}",
                    sheet=sheet,
                    number_format="0.00",
                    border=True,
                )
                # формула подсчета стоимости Заявки для Исполнителя
                self.set_data(
                    text=self._round_formula(formulas["itog_once"].format(row)),
                    address=f"I{row}",
                    sheet=sheet,
                    number_format="#,##0.00₽",
                    border=True,
                )

                # выплата HOOPS
                self.set_data(
                    text=self._round_formula(formulas["for_hoops"].format(row, remuneration)),
                    address=f"J{row}",
                    sheet=sheet,
                    number_format="#,##0.00₽",
                    border=True,
                )
                # вознаграждение HOOPS
                self.set_data(
                    text=for_remuneration,
                    address=f"K{row}",
                    sheet=sheet,
                    number_format="#,##0.00₽",
                    border=True,
                )
                # выплата Исполнителям
                self.set_data(
                    text=self._round_formula(formulas["for_executers"].format(row)),
                    address=f"L{row}",
                    sheet=sheet,
                    number_format="#,##0.00₽",
                    border=True,
                )
                # номер Заявки
                self.set_data(text=executer.task.id, address=f"M{row}", sheet=sheet, border=True)
                # описание проблемы(коррекционного комментария) в Заявке если есть
                self.set_data(text=executer.problem, address=f"N{row}", sheet=sheet, border=True)
                # ФИО Менеджера Заявки
                self.set_data(text=task.manager.fullname, address=f"O{row}", sheet=sheet, border=True)
                # Дополнительная информация
                if task.additional:
                    self.set_data(
                        text=self.get_time_with_offset(task.additional.datetime).date(),
                        number_format="DD.MM.YYYY",
                        address=f"P{row}",
                        sheet=sheet,
                        border=True,
                    )
                    self.set_data(
                        text=task.additional.description,
                        address=f"Q{row}",
                        sheet=sheet,
                        alignment="right",
                        border=True,
                    )
                    flag_additional = True

                row += 1
            all_pay += task.full_pay_real
            all_hours += task.full_work_time_real
        row += 1
        res_after_task = datetime.now() - now
        if not flag_additional:
            sheet.column_dimensions["P"].hidden = True
            sheet.column_dimensions["Q"].hidden = True

        # после отчета доп статистика (итоги за период по таблице и по факту)
        # суммы за период
        self.set_data(text="Сумма  услуг по заявкам за период:", address=f"A{row}", sheet=sheet)
        # сумма оплаты
        self.set_data(
            text=self._round_formula(formulas["itog_all_rub"].format(first_text, row - 2)),
            address=f"I{row}",
            sheet=sheet,
            number_format="#,##0.00₽",
        )
        # сумма часов
        self.set_data(
            text=formulas["itog_all_hours"].format(first_text, row - 2),
            address=f"H{row}",
            sheet=sheet,
            number_format="0.0",
        )

        # сумма комиссий HOOPS
        self.set_data(text=summ_for_hoops, address=f"J{row}", sheet=sheet, number_format="#,##0.00₽")
        # сумма выплат Исполнителям
        self.set_data(
            text=self._round_formula(formulas["for_executers"].format(row, row)), address=f"L{row}", sheet=sheet, number_format="#,##0.00₽"
        )
        self.set_data(text=for_remuneration_all, address=f"K{row}", sheet=sheet, number_format="#,##0.00₽")
        row += 1
        # суммы фактические за период
        self.set_data(text="Сумма фактически оказанных услуг за период:", address=f"A{row}", sheet=sheet)
        # сумма оплаты
        all_pay = sum(x.full_pay_real for x in tasks)
        # сумма часов
        all_hours = sum(x.full_work_time_real for x in tasks)

        # объем часов
        self.set_data(text=all_hours, address=f"H{row}", sheet=sheet, number_format="0.0")
        # сумма к оплате
        self.set_data(text=all_pay, address=f"I{row}", sheet=sheet, number_format="#,##0.00₽")
        # сумма комиссий HOOPS фактических
        self.set_data(text=summ_for_hoops_real, address=f"J{row}", sheet=sheet, number_format="#,##0.00₽")
        self.set_data(text=for_remuneration_all_real, address=f"K{row}", sheet=sheet, number_format="#,##0.00₽")
        # сумма выплат Исполнителям фактическая
        self.set_data(
            text=self._round_formula(formulas["for_executers"].format(row, row)), address=f"L{row}", sheet=sheet, number_format="#,##0.00₽"
        )
        res_before_footer = datetime.now() - now
        # производим добавление футера
        self.footer(sheet=sheet, row=row)
        self.wb.save(self.path_storage)
        self.wb.close()
        # server.getUrlForFile(path)
        # raise ValueError(f"{res_before_task=}, {res_after_task=}, {res_before_footer=}")
        return self.path

    def create_manager_management_report(self, *, tasks=None, period=""):
        """
        Формирует управленческий отчет (лист "Управленческий отчёт").

        Основная таблица по исполнителям, затем блоки суммарных показателей, а также
        детализация по персональным профессиям и по ставкам в задачах без персональных профессий.

        Типы и форматы:
        - Часы: столбцы G/J и т.п. — формат "0.00".
        - Стоимости: формат "#,##0.00₽". Для без НДС значения делятся на 1.2.
        - Формулы подставляются строками в виде "=...".

        TODO: как и в стандартном отчете менеджера, period записывается в B1 поверх названия отеля.
        """
        formulas = {
            "count_hours": r'=IF(OR(E{0}=0,F{0}=0),0,IF(F{0}>=E{0},(F{0}-E{0})*24,(("24:00"-E{0})+(F{0}-"00:00"))*24))',
            "itog_once": "=ROUND(D{0}*G{0}, 2)",
            "itog_all_hours": "=SUM(J{0}:J{1})",
            "itog_all_hours_table": "=SUM(G{0}:G{1})",
            "itog_all_rub": "=ROUND(SUM(H{0}:H{1}), 2)",
            "itog_all_rub_table": "=ROUND(SUM(H{0}:H{1}), 2)",
            "itog_all_rub_NDS": "=ROUND(SUM(I{0}:I{1}), 2)",
            "sum_for_hoops_table": "=ROUND(SUM(I{0}:I{1}), 2)",
            "sum_for_hoops_without_tax_table": "=ROUND(SUM(J{0}:J{1}), 2)",
            "for_executers_table": "=ROUND(SUM(K{0}:K{1}), 2)",
            "for_executers": "=ROUND(H{0}-I{0}, 2)",
            "for_hoops": "=ROUND(H{0}*(100-{1})/100, 2)",
            "cost_hoops_without_nds": "=ROUND($I${0}/1.2, 2)",
            "multiply_NDS": "=C{0}*B{0}",
            "multiply_without_NDS": "=D{0}*B{0}",
            "for_executer": "=C{0}*BE{0}",
            "sum_nds": "=H{0}-I{0}",
        }

        sheet = self.wb["Управленческий отчёт"]

        # заголовок ИМЯ ГОСТИНИЦЫ
        self.set_data(text=tasks[0].manager.hotel.nameHotel, sheet=sheet, address=f"B1", alignment="center")
        # ПЕРИОД отчета
        self.set_data(text=period, sheet=sheet, address=f"B1", alignment="center")
        summ_for_hoops = 0
        summ_for_hoops_real = 0
        for_executer_real = 0
        summ_for_pay = 0

        # работа с задачами
        first_text = 3
        row = first_text
        for task in tasks:
            for executer in task.executers.all():
                if executer.status == "CANCEL_BY_CUSTOMER" or executer.status == "CANCEL_YOURSELF":
                    continue
                self.set_data(
                    text=executer.executer.full_name, address=f"A{row}", sheet=sheet, border=True, alignment="left"
                )
                self.set_data(text=task.finish_name, address=f"B{row}", sheet=sheet, border=True)
                self.set_data(
                    text=self.get_time_with_offset(task.start_at).date(),
                    address=f"C{row}",
                    sheet=sheet,
                    number_format="DD.MM.YYYY",
                    border=True,
                )
                self.set_data(text=task.rent, address=f"D{row}", sheet=sheet, number_format="#,##0.00₽", border=True)
                self.set_data(
                    text=self.get_time_with_offset(executer.start_at_real_or_task).time(),
                    address=f"E{row}",
                    sheet=sheet,
                    number_format="HH:MM",  # см. TODO по Excel: для минут — 'mm'
                    border=True,
                )
                self.set_data(
                    text=self.get_time_with_offset(executer.stop_at_real_or_task).time(),
                    address=f"F{row}",
                    sheet=sheet,
                    number_format="HH:MM",  # см. TODO по Excel: для минут — 'mm'
                    border=True,
                )
                self.set_data(
                    text=executer.get_work_time_in_hours,
                    address=f"G{row}",
                    sheet=sheet,
                    number_format="0.00",
                    border=True,
                )
                self.set_data(
                    text=self._round_formula(formulas["itog_once"].format(row)),
                    address=f"H{row}",
                    sheet=sheet,
                    number_format="#,##0.00₽",
                    border=True,
                )
                self.set_data(
                    text=self._round_formula(formulas["for_hoops"].format(row, task.profession.multiplier)),
                    address=f"I{row}",
                    sheet=sheet,
                    number_format="#,##0.00₽",
                    border=True,
                )
                self.set_data(
                    text=self._round_formula(formulas["cost_hoops_without_nds"].format(row)),
                    address=f"J{row}",
                    sheet=sheet,
                    number_format="#,##0.00₽",
                    border=True,
                )


                self.set_data(
                    text=self._round_formula(formulas["for_executers"].format(row)),
                    address=f"K{row}",
                    sheet=sheet,
                    number_format="#,##0.00₽",
                    border=True,
                )
                self.set_data(text=executer.task.id, address=f"L{row}", sheet=sheet, border=True)
                self.set_data(text=executer.problem, address=f"M{row}", sheet=sheet, border=True)
                self.set_data(text=task.manager.fullname, address=f"N{row}", sheet=sheet, border=True)
                summ_for_hoops += executer.get_sum_for_hoops
                if executer.get_work_time_in_hours_real:
                    summ_for_hoops_real += executer.get_sum_for_hoops
                    for_executer_real += executer.get_sum_for_pay
                    summ_for_pay += executer.get_sum_full

                row += 1
        row += 1
        # region CУММЫ ЗА ПЕРИОД
        # суммы за период
        self.set_data(text="Сумма  услуг по заявкам за период:", address=f"A{row}", sheet=sheet)
        # сумма часов
        self.set_data(
            text=formulas["itog_all_hours_table"].format(first_text, row - 2),
            address=f"G{row}",
            sheet=sheet,
            number_format="0.0",
        )
        # сумма оплаты
        self.set_data(
            text=self._round_formula(formulas["itog_all_rub_table"].format(first_text, row - 2)),
            address=f"H{row}",
            sheet=sheet,
            number_format="#,##0.00₽",
        )

        # сумма комиссий HOOPS
        self.set_data(text=summ_for_hoops, address=f"I{row}", sheet=sheet, number_format="#,##0.00₽")
        # сумма комиссий HOOPS без НДС
        self.set_data(text=summ_for_hoops / 1.2, address=f"J{row}", sheet=sheet, number_format="#,##0.00₽")
        # сумма выплат Исполнителям
        self.set_data(
            text=self._round_formula(formulas["for_executers_table"].format(first_text, row - 2)),
            address=f"K{row}",
            sheet=sheet,
            number_format="#,##0.00₽",
        )

        row += 1

        # суммы фактические за период
        self.set_data(text="Сумма фактически оказанных услуг за период:", address=f"A{row}", sheet=sheet)
        # сумма оплаты
        all_hours = sum(x.full_work_time_real for x in tasks)
        # сумма часов
        all_pay = sum(x.full_pay_real for x in tasks)

        # объем часов
        self.set_data(text=all_hours, address=f"G{row}", sheet=sheet, number_format="0.0")
        # сумма к оплате
        self.set_data(text=all_pay, address=f"H{row}", sheet=sheet, number_format="#,##0.00₽")
        # сумма комиссий HOOPS фактических
        self.set_data(text=summ_for_hoops_real, address=f"I{row}", sheet=sheet, number_format="#,##0.00₽")
        # сумма комиссий HOOPS фактических без НДС
        self.set_data(text=summ_for_hoops_real / 1.2, address=f"J{row}", sheet=sheet, number_format="#,##0.00₽")
        # сумма выплат Исполнителям фактическая
        self.set_data(text=for_executer_real, address=f"K{row}", sheet=sheet, number_format="#,##0.00₽")
        # endregion

        # итоги по персональнмы профессиям
        tasks_with_personal_professions = tasks.exclude(personal_profession=None)
        tasks_without_personal_professions = tasks.filter(personal_profession=None)
        personal_professions = set(
            tasks_with_personal_professions.values_list(
                "personal_profession__id",
                "personal_profession__name",
            )
        )
        rents_in_tasks_without_personal_professions = set(
            tasks_without_personal_professions.values_list("rent", "profession__id")
        )
        if tasks_with_personal_professions:
            row += 2
            self.set_data(text="Детализация фактически оказанных услуг", address=f"A{row}", sheet=sheet, border=True)
            row += 1
            self.set_data(text="Наименование профессии", address=f"A{row}", sheet=sheet, border=True)

            self.set_data(text="Объем услуг", address=f"B{row}", sheet=sheet, border=True)
            self.set_data(text="Ставка с НДС", address=f"C{row}", sheet=sheet, border=True)
            self.set_data(text="Ставка без НДС", address=f"D{row}", sheet=sheet, border=True)
            self.set_data(text="Стоимость HOOPS с НДС", address=f"E{row}", sheet=sheet, border=True)
            self.set_data(text="Стоимость HOOPS без НДС", address=f"F{row}", sheet=sheet, border=True)
            self.set_data(text="Стоимость Исполнитель", address=f"G{row}", sheet=sheet, border=True)
            self.set_data(text="Стоимость услуг с НДС ", address=f"H{row}", sheet=sheet, border=True)
            self.set_data(text="Стоимость услуг без НДС ", address=f"I{row}", sheet=sheet, border=True)
            self.set_data(text="Сумма НДС ", address=f"J{row}", sheet=sheet, border=True)
            row += 1
        row_start_management = row
        for personal_profession in personal_professions:
            tasks_with_current_personal_profession = tasks_with_personal_professions.filter(
                personal_profession__id=personal_profession[0]
            )
            all_hours = sum(x.full_work_time_real for x in tasks_with_current_personal_profession)
            if not all_hours:
                continue
            # наименвоание профессии
            self.set_data(text=personal_profession[1], address=f"A{row}", sheet=sheet, border=True)
            # объем услуг
            self.set_data(text=all_hours, address=f"B{row}", sheet=sheet, number_format="0.0", border=True)
            # ставка с НДС
            self.set_data(
                text=tasks_with_current_personal_profession[0].rent,
                address=f"C{row}",
                number_format="#,##0.00₽",
                sheet=sheet,
                border=True,
            )
            # ставка без НДС
            self.set_data(
                text=tasks_with_current_personal_profession[0].without_tax,
                address=f"D{row}",
                number_format="#,##0.00₽",
                sheet=sheet,
                border=True,
            )
            # стоимость HOOPS
            self.set_data(
                text=tasks_with_current_personal_profession[0].for_hoops,
                address=f"E{row}",
                number_format="#,##0.00₽",
                sheet=sheet,
                border=True,
            )

            # стоимость HOOPS без НДС
            self.set_data(
                text=tasks_with_current_personal_profession[0].for_hoops_without_tax,
                address=f"F{row}",
                number_format="#,##0.00₽",
                sheet=sheet,
                border=True,
            )
            # стоимость Исполнитель
            self.set_data(
                text=tasks_with_current_personal_profession[0].rent
                - tasks_with_current_personal_profession[0].for_hoops,
                address=f"G{row}",
                number_format="#,##0.00₽",
                sheet=sheet,
                border=True,
            )
            # стоимость услуг с НДС
            self.set_data(
                text=self._round_formula(formulas["multiply_NDS"].format(row)),
                address=f"H{row}",
                sheet=sheet,
                number_format="#,##0.00₽",
                border=True,
            )
            # стоимость услуг без НДС
            self.set_data(
                text=self._round_formula(formulas["multiply_without_NDS"].format(row)),
                address=f"I{row}",
                sheet=sheet,
                number_format="#,##0.00₽",
                border=True,
            )
            # сумма НДС
            self.set_data(
                text=self._round_formula(formulas["sum_nds"].format(row)),
                address=f"J{row}",
                sheet=sheet,
                number_format="#,##0.00₽",
                border=True,
            )
            row += 1
        # raise ValueError(str(rents_in_tasks_without_personal_professions))
        for rent in rents_in_tasks_without_personal_professions:

            tasks_with_current_rent = tasks_without_personal_professions.filter(
                rent=rent[0],
                profession__id=rent[1],
            )
            all_hours = sum(x.full_work_time_real for x in tasks_with_current_rent)
            if not all_hours:
                continue
            # наименование профессии
            self.set_data(text=tasks_with_current_rent[0].profession.name, address=f"A{row}", sheet=sheet, border=True)
            # объем услуг
            self.set_data(text=all_hours, address=f"B{row}", sheet=sheet, number_format="0.0", border=True)
            # ставка с НДС
            self.set_data(
                text=tasks_with_current_rent[0].rent,
                address=f"C{row}",
                number_format="#,##0.00₽",
                sheet=sheet,
                border=True,
            )
            # ставка без НДС
            self.set_data(
                text=tasks_with_current_rent[0].without_tax,
                address=f"D{row}",
                number_format="#,##0.00₽",
                sheet=sheet,
                border=True,
            )
            # стоимость HOOPS
            self.set_data(
                text=tasks_with_current_rent[0].for_hoops,
                address=f"E{row}",
                number_format="#,##0.00₽",
                sheet=sheet,
                border=True,
            )

            # стоимость HOOPS без НДС
            self.set_data(
                text=tasks_with_current_rent[0].for_hoops_without_tax,
                address=f"F{row}",
                number_format="#,##0.00₽",
                sheet=sheet,
                border=True,
            )
            # стоимость Исполнитель
            self.set_data(
                text=tasks_with_current_rent[0].rent - tasks_with_current_rent[0].for_hoops,
                address=f"G{row}",
                number_format="#,##0.00₽",
                sheet=sheet,
                border=True,
            )
            # стоимость услуг с НДС
            self.set_data(
                text=self._round_formula(formulas["multiply_NDS"].format(row)),
                address=f"H{row}",
                sheet=sheet,
                number_format="#,##0.00₽",
                border=True,
            )
            # стоимость услуг без НДС
            self.set_data(
                text=self._round_formula(formulas["multiply_without_NDS"].format(row)),
                address=f"I{row}",
                sheet=sheet,
                number_format="#,##0.00₽",
                border=True,
            )
            # сумма НДС
            self.set_data(
                text=self._round_formula(formulas["sum_nds"].format(row)),
                address=f"J{row}",
                sheet=sheet,
                number_format="#,##0.00₽",
                border=True,
            )

            # self.set_data(text=tasks_with_current_rent[0].without_tax, address=f'B{row}',
            #               number_format='#,##0.00₽', sheet=sheet, border=True)
            # self.set_data(text=tasks_with_current_rent[0].rent, address=f'C{row}',
            #               number_format='#,##0.00₽', sheet=sheet, border=True)
            #
            # self.set_data(text=all_hours, address=f'D{row}', sheet=sheet, number_format='0.0', border=True)
            #
            # self.set_data(text=formulas['multiply_NDS'].format(row), address=f'E{row}', sheet=sheet,
            #               number_format='#,##0.00₽', border=True)
            # self.set_data(text=formulas['multiply_without_NDS'].format(row), address=f'F{row}', sheet=sheet,
            #               number_format='#,##0.00₽', border=True)
            row += 1
        row += 1
        self.set_data(text="Итог:", address=f"A{row}", sheet=sheet)
        self.set_data(
            text=self._round_formula(formulas["itog_all_rub"].format(row_start_management, row - 2)),
            address=f"H{row}",
            sheet=sheet,
            number_format="#,##0.00₽",
        )
        self.set_data(
            text=self._round_formula(formulas["itog_all_rub_NDS"].format(row_start_management, row - 2)),
            address=f"I{row}",
            sheet=sheet,
            number_format="#,##0.00₽",
        )
        self.set_data(
            text=formulas["itog_all_hours"].format(row_start_management, row - 2),
            address=f"J{row}",
            sheet=sheet,
            number_format="#,##0.00₽",
        )
        # производим добавление футера
        self.footer(sheet=sheet, row=row)
        # сохраняем файл
        self.wb.save(self.path_storage)
        # закрываем файл
        self.wb.close()
        # server.getUrlForFile(path)
        return self.path

    def create_manager_report(self, *, tasks, period):
        """
        Отчет по менеджерам (лист "Отчет по менеджерам").

        Для каждого активного менеджера отеля выводит его заявки, количество услуг,
        часы и сумму. Итоги суммируются формулами по диапазону строк.

        Примечания:
        - Для дат используется запись datetime.date + формат "DD.MM.YYYY".
        - Формулы суммирования: SUM по столбцам E/F/G.
        - Количество услуг — количество состояний исполнителей без отмененных.
        """

        sheet = self.wb["Отчет по менеджерам"]

        # заголовок ИМЯ ГОСТИНИЦЫ
        self.set_data(
            address=f"B1", text=tasks[0].manager.hotel.nameHotel, sheet=sheet, alignment="center", border=True
        )
        # ПЕРИОД отчета
        self.set_data(address=f"A1", text=period, sheet=sheet, alignment="center", border=True)

        # работа с заявками

        row = 2
        for manager in tasks[0].manager.hotel.manager_set.all().filter(status__in=[2, 3], is_active=True):
            manager_tasks = tasks.filter(manager=manager).exclude(status="DELETED").order_by("profession", "start_at")

            # region headerManager
            # запись заголовка менеджера

            self.set_data(
                address=f"A{str(row)}",
                text="ФИО менеджера",
                sheet=sheet,
                alignment="center",
                border=True,
                fill=openpyxl.styles.PatternFill(start_color="D9D9D9", end_color="D9D9D9", fill_type="solid"),
            )
            self.set_data(
                address=f"B{str(row)}",
                text="Дата",
                sheet=sheet,
                alignment="center",
                border=True,
                fill=openpyxl.styles.PatternFill(start_color="D9D9D9", end_color="D9D9D9", fill_type="solid"),
            )
            self.set_data(
                address=f"C{str(row)}",
                text="Наименование услуги",
                sheet=sheet,
                alignment="center",
                border=True,
                fill=openpyxl.styles.PatternFill(start_color="D9D9D9", end_color="D9D9D9", fill_type="solid"),
            )

            self.set_data(
                address=f"D{str(row)}",
                text="Ставка",
                sheet=sheet,
                alignment="center",
                border=True,
                fill=openpyxl.styles.PatternFill(start_color="D9D9D9", end_color="D9D9D9", fill_type="solid"),
            )

            self.set_data(
                address=f"E{str(row)}",
                text="Количество услуг, ед.",
                sheet=sheet,
                alignment="center",
                border=True,
                fill=openpyxl.styles.PatternFill(start_color="D9D9D9", end_color="D9D9D9", fill_type="solid"),
            )

            self.set_data(
                address=f"F{str(row)}",
                text="Итого часов",
                sheet=sheet,
                alignment="center",
                border=True,
                fill=openpyxl.styles.PatternFill(start_color="D9D9D9", end_color="D9D9D9", fill_type="solid"),
            )

            self.set_data(
                address=f"G{str(row)}",
                text="Итого оплата, руб.",
                sheet=sheet,
                alignment="center",
                border=True,
                fill=openpyxl.styles.PatternFill(start_color="D9D9D9", end_color="D9D9D9", fill_type="solid"),
            )
            row += 1
            # endregion
            row_start_manager = row
            if manager_tasks.count() == 0:
                self.set_data(address=f"A{row}", text=manager.fullname, sheet=sheet, border=True)
                row += 1

            for task in manager_tasks:
                if task.executers.all().count() == 0:
                    continue
                self.set_data(
                    address=f"A{row}", text=manager.fullname, sheet=sheet, border=True
                )
                # Дата
                sheet["B" + str(row)] = task.start_at.date()
                self.set_data(
                    address=f"B{row}", text=task.start_at.date(), number_format="DD.MM.YYYY", sheet=sheet, border=True
                )

                # Наименование услуги
                self.set_data(
                    address=f"C{row}", text=task.profession.name, number_format="DD.MM.YYYY", sheet=sheet, border=True
                )

                # Ставка
                self.set_data(address=f"D{row}", text=task.rent, number_format="#,##0.00₽", sheet=sheet, border=True)

                # Количество услуг
                count = (
                    task.executers.all().exclude(status="CANCEL_BY_CUSTOMER").exclude(status="CANCEL_YOURSELF").count()
                )
                self.set_data(
                    address=f"E{row}", text=count if count != 0 else task.count_executers, sheet=sheet, border=True
                )

                # Итого часов

                self.set_data(
                    address=f"F{row}", text=task.full_work_time_real, number_format="0.00", sheet=sheet, border=True
                )
                # итого стоимость
                self.set_data(
                    address=f"G{row}", text=self._round_formula(f"=D{row}*F{row}"), number_format="#,##0.00₽", sheet=sheet, border=True
                )

                row += 1

            sheet["A" + str(row)] = "Итог:"
            self.set_data(address=f"A{row}", text="Итог:", sheet=sheet)
            self.set_data(address=f"E{row}", text="=SUM(E{0}:E{1})".format(row_start_manager, row - 1), sheet=sheet)
            self.set_data(
                address=f"F{row}",
                text="=SUM(F{0}:F{1})".format(row_start_manager, row - 1),
                number_format="0.00",
                sheet=sheet,
            )
            self.set_data(
                address=f"F{row}",
                text=self._round_formula(f"=SUM(G{0}:G{1})".format(row_start_manager, row - 1)),
                number_format="#,##0.00₽",
                sheet=sheet,
            )

            row += 2

        self.wb.save(self.path_storage)
        self.wb.close()
        return self.path

    def create_manager_correction(self, *, tasks, period):
        """
        Отчет по корректировкам (лист "Корректировки") для менеджера.

        Выводит записи только по тем исполнителям, у которых есть correction_comment.
        """

        sheet = self.wb["Корректировки"]

        # заголовок ИМЯ ГОСТИНИЦЫ
        self.set_data(
            address=f"B1", text=tasks[0].manager.hotel.nameHotel, sheet=sheet, alignment="center", border=True
        )
        # ПЕРИОД отчета
        self.set_data(address=f"A1", text=period, sheet=sheet, alignment="center", border=True)

        row = 3
        for task in tasks:
            for executer in task.executers.all():
                if executer.correction_comment is None:
                    continue

                self.set_data(
                    address=f"A{row}",
                    text=self.get_time_with_offset(task.start_at).date(),
                    alignment="left",
                    number_format="DD.MM.YYYY",
                    sheet=sheet,
                    border=True,
                )
                self.set_data(
                    address=f"B{row}", text=task.manager.fullname, alignment="left", sheet=sheet, border=True
                )
                self.set_data(address=f"C{row}", text=executer.problem, alignment="left", sheet=sheet, border=True)
                self.set_data(address=f"D{row}", text=f"#{task.id}", alignment="left", sheet=sheet, border=True)
                self.set_data(
                    address=f"E{row}", text=executer.executer.full_name, alignment="left", sheet=sheet, border=True
                )
                self.set_data(
                    address=f"F{row}",
                    text=task.profession.name if task.personal_profession is None else task.personal_profession.name,
                    alignment="left",
                    sheet=sheet,
                    border=True,
                )

        self.wb.save(self.path_storage)
        self.wb.close()
        return self.path

    def create_manager_by_type(self, *, period, tasks):
        """
        Отчет по типам услуг (лист "По типам услуг") для менеджера.

        Для каждой заявки (с исполнителями) выводятся профессия, дата, ставка,
        количество исполнителей, суммарные часы и сумма (формула =E*С).
        Итоги по столбцам внизу таблицы (SUM).
        """

        sheet = self.wb["По типам услуг"]

        # заголовок ИМЯ ГОСТИНИЦЫ
        self.set_data(
            address=f"B1", text=tasks[0].manager.hotel.nameHotel, sheet=sheet, alignment="center", border=True
        )
        # ПЕРИОД отчета
        self.set_data(address=f"A1", text=period, sheet=sheet, alignment="center", border=True)
        # работа с задачами
        row = self.first_text

        for task in tasks:
            if task.executers.all().count() == 0:
                continue

            # Наименование услуги
            self.set_data(address=f"A{row}", text=task.profession.name, alignment="left", sheet=sheet, border=True)
            # Дата
            self.set_data(
                address=f"B{row}",
                text=self.get_time_with_offset(task.start_at).date(),
                alignment="left",
                number_format="DD.MM.YYYY",
                sheet=sheet,
                border=True,
            )

            # Ставка
            self.set_data(
                address=f"C{row}",
                text=task.rent,
                alignment="left",
                sheet=sheet,
                number_format="#,##0.00₽",
                border=True,
            )

            # Количество услуг
            self.set_data(
                address=f"D{row}",
                text=task.executers.all()
                .exclude(status="CANCEL_BY_CUSTOMER")
                .exclude(status="CANCEL_YOURSELF")
                .count(),
                alignment="left",
                sheet=sheet,
                border=True,
            )

            self.set_data(
                address=f"E{row}",
                text=task.full_work_time_real,
                alignment="left",
                sheet=sheet,
                number_format="0.00",
                border=True,
            )
            self.set_data(
                address=f"F{row}",
                text=self._round_formula(f"=E{row}*C{row}"),
                alignment="left",
                sheet=sheet,
                number_format="#,##0.00₽",
                border=True,
            )
            row += 1
        row += 1

        self.set_data(address=f"A{row}", text="Итог:", alignment="left", sheet=sheet)
        self.set_data(
            address=f"D{row}", text="=SUM(D{0}:D{1})".format(self.first_text, row - 2), alignment="left", sheet=sheet
        )
        self.set_data(
            address=f"E{row}", text="=SUM(E{0}:E{1})".format(self.first_text, row - 2), alignment="left", sheet=sheet
        )
        self.set_data(
            address=f"F{row}", text="=SUM(F{0}:F{1})".format(self.first_text, row - 2), alignment="left", sheet=sheet
        )

        self.wb.save(self.path_storage)
        self.wb.close()
        return self.path

    def create_executer_standart_report(self, *, tasks=None, period=""):
        """
        Стандартный отчет Исполнителя (лист "Стандартный отчёт").

        Для каждой работы исполнителя выводятся дата, отель, время начала/окончания,
        количество часов, ставка для исполнителя, комментарий, суммы к выплате
        и сумма с удержанием (умножение на коэффициент 0.94).

        Примечания:
        - Для get_sum_for_pay * 0.94: коэффициент удержания/скидки фиксирован в коде.
        - Для времени используется number_format "HH:MM" — см. TODO по Excel.
        - Итоги по часам/суммам — формулы SUM по диапазонам.
        """
        formulas = {
            "itog_all_rub_ds": "=SUM(I{0}:I{1})",
            "itog_all_rub": "=SUM(H{0}:H{1})",
            "itog_all_hours": "=SUM(E{0}:E{1})",
        }
        sheet = self.wb["Стандартный отчёт"]

        # ПЕРИОД отчета
        self.set_data(sheet=sheet, address="A1", text=period, alignment="center")

        # работа с задачами
        first_text = 3
        row = first_text
        for executer in tasks:
            self.set_data(
                sheet=sheet,
                address=f"A{row}",
                text=f"{self.get_time_with_offset(executer.start_at_real_or_task):%d.%m.%Y}",
                number_format="DD.MM.YYYY",
                alignment="right",
                border=True,
            )
            self.set_data(
                sheet=sheet,
                address=f"B{row}",
                text=executer.task.manager.hotel.nameHotel,
                alignment="right",
                border=True,
            )

            self.set_data(
                sheet=sheet,
                address=f"C{row}",
                text=self.get_time_with_offset(executer.start_at_real_or_task).time(),
                number_format="HH:MM",  # см. TODO по Excel: для минут — 'mm'
                border=True,
            )
            self.set_data(
                sheet=sheet,
                address=f"D{row}",
                text=(
                    self.get_time_with_offset(executer.stop_at_real_or_task).time()
                    if executer.volume_of_the_work is None
                    else ""
                ),
                number_format="HH:MM",  # см. TODO по Excel: для минут — 'mm'
                border=True,
            )
            self.set_data(
                sheet=sheet, address=f"E{row}", text=executer.get_work_time_in_hours, number_format="0.0", border=True
            )
            self.set_data(
                sheet=sheet,
                address=f"F{row}",
                text=executer.task.rent_for_executer,
                number_format="#,##0.00₽",
                border=True,
            )
            self.set_data(sheet=sheet, address=f"G{row}", text=executer.problem, border=True)
            self.set_data(
                sheet=sheet, address=f"H{row}", text=executer.get_sum_for_pay, number_format="#,##0.00₽", border=True
            )
            self.set_data(
                sheet=sheet,
                address=f"I{row}",
                text=executer.get_sum_for_pay * 0.94,
                number_format="#,##0.00₽",
                border=True,
            )
            row += 1
        row += 1
        self.set_data(text="Итог:", sheet=sheet, address=f"A{row}")

        self.set_data(
            text=formulas["itog_all_hours"].format(first_text, row - 2),
            sheet=sheet,
            address=f"E{row}",
            number_format="0.0",
        )
        self.set_data(
            text=formulas["itog_all_rub"].format(first_text, row - 2),
            sheet=sheet,
            address=f"H{row}",
            number_format="#,##0.00₽",
        )
        self.set_data(
            text=formulas["itog_all_rub_ds"].format(first_text, row - 2),
            sheet=sheet,
            address=f"I{row}",
            number_format="#,##0.00₽",
        )

        self.wb.save(self.path_storage)
        self.wb.close()
        return self.path

    def create_executer_by_type(self, *, executer_states=None, period=""):
        """
        Создание отчета по типам услуг для Исполнитлея
        :param executer_states: состояния исполнителя по задачам
        :param period: пеирод отчета
        :return: путь к файлу
        """
        # Типы и агрегирование:
        # - executer_states: QuerySet состояний, у каждого есть связи на task и свойства сумм/часов.
        # - Группировка по profession_id через values_list(distinct=True).
        # - Для каждой профессии суммируются часы (get_work_time_in_hours, float) и суммы (get_sum_full, float).
        # открываем страницу
        sheet = self.wb["По типам услуг"]

        # ПЕРИОД отчета
        self.set_data(sheet=sheet, address="A1", text=period, alignment="center")

        # работа с задачами
        row = 3
        # список возможных профессий из состояний
        professions_ids = executer_states.values_list("task__profession_id", flat=True).distinct()
        # итоговое количество денег
        rubs = 0.0
        # итоговое количество часов
        hours = 0.0
        # для всех профессий из возможных
        for profession_id in professions_ids:
            # итоговые значения по указанной профессии
            total_hours = 0.0
            total_rub = 0.0
            # получаем состояния по конкретной профессии
            executer_with_current_profession = executer_states.filter(task__profession_id=profession_id)
            # наименование профессии
            self.set_data(
                address=f"A{row}",
                text=executer_with_current_profession.first().task.profession.name,
                border=True,
                alignment="left",
                sheet=sheet,
            )
            # количество таких заявок
            self.set_data(
                address=f"B{row}",
                text=executer_with_current_profession.count(),
                border=True,
                alignment="left",
                sheet=sheet,
            )

            # для всех работ
            for executer in executer_with_current_profession:
                # сумма времени
                total_hours += executer.get_work_time_in_hours
                # сумма денег
                total_rub += executer.get_sum_full

            rubs += total_rub
            hours += total_hours
            # количество часов
            self.set_data(
                address=f"C{row}", text=total_hours, border=True, alignment="left", number_format="0.00", sheet=sheet
            )
            # стоимость
            self.set_data(
                address=f"D{row}",
                text=total_rub,
                border=True,
                alignment="left",
                number_format="#,##0.00₽",
                sheet=sheet,
            )
            # переходим к следующей строке
            row += 1
        # отделяемся от блока статситики к блоку итого
        row += 1

        # слово итог
        self.set_data(address=f"A{row}", text="Итог:", alignment="right", sheet=sheet)
        # итоговая стоимость
        self.set_data(
            address=f"D{row}", text=rubs, border=True, alignment="left", number_format="#,##0.00₽", sheet=sheet
        )

        # итоговое количество часов
        self.set_data(
            address=f"C{row}", text=hours, border=True, alignment="left", number_format="#,##0.00", sheet=sheet
        )

        # сохраняем и закрываем файл
        self.wb.save(self.path_storage)
        self.wb.close()

        return self.path

    def create_executer_financial(self, *, executer_states=None, period=""):
        """
        Сводный финансовый отчет для Исполнителя (лист "Сводный финансовый").

        Агрегирует суммы к выплате по месяцам (task.start_at -> "MM.YYYY").

        Особенности:
        - Используется словарь result_dict, т.к. фильтрация по month на MySQL через Django
          затруднена в используемой версии.
        - Столбец B — суммы к выплате (числа), итог — формула SUM(B:first:B:last).
        - Строки с отмененными статусами пропускаются.
        """

        formulas = {
            "itog_all_rub": "=SUM(B{0}:B{1})",
        }

        sheet = self.wb["Сводный финансовый"]

        # ПЕРИОД отчета
        self.set_data(sheet=sheet, address="A1", text=period, alignment="center")

        # работа с задачами
        row = self.first_text
        # через словарь потому что джанга не умеет на mySQL фильтровать по месяцам
        result_dict = {}
        # для всех задач
        for executer in executer_states:
            if executer.status == "CANCEL_BY_CUSTOMER" or executer.status == "CANCEL_YOURSELF":
                continue
            # дата заявки месяц.год
            m_y = f"{executer.task.start_at:%m.%Y}"
            # если в словаре есть такой месяц - плюсуем
            if m_y in result_dict:
                result_dict[m_y] += executer.get_sum_for_pay
            # если нет - присваиваем
            else:
                result_dict[m_y] = executer.get_sum_for_pay

        # для всех полученных пар
        for key, value in result_dict.items():
            # указываем период и количество
            self.set_data(address=f"A{row}", text=key, border=True, sheet=sheet)
            self.set_data(address=f"B{row}", text=value, border=True, number_format="#,##0.00₽", sheet=sheet)
            # переходим к следующей строке
            row += 1
        # отступ перед итоговой частью
        row += 1
        # пишем ИТОГ
        self.set_data(address=f"A{row}", text="Итог:", alignment="right", border=True, sheet=sheet)
        # и формулу подсчета по столбцу
        self.set_data(
            address=f"B{row}",
            text=formulas["itog_all_rub"].format(self.first_text, row - 2),
            alignment="right",
            border=True,
            number_format="#,##0.00₽",
            sheet=sheet,
        )
        # сохраняем и закрываем файл
        self.wb.save(self.path_storage)
        self.wb.close()

        return self.path

    def create_executer_correction(self, *, executer_states, period):
        """
        Создание отчета коррекций для исполнителя
        :param executer_states: статусы исполнителей
        :param period: строка для указания периода
        :return: путь к файлу
        """
        # Выводятся строки только для executer_states, у которых correction_comment != None.
        # Форматирование дат/строк аналогично другим отчетам.
        # открываем нужну страницу
        sheet = self.wb["Корректировки"]

        # ПЕРИОД отчета
        self.set_data(address=f"A1", text=period, sheet=sheet, alignment="center", border=True)

        row = self.first_text
        # для всех состояний
        for executer in executer_states.exclude(correction_comment=None):
            # указываем дату
            self.set_data(
                address=f"A{row}",
                text=self.get_time_with_offset(executer.task.start_at).date(),
                alignment="left",
                number_format="DD.MM.YYYY",
                sheet=sheet,
                border=True,
            )
            # указываем менеджера
            self.set_data(
                address=f"B{row}", text=executer.task.manager.fullname, alignment="left", sheet=sheet, border=True
            )
            # указываем проблему
            self.set_data(address=f"C{row}", text=executer.problem, alignment="left", sheet=sheet, border=True)
            # указываем номер заявки
            self.set_data(address=f"D{row}", text=f"#{executer.task.id}", alignment="left", sheet=sheet, border=True)
            # имя исполнителя
            self.set_data(
                address=f"E{row}", text=executer.executer.full_name, alignment="left", sheet=sheet, border=True
            )
            # наименование профессии задачи
            self.set_data(
                address=f"F{row}", text=executer.task.finish_name, alignment="left", sheet=sheet, border=True
            )
        # сохраняем и закрываем файл
        self.wb.save(self.path_storage)
        self.wb.close()
        return self.path

    def create_admin_activity_report(self, *, hotels, period, period_datetime, tasks):
        """
        Создание отчета активности для Администратора
        :param period_datetime: Отнормаленные даты периода
        :param hotels: Список гостиниц
        :param period: строка для указания периода
        :return: путь к файлу
        """
        # Примечание по данным:
        # - hotels: QuerySet, аннотируется count_tasks по диапазону дат через Count + Q(filter=...).
        # - tasks: QuerySet задач для вычисления выручки по отелю (sum full_pay_real).
        # - Колонки: A — №, B — Имя отеля, C — Кол-во задач, D/E — периоды оплат, F — выручка.
        row = self.first_text
        # открываем нужную страницу
        sheet = self.wb["Активность"]

        # ПЕРИОД отчета
        self.set_data(address=f"B1", text=period, sheet=sheet, alignment="center", border=True)
        hotels = hotels.annotate(
            count_tasks=Count(
                "manager__task",
                filter=Q(manager__task__start_at__range=period_datetime),
                exclude=Q(manager__task__status="DELETED"),
            )
        ).order_by("-count_tasks")

        # для всех гостиниц
        for number, hotel in enumerate(hotels, 1):
            # указываем номер
            self.set_data(address=f"A{row}", text=number, alignment="left", sheet=sheet, border=True)
            # указываем имя
            self.set_data(address=f"B{row}", text=hotel.nameHotel, alignment="left", sheet=sheet, border=True)
            # указываем количество
            self.set_data(address=f"C{row}", text=hotel.count_tasks, alignment="left", sheet=sheet, border=True)
            # указываем период оплат

            self.set_data(
                address=f"D{row}",
                text=str(hotel.payment_period_to_hoops_ru),
                alignment="left",
                sheet=sheet,
                border=True,
            )
            # указываем период выплат
            self.set_data(
                address=f"E{row}", text=hotel.payment_period_to_executor_ru, alignment="left", sheet=sheet, border=True
            )

            # выручка
            self.set_data(
                address=f"F{row}",
                text=sum(x.full_pay_real for x in tasks.filter(manager__hotel__id=hotel.id)),
                alignment="right",
                number_format="#,##0.00₽",
                sheet=sheet,
                border=True,
            )

            row += 1

        self.set_data(address=f"E{row}", text="Итого", alignment="right", sheet=sheet, border=True)
        self.set_data(
            address=f"F{row}",
            text=f"=SUM(F{self.first_text}:F{row-1})",
            alignment="right",
            sheet=sheet,
            border=True,
            number_format="#,##0.00₽",
        )
        # сохраняем и закрываем файл
        self.wb.save(self.path_storage)
        self.wb.close()
        return self.path

    def create_admin_comparative_report(self, *, executers, hotels, professions, period):
        """
        Создание отчета сравнительного для Администратора
        :param executers: Статусы исполнителей на конкретный период
        :param hotels: Список гостиниц
        :param professions: Список профессий
        :param period: строка для указания периода
        :return: путь к файлу
        """
        # Идея отчета:
        # - Для каждой профессии выводятся две строки: "постоянно" и "периодически".
        # - Для каждого отеля вставляются 4 колонки: % внештатных, количество, средний чек, сумма.
        # - "Постоянные" исполнители определяются эвристикой: count исполнений > 3.
        # - Считаются доли/кол-ва уникальных исполнителей и суммы/средние чеки по группам.
        # Типы:
        # - Суммы — float, формат "#,##0.00₽"; проценты — как числа с двумя знаками.
        # ВНИМАНИЕ: Используется множество set(...) для подсчета уникальных исполнителей.
        row = self.first_text
        column = "B"
        column_number = 2
        # открываем нужную страницу
        sheet = self.wb["Сравнительный"]

        # ПЕРИОД отчета
        self.set_data(address=f"A1", text=period, sheet=sheet, alignment="center", border=True)
        # сперва пойдем по профессиям и поставим первый столбец с данными
        for profession in professions:
            self.set_data(
                address=f"A{row}",
                text=profession.name,
                sheet=sheet,
                alignment="left",
                fill=openpyxl.styles.PatternFill(fgColor="E2EFDA", fill_type="solid"),
            )

            self.set_data(address=f"A{row+1}", text="постоянно", sheet=sheet, italic=True, alignment="right")
            self.set_data(address=f"A{row+2}", text="периодически", sheet=sheet, italic=True, alignment="right")
            row += 3

        # пройдемся по гостиницам и поставим им все значения
        for hotel in hotels:
            row = self.first_text

            cell = sheet.cell(row=row, column=column_number)
            column = cell.column_letter
            cell_1 = sheet.cell(row=row, column=column_number + 1)
            column_1 = cell_1.column_letter

            cell_2 = sheet.cell(row=row, column=column_number + 2)
            column_2 = cell_2.column_letter

            cell_3 = sheet.cell(row=row, column=column_number + 3)
            column_3 = cell_3.column_letter
            # наименование гостиницы
            sheet.merge_cells(f"{column}1:{column_3}1")
            self.set_data(address=f"{column}1", text=hotel.nameHotel, sheet=sheet, alignment="center")
            # информационная строка
            self.set_data(address=f"{column}2", text="% внештатных", sheet=sheet, alignment="center")
            self.set_data(address=f"{column_1}2", text="количество", sheet=sheet, alignment="center")
            self.set_data(address=f"{column_2}2", text="средний чек", sheet=sheet, alignment="center")
            self.set_data(
                address=f"{column_3}2",
                text="Сумма",
                sheet=sheet,
                alignment="center",
                fill=openpyxl.styles.PatternFill(fill_type="solid", start_color="fe0101", end_color="fe0101"),
            )

            # для профессии из списка профессий
            for index, profession in enumerate(professions):
                # region пустая строка
                self.set_data(
                    address=f"{column}{row}",
                    text=" ",
                    sheet=sheet,
                    alignment="center",
                    fill=openpyxl.styles.PatternFill(fgColor="E2EFDA", fill_type="solid"),
                )
                self.set_data(
                    address=f"{column_1}{row}",
                    text=" ",
                    sheet=sheet,
                    alignment="center",
                    fill=openpyxl.styles.PatternFill(fgColor="E2EFDA", fill_type="solid"),
                )

                self.set_data(
                    address=f"{column_2}{row}",
                    text=" ",
                    sheet=sheet,
                    alignment="center",
                    fill=openpyxl.styles.PatternFill(fgColor="E2EFDA", fill_type="solid"),
                )

                self.set_data(
                    address=f"{column_3}{row}",
                    text=" ",
                    sheet=sheet,
                    alignment="center",
                    fill=openpyxl.styles.PatternFill(fgColor="E2EFDA", fill_type="solid"),
                )
                # endregion
                # список не ротационных Исполнителей
                not_rotation_executers_list = []
                # список сумм оплат не ротационным Исполнителям
                summ_for_pay_not_rotation_list = []
                # список сумм оплат ротационным Исполнителям
                summ_for_pay_rotation_list = []
                # список исполнителей на конкретной профессии и конкретной гостиницы
                executers_current_hotel_and_profession = executers.filter(
                    task__profession=profession, task__manager__hotel=hotel
                )
                # список уникальных исполнителей из executers_current_hotel_and_profession
                executer_list_id = executers_current_hotel_and_profession.values_list("executer__id", flat=True)

                # смотрим количество исполнений в executers_current_hotel_and_profession и формируем список постоянных
                # по условию - больше трех заявок - постоянный
                for executer_id in executer_list_id:
                    current_executer_states = executers_current_hotel_and_profession.filter(executer__id=executer_id)
                    # если сотрудник постоянный
                    if executers_current_hotel_and_profession.filter(executer__id=executer_id).count() > 3:
                        # добавляем его в список постоянных
                        not_rotation_executers_list.append(executer_id)
                        # для всех кго работ считаем оплаты и добавляем в список
                        for current_executer_state in current_executer_states:
                            summ_for_pay_not_rotation_list.append(current_executer_state.get_sum_for_pay)
                    # если сотрудник не постоянный
                    else:
                        # добавляем его оплаты в другой список
                        for current_executer_state in current_executer_states:
                            summ_for_pay_rotation_list.append(current_executer_state.get_sum_for_pay)

                # ставим число и процент сотрудников
                count_not_rotation_executers = len(not_rotation_executers_list)
                count_unique_not_rotation_executers = len(set(not_rotation_executers_list))
                count_rotation_executers = len(executer_list_id) - len(not_rotation_executers_list)
                count_all_executers = len(executer_list_id)
                count_unique_all_executers = len(set(executer_list_id))
                count_unique_rotation_executers = count_unique_all_executers - count_unique_not_rotation_executers
                percent_not_roatation_executors = (
                    count_unique_not_rotation_executers / count_unique_all_executers * 100
                    if count_all_executers
                    else 0
                )
                percent_rotation_executors = (
                    count_unique_rotation_executers / count_unique_all_executers * 100 if count_all_executers else 0
                )
                summ_for_pay_not_rotation = sum(summ_for_pay_not_rotation_list)
                avg_summ_for_pay_not_rotation = (
                    summ_for_pay_not_rotation / len(summ_for_pay_not_rotation_list)
                    if summ_for_pay_not_rotation_list
                    else 0
                )
                sum_for_pay_rotation = sum(summ_for_pay_rotation_list)
                avg_summ_for_pay_rotation = (
                    sum_for_pay_rotation / len(summ_for_pay_rotation_list) if summ_for_pay_rotation_list else 0
                )

                # процент неротационных исполнителей
                self.set_data(
                    address=f"{column}{row +1}",
                    number_format="#,##0.00",
                    text=percent_not_roatation_executors or "-",
                    sheet=sheet,
                    alignment="center",
                )
                # количество неротационных исполнителей
                self.set_data(
                    address=f"{column_1}{row +1}",
                    text=f'{count_unique_not_rotation_executers or "-"}',
                    sheet=sheet,
                    alignment="center",
                )
                # средний чек неротационных исполнителей
                self.set_data(
                    address=f"{column_2}{row +1}",
                    number_format="#,##0.00₽",
                    text=avg_summ_for_pay_not_rotation or "-",
                    sheet=sheet,
                    alignment="center",
                )
                # сумма оплат неротационных исполнителей
                self.set_data(
                    address=f"{column_3}{row +1}",
                    number_format="#,##0.00₽",
                    text=summ_for_pay_not_rotation or "-",
                    sheet=sheet,
                    alignment="center",
                )

                # процент ротационных исполнителей
                self.set_data(
                    address=f"{column}{row + 2}",
                    number_format="#,##0.00",
                    text=percent_rotation_executors or "-",
                    sheet=sheet,
                    alignment="center",
                )
                # количество ротационных исполнителей
                self.set_data(
                    address=f"{column_1}{row + 2}",
                    text=count_unique_rotation_executers or "-",
                    sheet=sheet,
                    alignment="center",
                )
                # средний чек ротационных исполнителей
                self.set_data(
                    address=f"{column_2}{row +2}",
                    number_format="#,##0.00₽",
                    text=avg_summ_for_pay_rotation or "-",
                    sheet=sheet,
                    alignment="center",
                )
                # сумма оплат ротационных исполнителей
                self.set_data(
                    address=f"{column_3}{row +2}",
                    number_format="#,##0.00₽",
                    text=sum_for_pay_rotation or "-",
                    sheet=sheet,
                    alignment="center",
                )

                # переходим к следующей профессии
                row += 3
            column_number += 4
        # сохраняем и закрываем файл
        self.wb.save(self.path_storage)
        self.wb.close()
        return self.path

    def create_admin_payment_for_coordinators(self, *, tasks, period):
        row = self.first_text
        # открываем нужную страницу
        sheet = self.wb["Координаторы"]

        # ПЕРИОД отчета
        self.set_data(
            address="B1",
            text=f"Отчет координаторы HOOPS Service, {period.lower()}",
            sheet=sheet,
            alignment="center",
            border=True,
        )

        # собираем сводную таблицу
        # список всех админов из заявок
        admins = tasks.exclude(manager__admin=None).values_list("manager__admin", flat=True).distinct()
        admins = set(admins)

        for number, admin in enumerate(admins, 1):
            summ_address = []
            all_sum = 0.0
            tasks_for_current_admin = tasks.filter(manager__admin__id=admin)
            managers = tasks_for_current_admin.values_list("manager", flat=True).distinct()
            managers = set(managers)
            self.set_data(
                address=f"A{row}",
                text=number,
                alignment="center",
                fill=openpyxl.styles.PatternFill(start_color="D9D9D9", end_color="D9D9D9", fill_type="solid"),
                sheet=sheet,
                border=True,
            )
            # имя администратора
            self.set_data(
                address=f"B{row}",
                text=tasks_for_current_admin.last().manager.admin.name,
                alignment="right",
                fill=openpyxl.styles.PatternFill(start_color="D9D9D9", end_color="D9D9D9", fill_type="solid"),
                sheet=sheet,
                border=True,
            )
            # формула премии
            self.set_data(
                address=f"C{row}",
                text=f"=D{row}*E{row}",
                alignment="right",
                number_format="#,##0.00₽",
                fill=openpyxl.styles.PatternFill(start_color="D9D9D9", end_color="D9D9D9", fill_type="solid"),
                sheet=sheet,
                border=True,
            )
            # процент администратора
            self.set_data(
                address=f"D{row}",
                text=tasks_for_current_admin.last().manager.admin.percent / 100,
                alignment="right",
                number_format="#,##0.00%",
                fill=openpyxl.styles.PatternFill(start_color="D9D9D9", end_color="D9D9D9", fill_type="solid"),
                sheet=sheet,
                border=True,
            )

            for number, manager in enumerate(managers):
                tasks_current_manager = tasks_for_current_admin.filter(manager__id=manager)

                cell = sheet.cell(row=row, column=6 + number)
                column = cell.column_letter
                # имя гостиницы
                self.set_data(
                    address=f"{column}{row-1}",
                    text=tasks_current_manager.last().manager.hotel.nameHotel,
                    alignment="center",
                    sheet=sheet,
                    border=True,
                    fill=openpyxl.styles.PatternFill(start_color="DAE1F3", end_color="DAE1F3", fill_type="solid"),
                )
                # имя менеджера
                self.set_data(
                    address=f"{column}{row}",
                    text=tasks_current_manager.last().manager.fullname,
                    alignment="right",
                    sheet=sheet,
                    border=True,
                    fill=openpyxl.styles.PatternFill(start_color="D9D9D9", end_color="D9D9D9", fill_type="solid"),
                )
                sum_tasks = sum(x.full_pay_real for x in tasks_current_manager)
                all_sum += sum_tasks
                summ_address.append(f"{column}{row+1}")

                # выручка
                self.set_data(
                    address=f"{column}{row+1}",
                    text=sum_tasks,
                    alignment="right",
                    number_format="#,##0.00₽",
                    sheet=sheet,
                    border=True,
                )

            # выручка администратора
            self.set_data(
                address=f"E{row}",
                text="=" + "+".join(summ_address),
                alignment="right",
                number_format="#,##0.00₽",
                fill=openpyxl.styles.PatternFill(start_color="D9D9D9", end_color="D9D9D9", fill_type="solid"),
                sheet=sheet,
                border=True,
            )
            row += 3

        # сохраняем и закрываем файл
        self.wb.save(self.path_storage)
        self.wb.close()
        return self.path

    def create_admin_admin_statistic(self, tasks, tasks2, hotels, period, period2=""):
        manager_name = openpyxl.styles.PatternFill(start_color="f2e8cb", end_color="f2e8cb", fill_type="solid")
        hotel_name = openpyxl.styles.PatternFill(start_color="cbddf2", end_color="cbddf2", fill_type="solid")
        row = self.first_text
        # открываем нужную страницу
        sheet = self.wb.active
        sheet.sheet_properties.outlinePr.summaryBelow = False
        # ПЕРИОД отчета
        self.set_data(address="A2", text="Гостиницы", bold=True, sheet=sheet, alignment="center", border=True)
        self.set_data(
            address="B2",
            text=tasks.exclude(executers=None).exclude(personal_profession=None).values("executers").count(),
            sheet=sheet,
            alignment="center",
            border=True,
            bold=True,
        )
        self.set_data(
            address="C2",
            text=tasks2.exclude(executers=None).exclude(personal_profession=None).values("executers").count(),
            sheet=sheet,
            alignment="center",
            border=True,
            bold=True,
        )
        self.set_data(address="D2", text="Разница", bold=True, sheet=sheet, alignment="center", border=True)
        self.set_data(address="E2", text="Координатор", bold=True, sheet=sheet, alignment="center", border=True)
        # ПЕРИОД отчета
        self.set_data(
            address="A1",
            text=f"Отчет HOOPS Service, {period.lower()}, {period2.lower()}",
            sheet=sheet,
            alignment="left",
            border=True,
        )

        grouper_1 = []
        grouper_2 = []
        for hotel in hotels:
            start_group = row
            self.set_data(
                address=f"A{row}",
                text=hotel.nameHotel,
                alignment="center",
                sheet=sheet,
                border=True,
                fill=hotel_name,
                bold=True,
            )
            self.set_data(
                address=f"B{row}",
                text=tasks.exclude(executers=None).filter(manager__hotel=hotel).values("executers").count(),
                alignment="center",
                sheet=sheet,
                bold=True,
                border=True,
                fill=hotel_name,
            )
            self.set_data(
                address=f"C{row}",
                text=tasks2.exclude(executers=None).filter(manager__hotel=hotel).values("executers").count(),
                alignment="center",
                sheet=sheet,
                border=True,
                bold=True,
                fill=hotel_name,
            )
            self.set_data(
                address=f"D{row}",
                text=f"=C{row}-B{row}",
                alignment="center",
                sheet=sheet,
                border=True,
                bold=True,
                fill=hotel_name,
            )
            row += 1
            for manager in hotel.manager_set.filter(is_active=True, status__in=[2, 3]):
                self.set_data(
                    address=f"A{row}",
                    text=manager.fullname or "Нет полного имени",
                    alignment="left",
                    sheet=sheet,
                    border=True,
                    fill=manager_name,
                    size="11",
                )
                self.set_data(
                    address=f"B{row}",
                    text=tasks.exclude(executers=None).filter(manager=manager).values("executers").count(),
                    alignment="center",
                    sheet=sheet,
                    border=True,
                    fill=manager_name,
                )
                self.set_data(
                    address=f"C{row}",
                    text=tasks2.exclude(executers=None).filter(manager=manager).values("executers").count(),
                    alignment="center",
                    sheet=sheet,
                    border=True,
                    fill=manager_name,
                )
                self.set_data(
                    address=f"D{row}",
                    text=f"=C{row}-B{row}",
                    alignment="center",
                    sheet=sheet,
                    border=True,
                    fill=manager_name,
                )
                self.set_data(
                    address=f"E{row}",
                    text=manager.admin.name if manager.admin else "",
                    alignment="left",
                    sheet=sheet,
                    border=True,
                    fill=manager_name,
                )
                row += 1
                start_group_2 = row
                for pp in hotel.personalprofession_set.filter(active=True):

                    self.set_data(
                        address=f"A{row}",
                        text=f"{    pp.name}",
                        alignment="left",
                        sheet=sheet,
                        italic=True,
                        size="11",
                        border=True,
                        indent=3,
                    )
                    self.set_data(
                        address=f"B{row}",
                        text=tasks.exclude(executers=None)
                        .filter(manager=manager, personal_profession=pp)
                        .values("executers")
                        .count(),
                        alignment="center",
                        sheet=sheet,
                        border=True,
                    )
                    self.set_data(
                        address=f"C{row}",
                        text=tasks2.exclude(executers=None)
                        .filter(manager=manager, personal_profession=pp)
                        .values("executers")
                        .count(),
                        alignment="center",
                        sheet=sheet,
                        border=True,
                    )
                    self.set_data(
                        address=f"D{row}", text=f"=C{row}-B{row}", alignment="center", sheet=sheet, border=True
                    )
                    row += 1
                grouper_2.append((start_group_2, row - 1))

            grouper_1.append((start_group + 1, row - 1))

        for group in grouper_1:
            sheet.row_dimensions.group(group[0], group[1], outline_level=1, hidden=True)

        for group2 in grouper_2:
            sheet.row_dimensions.group(group2[0], group2[1], outline_level=2, hidden=True)

        # сохраняем и закрываем файл
        self.wb.save(self.path_storage)
        self.wb.close()
        return self.path

    def create_list_executer_of_task(self, *, task=None):
        """
        Создание списка Исполнителей в заявке
        :param task: Заявка
        :param path: Путь к файлу
        :param time_zone_offset: Смещение по времени из часового пояса
        :return: путь к файлу
        """

        sheet = self.wb["Список"]
        self.set_data(address="A1", text=task.manager.hotel.nameHotel, alignment="center", sheet=sheet, border=True)
        self.set_data(address="A2", text="ФИО", alignment="center", sheet=sheet, border=True)
        self.set_data(address="B2", alignment="center", text="Профессия", sheet=sheet, border=True)
        self.set_data(address="C2", text="Время начала", alignment="center", sheet=sheet, border=True)
        self.set_data(address="D2", text="Дата", alignment="center", sheet=sheet, border=True)

        row = 5
        for executer in task.executers.all():
            # ФИО
            self.set_data(address=f"A{row}", text=executer.executer.full_name, sheet=sheet, border=True)
            # Имя профессии в заявке
            self.set_data(
                address=f"B{row}",
                text=task.profession.name if task.personal_profession is None else task.personal_profession.name,
                sheet=sheet,
                border=True,
            )
            # Время заявки
            self.set_data(
                address=f"C{row}",
                text=self.get_time_with_offset(task.start_at).time(),
                number_format="HH:mm",
                sheet=sheet,
                border=True,
            )
            # Дата заявки
            self.set_data(
                address=f"D{row}",
                text=self.get_time_with_offset(task.start_at).date(),
                number_format="DD.MM.YYYY",
                sheet=sheet,
                border=True,
            )

            row += 1
        self.footer(sheet=sheet, row=row)
        row += 2
        self.set_data(address=f"B{row}", text="Генеральный директор", sheet=sheet)
        self.set_data(address=f"B{row+1}", text="Волков А.В.", sheet=sheet)
        self.stamp_and_signature(anchor=f"C{row}", sheet=sheet)

        # производим добавление футера

        self.wb.save(self.path_storage)
        self.wb.close()
        # server.getUrlForFile(path)
        return self.path


def createListExecuter(*, task=None, path=None, timeoffset: int = -180):
    """
    Создание списка Исполнителей в заявке
    :param task: Заявка
    :param path: Путь к файлу
    :param time_zone_offset: Смещение по времени из часового пояса
    :return: путь к файлу
    """
    server = SH.minioDocuments()

    if os.path.isfile(f"/usr/local/share/minio/{bucket}/{path}"):
        # server.deleteFile(path)
        print(True)
        os.remove(f"/usr/local/share/minio/{bucket}/{path}")
    os.makedirs(os.path.dirname(f"/usr/local/share/minio/{bucket}/{path}"), exist_ok=True)
    copyfile(f"./{core}/scripts/sample/clear.xlsx", f"/usr/local/share/minio/{bucket}/{path}")
    wb = openpyxl.load_workbook(filename=f"/usr/local/share/minio/{bucket}/{path}")

    sheet = wb["Список"]

    sheet["A1"] = task.manager.hotel.nameHotel
    sheet["A3"] = "ФИО"
    sheet["B3"] = "Профессия"
    sheet["C3"] = "Время начала оказания услуги"
    sheet["D3"] = "Дата оказания услуги"
    row = 5
    for executer in task.executers.all():
        if executer.status == "CANCEL_BY_CUSTOMER" or executer.status == "CANCEL_YOURSELF":
            continue
        sheet["A" + str(row)] = (
            executer.executer.middle_name + " " + executer.executer.first_name + " " + executer.executer.second_name
        )

        sheet["B" + str(row)] = (
            task.profession.name if task.personal_profession is None else task.personal_profession.name
        )
        sheet["C" + str(row)] = str(
            ReportBuilder.get_time_with_offset_with_offset(task.start_at, time_zone_offset=timeoffset).time()
        )[:5]
        sheet["D" + str(row)] = ReportBuilder.get_time_with_offset_with_offset(
            task.start_at, time_zone_offset=timeoffset
        ).date()

        row += 1

    if path == None:
        wb.save(rf"./{core}/scripts/sample/openpyxl.xlsx")
    else:
        wb.save(f"/usr/local/share/minio/{bucket}/{path}")
    wb.close()
    server.getUrlForFile(path)

    return path


def executer_payment(executors_for_paid, payment_id=-1):
    server = SH.minioDocuments()

    header = "ФИО;Телефон;Инн;Правовой статус;Номер карты;Наименование услуг;Назначение платежа в банк;ID банка для СБП;Номер телефона для СБП;Сумма\r\n"
    new_line = "{0} {1} {2};7{3};{4};самозанятый;{5};{6};;;;{7}\r\n"

    current_datetime = datetime.now()
    path_return = f"/bills/paid_for_executers/{current_datetime.year}/{current_datetime.month}/{payment_id}.xlsx"
    path_suffix = f"{bucket}{path_return}"
    path_out = f"/usr/local/share/minio/" + path_suffix
    os.makedirs(os.path.dirname(path_out), exist_ok=True)
    copyfile(f"./{core}/scripts/sample/PAYMENT_JUMPPAY.xlsx", path_out)

    wb = openpyxl.load_workbook(filename=path_out)

    sheet = wb["Лист1"]

    row = 2
    for executor in executors_for_paid:

        sheet[f"A{row}"] = executor.contractor.executer.full_name
        # PHONE NUMBER
        sheet[f"B{row}"] = executor.contractor.executer.phone_number_international_format
        # INN
        sheet[f"C{row}"] = executor.contractor.executer.simplerequisite.inn
        # status
        sheet[f"D{row}"] = "самозанятый"
        # bank card
        bank_card = executor.contractor.executer.simplerequisite.card_number
        if bank_card == "":
            bank_card = "0" * 18

        sheet[f"E{row}"] = bank_card
        # description
        sheet[f"G{row}"] = executor.purpose
        # summ
        sheet[f"J{row}"] = executor.amount
        row += 1
    wb.save(path_out)
    wb.close()
    url = server.getUrlForFile(path_out)

    return path_return


def closing_document_invoice(*, tasks, number):
    file = "INVOICE.xlsx"
    server = SH.minioDocuments()
    current_datetime = datetime.now()
    path_return = f"/closing_documents/{tasks[0].manager.hotel.id}/{current_datetime.year}/{current_datetime.month}/{number}.xlsx"

    path_suffix = f"{bucket}{path_return}"
    path_out = f"/usr/local/share/minio/" + path_suffix
    os.makedirs(os.path.dirname(path_out), exist_ok=True)
    copyfile(f"./{core}/scripts/sample/{file}", path_out)
    wb = openpyxl.load_workbook(filename=path_out)
    sheet = wb["Sheet1"]

    sheet["AD2"] = number
    sheet["AS2"] = current_datetime.date().strftime("%d.%m.%y")
    sheet["Z36"] = current_datetime.date().strftime("%d.%m.%y")

    sheet["DS6"] = tasks[0].manager.hotel.nameLegalEntity
    sheet["DS7"] = tasks[0].manager.hotel.coordinates.address
    sheet["DS8"] = f"{tasks[0].manager.hotel.inn}/{tasks[0].manager.hotel.requisites.kpp}"
    sheet["CM45"] = (
        f"{tasks[0].manager.hotel.nameLegalEntity}, {tasks[0].manager.hotel.inn}/{tasks[0].manager.hotel.requisites.kpp}"
    )
    total_rub_for_executer = 0
    total_rub_for_hoops = 0
    total_sec = 0.0
    for task in tasks:
        for executerState in task.executers.all():
            if executerState.status != "STOP":
                raise ValueError(
                    f"В заявке {task.id} у {task.manager.hotel} исполнитель #{executerState.executer.id} "
                    f"{executerState.executer.middle_name} {executerState.executer.first_name} "
                    f"{executerState.executer.second_name} не закончил работать!"
                )
            start_time = executerState.start_at if executerState.start_at is not None else task.start_at
            end_time = (
                executerState.stop_at
                if executerState.stop_at is not None
                else (task.start_at + timedelta(hours=task.duration))
            )
            total_sec += (end_time - start_time).total_seconds()

        total_rub_for_executer += (task.rent * (task.profession.multiplier / 100)) * (total_sec / 3600.0)
        total_rub_for_hoops += (task.rent * ((100 - task.profession.multiplier) / 100)) * (total_sec / 3600.0)

    sheet["DS17"] = total_rub_for_hoops
    sheet["DS18"] = total_rub_for_executer
    sheet["BP17"] = "{:.2f}".format(total_sec / 3600)
    wb.save(path_out)
    wb.close()
    url = server.getUrlForFile(path_out)

    return path_return


def create_blank_with_receipt(*, receipts, to_load_receipts: bool, period: str, hotel_name: str = ""):
    """
    Создание документа с чеками
    @param receipts: чеки для документа
    @param to_load_receipts: флаг выгрузки чеков
    @param period: период документа
    @param hotel_name: имя отеля
    @return: путь к файлу
    """
    server = SH.minioDocuments()
    current_datetime = datetime.now()
    path_return = f"/bills/paid_for_executers/{current_datetime.year}/{current_datetime.month}/{uuid4()}_{receipts[0].payment.id}_BLANK.xlsx"
    path_suffix = f"{bucket}{path_return}"
    path_out = f"/usr/local/share/minio/" + path_suffix
    os.makedirs(os.path.dirname(path_out), exist_ok=True)
    thin_border = Border(
        left=Side(style="thin"), right=Side(style="thin"), top=Side(style="thin"), bottom=Side(style="thin")
    )
    wb = openpyxl.load_workbook(filename=f"./{core}/scripts/sample/RECEIPTS.xlsx")
    # wb = openpyxl.Workbook()
    sheet = wb.active
    sheet[f"A1"] = hotel_name
    sheet[f"D1"] = f"Период {period}"
    row = 3
    if to_load_receipts:
        zip_buffer = io.BytesIO()
        zip_file = zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False)

    for number, executor in enumerate(receipts, 1):
        sheet[f"A{row}"] = number
        sheet[f"A{row}"].border = thin_border
        # full name
        sheet[f"B{row}"] = executor.contractor.executer.full_name
        sheet[f"B{row}"].border = thin_border
        # amount
        sheet[f"C{row}"] = executor.amount
        sheet[f"C{row}"].border = thin_border
        # description
        sheet[f"D{row}"] = executor.purpose
        sheet[f"D{row}"].border = thin_border
        # чек
        sheet[f"E{row}"] = executor.fns_url or ""
        sheet[f"E{row}"].border = thin_border
        if to_load_receipts:
            receipt_buffer = io.BytesIO()
            try:
                res = requests.get(executor.fns_url)
                receipt_buffer.write(res.content)
                receipt_buffer.name = f"Чек {executor.contractor.executer.full_name}_{executor.id}.png"
                zip_file.writestr(receipt_buffer.name, receipt_buffer.getvalue())

            except Exception as e:
                zip_file.close()
                del zip_buffer
                raise ValueError(e)
            finally:
                del receipt_buffer

        row += 1
    if not to_load_receipts:
        wb.save(path_out)
        wb.close()
        url = server.getUrlForFile(path_out)
        return path_return

    report_buffer = io.BytesIO()
    report_buffer.name = "receipts_blank.xlsx"
    wb.save(report_buffer)
    path_return = path_return + ".zip"
    zip_file.writestr(report_buffer.name, report_buffer.getvalue())
    zip_file.close()
    del report_buffer
    server.put(path_return, zip_buffer.getvalue())
    del zip_buffer
    gc.collect()
    return path_return


def create_blank_with_executors(*, executors):
    server = SH.minioDocuments()
    current_datetime = datetime.now()
    path_return = f"/admin/sdjkhfsdfcoiweciic384775387fh9238dj01992d892f/BLANK.xlsx"
    path_suffix = f"{bucket}{path_return}"
    path_out = f"/usr/local/share/minio/" + path_suffix
    os.makedirs(os.path.dirname(path_out), exist_ok=True)

    # wb = openpyxl.load_workbook(filename=path_out)
    wb = openpyxl.Workbook()
    sheet = wb.active

    row = 2
    for executor in executors:
        # Имя
        sheet[f"A{row}"] = executor.full_name
        # Номер телефона
        sheet[f"B{row}"] = executor.phone_number_international_format
        row += 1
    # Сохраняем
    wb.save(path_out)
    wb.close()
    url = server.getUrlForFile(path_out)

    return path_return
