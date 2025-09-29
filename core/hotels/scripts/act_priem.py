import logging
import os
from datetime import datetime
from shutil import copyfile

import pdfkit
from russian_numerals import NumberToRoubles

from ..config import bucket as bucket
from ..config import core as core
from ..scripts import server_handler as SH

a = NumberToRoubles()
logger = logging.getLogger(__name__)


def act_creator(
    *,
    rows,
    number,
    total_tax,
    offer_date,
    accepted_at,
    hotel_name,
    inn,
    kpp,
    address,
    hoops_cost,
    executer_cost,
    signer="",
    closing_date=None,
):

    logger.info("Создание счет фактуры html")
    file = "SAMPLE_ACT_PRIEMKA.html"
    rows_for_1_task = """
    <tr>
        <td style="text-align: center; border: 1px solid grey;">{0}</td>
        <td style="text-align: left; border: 1px solid grey;">Стоимость Услуг HOOPS Service по заявкам №{1}</td>
        <td style="text-align: left; border: 1px solid grey;">{10}</td>
        <td style="text-align: right; border: 1px solid grey;">{2}</td>
        <td style="text-align: right; border: 1px solid grey;">{3}</td>
        <td style="text-align: right; border: 1px solid grey;">{4}</td>
        <td style="text-align: right; border: 1px solid grey;">{5}</td>
        <td style="text-align: right; border: 1px solid grey;">{6}</td>
    </tr>
    <tr>
        <td style="text-align: center; border: 1px solid grey;">{11}</td>
        <td style="text-align: left; border: 1px solid grey;">Вознаграждение за исполнение поручения по заявкам №{1}</td>
        <td style="text-align: left; border: 1px solid grey;">{10}</td>
        <td style="text-align: right; border: 1px solid grey;">{2}</td>
        <td style="text-align: right; border: 1px solid grey;">{12}</td>
        <td style="text-align: right; border: 1px solid grey;">{13}</td>
        <td style="text-align: right; border: 1px solid grey;">{14}</td>
        <td style="text-align: right; border: 1px solid grey;">{15}</td>
    </tr>
    <tr>
        <td style="text-align: center; border: 1px solid grey;">{7}</td>
        <td style="text-align: left; border: 1px solid grey;">Оплата HOOPS для выплаты исполнителям согласно раздела 4 договора оферты ред. OFFER_DATE, акцепт ACCEPTED_AT за оказанные услуги по заявкам  №{1}</td>
        <td style="text-align: left; border: 1px solid grey;">{10}</td>
        <td style="text-align: right; border: 1px solid grey;">{2}</td>
        <td style="text-align: right; border: 1px solid grey;">{8}</td>
        <td style="text-align: right; border: 1px solid grey;">{9}</td>
        <td style="text-align: right; border: 1px solid grey;">Без НДС</td>
        <td style="text-align: right; border: 1px solid grey;">{9}</td>
    </tr>
    """

    rows_for_all_task = ""

    server = SH.minioDocuments()
    current_datetime = closing_date or datetime.now()
    path_return = f"/closing_documents/{inn}/{current_datetime.year}/act_{current_datetime.month}/{number}.html"
    path_suffix = f"{bucket}{path_return}"
    path_out = f"/usr/local/share/minio/" + path_suffix
    os.makedirs(os.path.dirname(path_out), exist_ok=True)
    copyfile(f"./{core}/scripts/sample/{file}", path_out)

    with open(path_out, "r", encoding="utf-8") as file:
        data = file.read()

    number_row = 1

    for row in rows:
        rows_for_all_task += rows_for_1_task.format(
            number_row,
            *row.get_tuple_with_data_for_row_act_first_row,
            number_row + 1,
            *row.get_tuple_with_data_for_row_act_second_row,
            number_row + 2,
            *row.get_tuple_with_data_for_row_act_remenuration,
        )
        number_row += 3

    total_price = hoops_cost + executer_cost

    data = data.replace("{DATA}", rows_for_all_task)
    data = data.replace("{NUMBER}", str(number))
    data = data.replace("{DATE}", current_datetime.date().strftime("%d.%m.%y"))
    data = data.replace("{OFFER}", offer_date)

    data = data.replace("{HOTEL_NAME}", hotel_name)
    data = data.replace("{HOTEL_NAME}", hotel_name)
    data = data.replace("{INN}", inn)
    data = data.replace("{KPP}", kpp)
    data = data.replace("{HOTEL_ADDRESS}", address)

    data = data.replace("{SUM}", "{:.2f}".format(total_price).replace(".", ","))
    data = data.replace("{SUM_TAX}", "{:.2f}".format(total_tax).replace(".", ","))
    data = data.replace("{SUM_WITHOUT_TAX}", "{:.2f}".format(total_price - total_tax).replace(".", ","))

    data = data.replace(
        "{SUM_TEXT}", ("ноль рублей " if int(total_price) == 0 else "") + str(a.prepare("%.2f" % total_price))
    )
    data = data.replace(
        "{SUM_TAX_TEXT}", ("ноль рублей " if int(total_tax) == 0 else "") + str(a.prepare("%.2f" % total_tax))
    )

    data = data.replace("{DAY}", current_datetime.strftime("%d"))
    data = data.replace("{MONTH}", current_datetime.strftime("%m"))
    data = data.replace("{YEAR}", current_datetime.strftime("%Y"))
    data = data.replace("{YEAR}", current_datetime.strftime("%Y"))
    data = data.replace("{PODPISANT}", signer)
    data = data.replace("OFFER_DATE", offer_date)
    data = data.replace("ACCEPTED_AT", accepted_at)

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

    return path_return, total_price
