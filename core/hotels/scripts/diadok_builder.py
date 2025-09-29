import uuid
from datetime import datetime

from .invoice import RowForInvoice
from .server_handler import minioDocuments as SH


class DiadokBuilder:
    row = """
            <СведТов НомСтр="{0}" НаимТов="Стоимость Услуг HOOPS Service по заявкам № {1}" ОКЕИ_Тов="{2}" КолТов="{3}" ЦенаТов="{4}" СтТовБезНДС="{5}" НалСт="{9}" СтТовУчНал="{6}" НаимЕдИзм="{8}">
                <ДопСведТов />
                <Акциз>
                  <БезАкциз>без акциза</БезАкциз>
                </Акциз>
                <СумНал>
                  <СумНал>{7}</СумНал>
                </СумНал>

            </СведТов>
    """
    row_remuneration = """
            <СведТов НомСтр="{0}" НаимТов="Вознаграждение за исполнение поручения по заявкам № {1}" ОКЕИ_Тов="{2}" КолТов="{3}" ЦенаТов="{4}" СтТовБезНДС="{5}" НалСт="{9}" СтТовУчНал="{6}" НаимЕдИзм="{8}">
                <ДопСведТов />
                <Акциз>
                  <БезАкциз>без акциза</БезАкциз>
                </Акциз>
                <СумНал>
                  <СумНал>{7}</СумНал>
                </СумНал>

            </СведТов>
    """

    end_row = """
            <ВсегоОпл СтТовБезНДСВсего="{0}" СтТовУчНалВсего="{1}">
                <СумНалВсего>
                  <СумНал>{2}</СумНал>
                </СумНалВсего>
            </ВсегоОпл>
    """
    quot = "&quot;"

    sample = "SAMPLE_DIADOK.xml"

    def __init__(self):
        self.document = ""
        with open(f"./hotels/scripts/sample/{self.sample}", "r", encoding="windows-1251") as file:
            self.document = file.read()

        self.storage = SH()

    def create_rows(self, datas, end_data):
        res = ""
        number = 0
        for row in datas:
            number += 1
            res += self.row.format(number, *row.get_tuple_with_data_for_row_diadok_row[1:])
            number += 1
            res += self.row_remuneration.format(number, *row.get_tuple_with_data_for_row_diadok_row_remuneration[1:])
        res += self.end_row.format(*end_data)
        return res

    def create_document(
        self,
        rows,
        total_price,
        number,
        date,
        inn,
        kpp,
        hotel_name,
        legal_address,
        date_offer,
        accepted_date,
        total_tax,
    ):
        file_id = str(uuid.uuid4()) + str(uuid.uuid4())
        path_return = f"closing_document/diadok_xml/{date.year}/{date.month}/{number}/{file_id}.xml"

        self.document = self.document.replace("{FILE_ID}", file_id)
        self.document = self.document.replace("{NUMBER}", str(number))
        self.document = self.document.replace("{DATE}", date.date().strftime("%d.%m.%Y"))
        self.document = self.document.replace("{INN}", inn)
        self.document = self.document.replace("{KPP}", kpp)
        self.document = self.document.replace("{HOTEL_NAME}", hotel_name.replace('"', self.quot))
        self.document = self.document.replace("{LEGAL_ADDRESS}", legal_address)

        rows = self.create_rows(
            rows,
            (
                RowForInvoice.get_str_with_format(total_price - total_tax),
                RowForInvoice.get_str_with_format(total_price),
                RowForInvoice.get_str_with_format(total_tax),
            ),
        )
        self.document = self.document.replace("{PARAGRAPHS}", str(f"1-{len(rows)}"))
        self.document = self.document.replace("{PRODUCT_INFOS}", rows)
        self.document = self.document.replace("{TIME}", datetime.now().time().strftime("%H.%M.%S"))
        self.document = self.document.replace("{DATE_OFFER}", date_offer)
        self.document = self.document.replace("{DATE_OFFER}", date_offer)
        self.document = self.document.replace("{ACCEPTED_DATE}", accepted_date)
        self.document = self.document.replace("{CLOSING_DATE}", date.date().strftime("%d.%m.%Y"))

        self.storage.put(path_return, self.document)

        return path_return, total_price
