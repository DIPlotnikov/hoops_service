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
a = NumberToRoubles()


class BillCreator(object):
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
              <tr>
        <td style="width:13mm; text-align: center;">{0}</td>

        <td text-align: center;>{1}</td>
        <td style="width:20mm; text-align: center;">{3}</td>

        <td style="width:27mm; text-align: center; ">{4}</td>
        <td style="width:27mm; text-align: center; ">{2}</td>
    </tr>"""

    def __create_pdf(self):
        pdfkit.from_file(self._file_path, os.path.splitext(self._file_path)[0] + ".pdf")
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
        total_sum = sum(float(v) for _, v, _, _ in goods)

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
        """
        Отправка письма с счетом
        @param url: Домен
        @param nds:
        @return: None
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

        pdf = io.BytesIO(pdfkit.from_string(data))
        pdf.name = "HoopsService.pdf"
        del data
        send_bill(email=self._email, file=pdf, url=url)

    def calculateBill(self, rows, offer_date, hoops_cost, executer_cost, total_tax, join_documents=False):
        for_hoops = [x.get_tuple_with_data_for_row_bill_hoops for x in rows]
        for_remuneration = [x.get_tuple_with_data_for_row_bill_hoops_remuneration for x in rows]
        for_hoops.extend(for_remuneration)
        for_executer = [x.get_tuple_with_data_for_row_bill_executer for x in rows]
        if join_documents:
            for_hoops.extend(for_executer)
            self.createBill(verification=False, offer_date=offer_date, goods=for_hoops, is_hoops=True, nds=total_tax)
            file_path_hoops = self.getUrl(pdf=True)
            file_path_hotel = None
        else:
            self.createBill(verification=False, offer_date=offer_date, goods=for_hoops, is_hoops=True, nds=total_tax)
            file_path_hoops = self.getUrl(pdf=True)

            self.createBill(verification=False, offer_date=offer_date, goods=for_executer, postfix_name="/1")
            file_path_hotel = self.getUrl(pdf=True)

        return file_path_hoops, file_path_hotel

    def sendBill(self, pdf=False, url=""):
        if pdf:
            self.__create_pdf()
        send_bill.delay(email=self._email, file=self._file_path, url=url)

    def getUrl(self, pdf=False):
        logger.info(self._file_path.split(bucket)[1])
        if pdf:
            self.__create_pdf()
        server = SH.minioDocuments()
        url = server.getUrlForFile(self._file_path, response_headers={})
        url = self._file_path.split(bucket)[1]
        return url
