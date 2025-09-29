from datetime import datetime

from ...config import core

strings_for_footer = [
    "Дата создания отчета: {0}",
    "Отчет является Данными статистики",
    "Отчет составлен Программой HOOPS Service",
    "https://hoopsservice.ru",
    'Правообладатель ООО "Гостиничные ресурсы"',
    "ИНН/КПП 9703086470/770301001",
]


def create_footer(worksheet, position):
    position += 2
    for i, string in enumerate(strings_for_footer):
        position += 1
        worksheet.write(position, 0, string.format(datetime.now().strftime("%d.%m.%Y")))
    return position


def create_stamp_signature(worksheet, position):
    position += 2
    worksheet.write(position, 0, "Генеральный директор")
    worksheet.write(position + 1, 0, "Волков А.В.")

    worksheet.insert_image(position - 3, 2, f"./{core}/scripts/sample/stamp.png")
    worksheet.insert_image(position - 2, 1, f"./{core}/scripts/sample/signature.png")
    worksheet.write(position + 1, 1, "______________")
    return worksheet


def create_footer_and_stamp_signature(worksheet, position):
    position = create_footer(worksheet, position)
    create_stamp_signature(worksheet, position)
    return worksheet



