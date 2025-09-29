from datetime import timedelta

import pandas as pd
from django.db.models import DateTimeField, ExpressionWrapper, F, Value
from django.db.models.functions import Concat

from .utils import create_footer, create_stamp_signature


def executors_list(queryset, period, offset, path):
    adding_start_stop = queryset[0].task.manager.hotel.id == 32
    queryset = queryset.annotate(
        executer_full_name=Concat(
            "executer__middle_name", Value(" "), "executer__first_name", Value(" "), "executer__second_name"
        )
    )
    queryset = queryset.annotate(hotel_name=F("task__manager__hotel__nameHotel"))
    queryset = queryset.annotate(profession_name=F("task__personal_profession__name" or "task__profession__name"))
    queryset = queryset.annotate(
        start_datetime=ExpressionWrapper(F("task__start_at") - timedelta(minutes=offset), output_field=DateTimeField())
    ).order_by("start_datetime")

    additional = {
        "start_at_c": "Время начала",
        "stop_at_c": "Время окончания",
        "signature": "  Питание      ",
    }
    queryset = queryset.annotate(start_at_c=Value(" "))
    queryset = queryset.annotate(stop_at_c=Value(" "))
    queryset = queryset.annotate(signature=Value(" "))

    columns = [
        "hotel_name",
        "executer_full_name",
        "profession_name",
        "start_datetime",
    ]
    columns_df = {
        "executer_full_name": "ФИО Исполнителя",
        "hotel_name": "Гостиница",
        "profession_name": "Наименование профессии",
        "start_datetime": "Время",
        "start_date": "Дата",
    }
    if adding_start_stop:
        columns = columns + list(additional.keys())
        columns_df = {**columns_df, **additional}
    df = pd.DataFrame(queryset.values(*columns))
    df = df.reset_index(drop=True)
    df.index += 1

    df["start_date"] = df["start_datetime"].dt.strftime("%d.%m.%Y")
    df["start_datetime"] = df["start_datetime"].dt.strftime("%H:%M")
    df = df[columns_df.keys()]
    df = df.rename(columns=columns_df)
    max_row = df.shape[0] + 1
    writer = pd.ExcelWriter(path, engine="xlsxwriter")
    df.to_excel(
        writer,
        sheet_name="Список исполнителей",
        startrow=1,
    )
    worksheet = writer.sheets["Список исполнителей"]
    # worksheet.set_default_row(height=15, hide_unused_rows=True)
    worksheet.autofit()
    worksheet.autofilter("B2:E2")
    worksheet.merge_range(0, 2, 0, 3, data=period)

    max_row, max_col = df.shape
    max_col -= 1
    max_row += 1

    border = writer.book.add_format(
        {
            "border": 1,
        }
    )
    worksheet.conditional_format(
        2,
        0,
        max_row,
        max_col + 1,
        {"type": "no_errors", "format": border},
    )

    new_posititon = create_footer(worksheet, max_row)
    create_stamp_signature(worksheet, new_posititon)
    writer.close()
    return path
