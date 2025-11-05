import logging
import os
from datetime import datetime
from shutil import copyfile

import pdfkit
from russian_numerals import NumberToRoubles

from .utils.date_utils import format_period_ru
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
    <tr class=\"no-break-row\">
        <td style=\"text-align: center; border: 1px solid grey;\"><div class=\"cell-content\">{0}</div></td>
        <td style=\"text-align: left; border: 1px solid grey;\"><div class=\"cell-content\">Стоимость Услуг HOOPS Service по заявкам №{1}</div></td>
        <td style=\"text-align: left; border: 1px solid grey;\"><div class=\"cell-content\">{10}</div></td>
        <td style=\"text-align: right; border: 1px solid grey;\"><div class=\"cell-content\">{2}</div></td>
        <td style=\"text-align: right; border: 1px solid grey;\"><div class=\"cell-content\">{3}</div></td>
        <td style=\"text-align: right; border: 1px solid grey;\"><div class=\"cell-content\">{4}</div></td>
        <td style=\"text-align: right; border: 1px solid grey;\"><div class=\"cell-content\">{5}</div></td>
        <td style=\"text-align: right; border: 1px solid grey;\"><div class=\"cell-content\">{6}</div></td>
    </tr>
    <tr class=\"no-break-row\">
        <td style=\"text-align: center; border: 1px solid grey;\"><div class=\"cell-content\">{7}</div></td>
        <td style=\"text-align: left; border: 1px solid grey;\"><div class=\"cell-content\">Вознаграждение за исполнение поручения по заявкам №{1}</div></td>
        <td style=\"text-align: left; border: 1px solid grey;\"><div class=\"cell-content\">{10}</div></td>
        <td style=\"text-align: right; border: 1px solid grey;\"><div class=\"cell-content\">{2}</div></td>
        <td style=\"text-align: right; border: 1px solid grey;\"><div class=\"cell-content\">{12}</div></td>
        <td style=\"text-align: right; border: 1px solid grey;\"><div class=\"cell-content\">{13}</div></td>
        <td style=\"text-align: right; border: 1px solid grey;\"><div class=\"cell-content\">{14}</div></td>
        <td style=\"text-align: right; border: 1px solid grey;\"><div class=\"cell-content\">{15}</div></td>
    </tr>
    <tr class=\"no-break-row\">
        <td style=\"text-align: center; border: 1px solid grey;\"><div class=\"cell-content\">{11}</div></td>
        <td style=\"text-align: left; border: 1px solid grey;\"><div class=\"cell-content\">Оплата HOOPS для выплаты исполнителям согласно раздела 4 договора оферты ред. OFFER_DATE, акцепт ACCEPTED_AT за оказанные услуги по заявкам  №{1}</div></td>
        <td style=\"text-align: left; border: 1px solid grey;\"><div class=\"cell-content\">{10}</div></td>
        <td style=\"text-align: right; border: 1px solid grey;\"><div class=\"cell-content\">{2}</div></td>
        <td style=\"text-align: right; border: 1px solid grey;\"><div class=\"cell-content\">{8}</div></td>
        <td style=\"text-align: right; border: 1px solid grey;\"><div class=\"cell-content\">{9}</div></td>
        <td style=\"text-align: right; border: 1px solid grey;\"><div class=\"cell-content\">Без НДС</div></td>
        <td style=\"text-align: right; border: 1px solid grey;\"><div class=\"cell-content\">{9}</div></td>
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
            "encoding": "UTF-8",
            "print-media-type": None,
            "enable-local-file-access": None,
            "no-stop-slow-scripts": None,
        },
    )

    path_out = os.path.splitext(path_out)[0] + ".pdf"
    path_return = os.path.splitext(path_return)[0] + ".pdf"
    server.getUrlForFile(path_out)

    return path_return, total_price


def act_creator_for_group_cd(
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
    date_start=None,
    date_stop=None,
):

    logger.info("Создание счет фактуры html")
    file = "SAMPLE_ACT_PRIEMKA_GCD.html"
    rows_for_1_task = """
    <table style=\"width: 100%; border-collapse: collapse; page-break-inside: avoid; margin: 0; padding: 0; table-layout: fixed; font-size: 12px;\">
    <tr>
            <td style=\"width:7%; text-align: center; border: 1px solid grey;\"><div class=\"cell-content\">{0}</div></td>
            <td style=\"text-align: left; border: 1px solid grey;\"><div class=\"cell-content\">{1} Оплата услуг HOOPS Service за период {FORMATED_DATE}</div></td>
            <td style=\"width:7%; text-align: left; border: 1px solid grey;\"><div class=\"cell-content\">{10}</div></td>
            <td style=\"width:7%; text-align: right; border: 1px solid grey;\"><div class=\"cell-content\">{2}</div></td>
            <td style=\"width:12.5%; text-align: right; border: 1px solid grey;\"><div class=\"cell-content\">{3}</div></td>
            <td style=\"width:12.5%; text-align: right; border: 1px solid grey;\"><div class=\"cell-content\">{4}</div></td>
            <td style=\"width:15%; text-align: right; border: 1px solid grey;\"><div class=\"cell-content\">{5}</div></td>
            <td style=\"width:15%; text-align: right; border: 1px solid grey;\"><div class=\"cell-content\">{6}</div></td>
    </tr>
    </table>
    <table style=\"width: 100%; border-collapse: collapse; page-break-inside: avoid; margin: 0; padding: 0; table-layout: fixed; font-size: 12px;\">
        <tr>
            <td style=\"width:7%; text-align: center; border: 1px solid grey;\"><div class=\"cell-content\">{7}</div></td>
            <td style=\"text-align: left; border: 1px solid grey;\"><div class=\"cell-content\">{1} Вознаграждение за исполнение поручения за период {FORMATED_DATE}</div></td>
            <td style=\"width:7%; text-align: left; border: 1px solid grey;\"><div class=\"cell-content\">{10}</div></td>
            <td style=\"width:7%; text-align: right; border: 1px solid grey;\"><div class=\"cell-content\">{2}</div></td>
            <td style=\"width:12.5%; text-align: right; border: 1px solid grey;\"><div class=\"cell-content\">{12}</div></td>
            <td style=\"width:12.5%; text-align: right; border: 1px solid grey;\"><div class=\"cell-content\">{13}</div></td>
            <td style=\"width:15%; text-align: right; border: 1px solid grey;\"><div class=\"cell-content\">{14}</div></td>
            <td style=\"width:15%; text-align: right; border: 1px solid grey;\"><div class=\"cell-content\">{15}</div></td>
    </tr>
    </table>
    <table style=\"width: 100%; border-collapse: collapse; page-break-inside: avoid; margin: 0; padding: 0; table-layout: fixed; font-size: 12px;\">
        <tr>
            <td style=\"width:7%; text-align: center; border: 1px solid grey;\"><div class=\"cell-content\">{11}</div></td>
            <td style=\"text-align: left; border: 1px solid grey;\"><div class=\"cell-content\">{1} Оплата HOOPS для выплаты исполнителям за период {FORMATED_DATE}</div></td>
            <td style=\"width:7%; text-align: left; border: 1px solid grey;\"><div class=\"cell-content\">{10}</div></td>
            <td style=\"width:7%; text-align: right; border: 1px solid grey;\"><div class=\"cell-content\">{2}</div></td>
            <td style=\"width:12.5%; text-align: right; border: 1px solid grey;\"><div class=\"cell-content\">{8}</div></td>
            <td style=\"width:12.5%; text-align: right; border: 1px solid grey;\"><div class=\"cell-content\">{9}</div></td>
            <td style=\"width:15%; text-align: right; border: 1px solid grey;\"><div class=\"cell-content\">Без НДС</div></td>
            <td style=\"width:15%; text-align: right; border: 1px solid grey;\"><div class=\"cell-content\">{9}</div></td>
    </tr>
    </table>
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
    formatted_period = format_period_ru(date_start, date_stop)

    for row in rows:
        rows_for_all_task += rows_for_1_task.format(
            number_row,
            *row.get_tuple_with_data_for_row_act_first_row_gcd,
            number_row + 1,
            *row.get_tuple_with_data_for_row_act_second_row_gcd,
            number_row + 2,
            *row.get_tuple_with_data_for_row_act_remenuration_gcd,
            FORMATED_DATE=formatted_period,
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
        },
    )

    path_out = os.path.splitext(path_out)[0] + ".pdf"
    path_return = os.path.splitext(path_return)[0] + ".pdf"
    server.getUrlForFile(path_out)

    return path_return, total_price
