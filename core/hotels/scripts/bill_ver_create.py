"""Модуль генерации счетов (HTML/PDF) для HOOPS и Исполнителей.

Зависимость:
 - pdfkit: конвертация HTML -> PDF (требуется wkhtmltopdf в системе).
 - russian_numerals.NumberToRoubles: преобразование чисел в пропись (рубли/копейки).
 - ..scripts.server_handler (SH): работа с MinIO (ссылки/доступ к файлам).
 - ..tasks.send_bill: отправка счета по email (Celery задача).
 - ..config.bucket/core: конфигурация бакета и префиксов путей.

Использование:
 - См. `core/closing_documents/mutation.py` → `CreateClosingDocument` → `BillCreator.calculateBill()`.
"""
import io
import logging
import os
from datetime import datetime

import pdfkit

# числительные на русском
from russian_numerals import NumberToRoubles

from ..config import bucket as bucket
from ..config import core as core
from ..scripts import server_handler as SH
from ..tasks import send_bill

# падежи от числительных

logger = logging.getLogger(__name__)
a = NumberToRoubles()  # Конвертер суммы в строковое представление (рубли/копейки) на русском


class BillCreator(object):
    """Класс для генерации HTML/PDF счетов и ссылок на них в MinIO.

    Параметры конструктора:
    - number: номер счета (обычно ID платежа/документа в БД).
    - email: email получателя счета.
    - ur_name: юр. наименование компании.
    - adress: юридический адрес.
    - inn: ИНН.
    - kpp: КПП (может быть пустым для ИП).
    - phone: контактный телефон.
    - closing_date: дата закрытия периода (если не задана — текущее время).
    """
    def __init__(
        self,
        *,
        number: str = "1",
        email: str,
        ur_name: str,
        adress: str,
        inn: str,
        kpp: str,
        phone: str,
        closing_date=None,
    ):
        self._email = email
        self._number = number
        self._ur_name = ur_name
        self._adress = adress
        self._inn = inn
        self._kpp = kpp
        self._phone = phone

        if closing_date is None:
            self.closing_date = datetime.now()
        else:
            self.closing_date = closing_date
        self._total_rub = 1.00
        self._goods_html_ = """
              <tr class=\"no-break-row\">
        <td style=\"width:13mm; text-align: center;\"><div class=\"cell-content\">{0}</div></td>
        <td style=\"text-align: center;\"><div class=\"cell-content\">{1}</div></td>
        <td style=\"width:20mm; text-align: center;\"><div class=\"cell-content\">{3}</div></td>
        <td style=\"width:27mm; text-align: center;\"><div class=\"cell-content\">{4}</div></td>
        <td style=\"width:27mm; text-align: center;\"><div class=\"cell-content\">{2}</div></td>
    </tr>"""

    def __create_pdf(self, for_group=False):
        """Конвертирует текущий HTML-файл счета в PDF рядом с ним и обновляет `_file_path`."""
        if for_group:
            # Формат для CreateGroupedClosingDocuments: A4 книжная, отступы 2 см
            options = {
                "page-size": "A4",
                "orientation": "Portrait",
                "margin-top": "2cm",
                "margin-right": "2cm",
                "margin-bottom": "2cm",
                "margin-left": "2cm",
                "encoding": "UTF-8",
                "print-media-type": None,
                "enable-local-file-access": None,
                "no-stop-slow-scripts": None,
            }
        else:
            # Формат для CreateClosingDocument: Letter, старые отступы
            options = {
                "page-size": "Letter",
                "margin-top": "0.2in",
                "margin-right": "0.75in",
                "margin-bottom": "0.2in",
                "margin-left": "0.75in",
                "encoding": "UTF-8",
                "print-media-type": None,
                "enable-local-file-access": None,
                "no-stop-slow-scripts": None,
            }
        
        pdfkit.from_file(
            self._file_path,
            os.path.splitext(self._file_path)[0] + ".pdf",
            options=options,
        )
        self._file_path = os.path.splitext(self._file_path)[0] + ".pdf"

    def createBill(
        self,
        path_from: str = f"./{core}/scripts/sample/bill.html",
        path_to: str = f"/usr/local/share/minio/{bucket}/bills",
        object: str = "hotel",
        verification: bool = True,
        nds: float = 0.0,
        goods=None,
        is_hoops: bool = False,
        offer_date="",
        postfix_name="",
    ):
        """Рендерит HTML счета на основе шаблона и сохраняет его в MinIO FS.

        - Если `verification=True`, создается счет на подтверждение реквизитов (1 позиция на 1 рубль).
        - Для реальных платежей формируется путь вида `.../payment/{YYYY}/{M}/{number}/{suffix}_{number}.html`,
          где `suffix` = `hops` (HOOPS) или `executer` (Исполнители). В шапке к номеру может добавляться `postfix_name`.
        """
        if goods is None:
            goods = [("Подтверждение реквизитов организации и акцепт договора-оферты", 1.00, 1, 1)]
        if verification:
            self._file_path = os.path.join(path_to, object, self._number, "bill.html")
        else:
            current_datetime = self.closing_date
            suffix = "hops" if is_hoops else "executer"
            self._file_path = os.path.join(
                path_to,
                object,
                "payment",
                str(current_datetime.year),
                str(current_datetime.month),
                self._number,
                f"{suffix}_{self._number}.html",
            )
            logger.info(suffix)
            logger.info(self._file_path)

        os.makedirs(os.path.dirname(self._file_path), exist_ok=True)
        # [GROUP-CLOSING-DOCS] Обработка списка goods для нескольких организаций
        # goods — список строк (tuple) для всех организаций, уже собранный на этапе мутации
        total_sum = sum(float(v) for _, v, _, _ in goods)  # суммарная стоимость по всем строкам
        with open(path_from, "r") as file:
            data = file.read()
        data = data.replace("{NUMBER}", self._number + postfix_name)
        data = data.replace("{DATE}", self.closing_date.strftime("%d.%m.%Y"))
        data = data.replace("{UR NAME}", self._ur_name)
        data = data.replace("{INN}", self._inn)
        data = data.replace("{KPP}", self._kpp)
        data = data.replace("{ADDRES}", self._adress)
        data = data.replace("{PHONE NUMBER}", self._phone)
        data = data.replace("{TOTAL_SUM_float}", ("%.2f" % total_sum).replace(".", ","))
        data = data.replace(
            "{TOTAL_SUM_string}",
            (a.prepare("%.2f" % total_sum).capitalize()) + (" 00 копеек" if total_sum % 1 == 0 else ""),
        )
        data = data.replace("{NDS_float}", ("%.2f" % nds).replace(".", ","))
        data = data.replace("{NDS_string}", ("ноль рублей " if int(nds) == 0 else "") + str(a.prepare("%.2f" % nds)))

        data = data.replace(
            "{GOODS_TR}",
            "".join(
                self._goods_html_.format(count, good[0], "{:.2f}".format(good[1]).replace(".", ","), good[2], good[3])
                for count, good in enumerate(goods, start=1)
            ),
        )
        data = data.replace("{GOODS_COUNT}", str(len(goods)))
        data = data.replace("{DATE_OFFER}", offer_date)
        with open(self._file_path, "w") as file:
            file.write(data)

    def send_bill_for_verification(self, url, nds):
        """Формирует счет для проверки реквизитов и отправляет его PDF по email.

        Параметры:
        - url: домен/база для формирования ссылок в письме.
        - nds: сумма НДС, отображаемая в документе.
        """
        path_from = f"./{core}/scripts/sample/bill.html"
        goods = ("Подтверждение реквизитов организации и акцепт договора-оферты", 1.00, 1, 1)

        with open(path_from, "r") as file:
            data = file.read()
        data = data.replace("{NUMBER}", self._number)
        data = data.replace("{DATE}", self.closing_date.strftime("%d.%m.%Y"))
        data = data.replace("{UR NAME}", self._ur_name)
        data = data.replace("{INN}", self._inn)
        data = data.replace("{KPP}", self._kpp)
        data = data.replace("{ADDRES}", self._adress)
        data = data.replace("{PHONE NUMBER}", self._phone)
        data = data.replace("{TOTAL_SUM_float}", "1,00")
        data = data.replace("{TOTAL_SUM_string}", (a.prepare(1.00).capitalize()) + " 00 копеек")
        data = data.replace("{NDS_float}", ("%.2f" % nds).replace(".", ","))
        data = data.replace("{NDS_string}", ("ноль рублей " if int(nds) == 0 else "") + str(a.prepare("%.2f" % nds)))

        data = data.replace("{GOODS_TR}", self._goods_html_.format(1, goods[0], "1,00", goods[2], goods[3]))

        data = data.replace("{GOODS_COUNT}", "1")
        data = data.replace("{DATE_OFFER}", "")

        pdf = io.BytesIO(pdfkit.from_string(data))  # генерируем PDF из HTML-строки (без сохранения HTML на диск)
        pdf.name = "HoopsService.pdf"
        del data
        send_bill(email=self._email, file=pdf, url=url)

    def calculateBill(self, rows, offer_date, hoops_cost=None, executer_cost=None, total_tax=None, join_documents=False, for_group=False):
        """Формирует объединенный или раздельные счета по данным `rows` и возвращает пути к файлам (PDF).

        - rows: объекты с данными для строк счета; должны иметь свойства:
          `get_tuple_with_data_for_row_bill_hoops`,
          `get_tuple_with_data_for_row_bill_hoops_remuneration`,
          `get_tuple_with_data_for_row_bill_executer`.
        - join_documents: если True — формируется один объединенный счет (только HOOPS путь возвращается).
        - for_group: если True — использует формат A4 для CreateGroupedClosingDocuments.
        """
        # Примечание: параметры `hoops_cost` и `executer_cost` не используются внутри метода,
        # оставлены для обратной совместимости вызовов.
        # Собираем строки в нужном для типа документа формате
        if not for_group:
            for_hoops = [x.get_tuple_with_data_for_row_bill_hoops for x in rows]
            for_remuneration = [x.get_tuple_with_data_for_row_bill_hoops_remuneration for x in rows]
            for_hoops.extend(for_remuneration)
            for_executer = [x.get_tuple_with_data_for_row_bill_executer for x in rows]
        else:
            for_hoops = [x.get_tuple_with_data_for_row_bill_hoops_group_cd for x in rows]
            for_remuneration = [x.get_tuple_with_data_for_row_bill_hoops_remuneration_for_group_cd for x in rows]
            for_hoops.extend(for_remuneration)
            for_executer = [x.get_tuple_with_data_for_row_bill_executer_for_group_cd for x in rows]

        if join_documents:
            for_hoops.extend(for_executer)
            self.createBill(verification=False, offer_date=offer_date, goods=for_hoops, is_hoops=True, nds=total_tax)
            file_path_hoops = self.getUrl(pdf=True, for_group=for_group)
            file_path_hotel = None
        else:
            self.createBill(verification=False, offer_date=offer_date, goods=for_hoops, is_hoops=True, nds=total_tax)
            file_path_hoops = self.getUrl(pdf=True, for_group=for_group)

            self.createBill(verification=False, offer_date=offer_date, goods=for_executer, postfix_name="/1")
            file_path_hotel = self.getUrl(pdf=True, for_group=for_group)

        return file_path_hoops, file_path_hotel

    def sendBill(self, pdf=False, url="", for_group=False):
        """Отправляет счет по email; опционально сначала генерирует PDF."""
        if pdf:
            self.__create_pdf(for_group=for_group)
        send_bill.delay(email=self._email, file=self._file_path, url=url)

    def getUrl(self, pdf=False, for_group=False):
        """Возвращает относительный путь внутри бакета к текущему файлу; при `pdf=True` — сначала создает PDF."""
        logger.info(self._file_path.split(bucket)[1])
        if pdf:
            self.__create_pdf(for_group=for_group)
        server = SH.minioDocuments()
        url = server.getUrlForFile(self._file_path, response_headers={})
        url = self._file_path.split(bucket)[1]
        return url

