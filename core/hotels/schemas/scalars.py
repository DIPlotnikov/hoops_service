import re
from datetime import datetime

from graphene.types import Scalar

from ..scripts import exception_handler as EH


class OGRN(Scalar):
    """ОГРН: 13 символов"""

    @staticmethod
    def serialize(value):
        print(value)
        print(type(value))
        return re.search("^\d{13,15}$", value)[0]

    @staticmethod
    def parse_literal(ast):
        res = re.search("^\d{13,15}$", ast.value)
        if res:
            return str(res[0])
        else:
            raise EH.customError("Ошибка", f"не правильная длина ОГРН (13 или 15)")

    @staticmethod
    def parse_value(value):
        res = re.search("^\d{13,15}$", value)
        if res:
            return str(res[0])
        else:
            raise EH.customError("Ошибка", f"не правильная длина ОГРН (13 или 15)")


class INNBank(Scalar):
    """ОГРН: 13 символов"""

    @staticmethod
    def serialize(value):
        print(value)
        print(type(value))
        return re.search("^\d{10,12}$", value)[0]

    @staticmethod
    def parse_literal(ast):
        res = re.search("^\d{10,12}$", ast.value)
        if res:
            return str(res[0])
        else:
            raise EH.customError("Ошибка", f"не правильная длина ИНН банка (10)")

    @staticmethod
    def parse_value(value):
        res = re.search("^\d{10,12}$", value)
        if res:
            return str(res[0])
        else:
            raise EH.customError("Ошибка", f"не правильная длина ИНН банка (10)")


class PaymentBill(INNBank):
    """Расчетный счет: 20 цифр"""

    @staticmethod
    def serialize(value):
        return re.search("^\d{20}$", value)[0]

    @staticmethod
    def parse_literal(ast):
        res = re.search("^\d{20}$", ast.value)
        if res:
            print(res[0])
            return str(res[0])
        else:
            raise EH.customError("Ошибка", f"не правильная длина счета (20)")

    @staticmethod
    def parse_value(value):
        res = re.search("^\d{20}$", value)
        if res:
            return str(res[0])
        else:
            raise EH.customError("Ошибка", f"не правильная длина счета (20)")


class CorrectBill(PaymentBill):
    """Кор счет: 20 цифр"""

    pass


class KPP(INNBank):
    "КПП: 9 цифр"

    @staticmethod
    def serialize(value):
        return re.search("^\d{9}$", value)[0]

    @staticmethod
    def parse_literal(ast):
        res = re.search("^\d{9}$", ast.value)
        if res:
            return str(res[0])
        else:
            raise EH.customError("Ошибка", f"не правильная длина КПП (9)")

    @staticmethod
    def parse_value(value):
        res = re.search("^\d{9}$", value)
        if res:
            return str(res[0])
        else:
            raise EH.customError("Ошибка", f"не правильная длина КПП (9)")


class BIK(KPP):
    """БИК: 9 цифр"""

    @staticmethod
    def parse_literal(ast):
        res = re.search("^\d{9}$", ast.value)
        if res:
            return str(res[0])
        else:
            raise EH.customError("Ошибка", f"не правильная длина БИК (9)")


class INN(INNBank):
    """ИНН: 12 цифр"""

    @staticmethod
    def serialize(value):
        return re.search("^\d{10,12}$", value)[0]

    @staticmethod
    def parse_literal(ast):
        res = re.search(r"^\d{10,12}$", ast.value)
        if res:
            return str(res[0])
        else:
            raise ValueError("Ошибка: не правильная длина ИНН (10-12)")

    @staticmethod
    def parse_value(value):
        res = re.search("^\d{10,12}$", value)
        if res:
            return str(res[0])
        else:
            raise ValueError("Ошибка: не правильная длина ИНН (10-12)")


class Phonenumber(Scalar):
    """номер телефона: 11 цифр, формат 79xxxxxxxxx"""

    @staticmethod
    def serialize(value):
        return re.search("^9\d{9}$", value)[0]

    @staticmethod
    def parse_literal(ast):
        res = re.search(r"^9\d{9}$", ast.value)
        if res:
            return str(res[0])
        else:
            raise EH.customError("Ошибка", f"формат номера телефона: 9xxxxxxx!")

    @staticmethod
    def parse_value(value):
        return str(value)


class Email(Scalar):
    @staticmethod
    def serialize(value):
        return re.search(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", value)[0]

    @staticmethod
    def parse_literal(ast):
        res = re.search(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", ast.value)
        if res:
            return str(res[0])
        else:
            raise EH.customError("Ошибка", f"неверный формат e-mail адреса")

    @staticmethod
    def parse_value(value):
        return str(value)


class BirthDate(Scalar):
    @staticmethod
    def serialize(value):
        print("value3")
        return re.search(r"^\d{4}\-\d{2}\-\d{2}$", value)[0]

    @staticmethod
    def parse_literal(ast):
        print("value2")
        res = re.search(r"^\d{4}\-\d{2}\-\d{2}$", ast.value)
        if res:
            return str(res[0])
        else:
            raise EH.customError("Ошибка", f"введите корректную дату формата ГГГГ-ММ-ДД")

    @staticmethod
    def parse_value(value):
        res = re.search(r"^\d{4}\-\d{2}\-\d{2}$", value)
        if res:
            return res[0]
        else:
            raise EH.customError("Ошибка", f"введите корректную дату формата ГГГГ-ММ-ДД")


class PassportDate(BirthDate):

    @staticmethod
    def serialize(value):
        return datetime.strptime((re.search(r"^\d{4}\-\d{2}\-\d{2}$", value)[0]), "%Y-%m-%d").date()

    @staticmethod
    def parse_literal(ast):
        res = re.search(r"^\d{4}\-\d{2}\-\d{2}$", ast.value)
        if res:
            return datetime.strptime(str(res[0]), "%Y-%m-%d").date()
        else:
            raise EH.customError("Ошибка", f"введите корректную дату формата ДД.ММ.ГГГГ")

    @staticmethod
    def parse_value(value):
        res = re.search(r"^\d{4}\-\d{2}\-\d{2}$", value)
        if res:
            return datetime.strptime(res[0], "%Y-%m-%d").date()
        else:
            raise EH.customError("Ошибка", f"введите корректную дату формата ДД.ММ.ГГГГ")


class SubdivisionCode(Scalar):
    @staticmethod
    def serialize(value):
        res = re.search(r"^\d{6}$", value)
        if res:
            return str(res[0])
        else:
            raise EH.customError("Ошибка", f"введите корректный код формата XXXXXX")

    @staticmethod
    def parse_literal(ast):
        res = re.search(r"^\d{6}$", ast.value)
        if res:
            return str(res[0])
        else:
            raise EH.customError("Ошибка", f"введите корректный код формата XXXXXX")

    @staticmethod
    def parse_value(value):
        res = re.search(r"^\d{6}$", value)
        if res:
            return str(res[0])
        else:
            raise EH.customError("Ошибка", f"введите корректный код формата XXXXXX")


class PassportSeries(Scalar):
    @staticmethod
    def serialize(value):
        return int(re.search(r"^\d{4}$", value)[0])

    @staticmethod
    def parse_literal(ast):
        res = re.search(r"^\d{4}$", ast.value)
        if res:
            return int(str(res[0]))
        else:
            raise EH.customError("Ошибка", f"введите корректную серию паспорта")

    @staticmethod
    def parse_value(value):
        res = re.search(r"^\d{4}$", value)
        if res:
            return int(res[0])
        else:
            raise EH.customError("Ошибка", f"введите корректную серию паспорта")


class PassportNumber(Scalar):
    @staticmethod
    def serialize(value):
        return int(re.search(r"^\d{6}$", value)[0])

    @staticmethod
    def parse_literal(ast):
        res = re.search(r"^\d{6}$", ast.value)
        if res:
            return int(res[0])
        else:
            raise EH.customError("Ошибка", f"введите корректный номер паспорта")

    @staticmethod
    def parse_value(value):
        res = re.search(r"^\d{6}$", value)
        if res:
            return int(res[0])
        else:
            raise EH.customError("Ошибка", f"введите корректный номер паспорта")


class PostalCode(Scalar):
    @staticmethod
    def serialize(value):
        return int(re.search(r"^\d{6}$", value)[0])

    @staticmethod
    def parse_literal(ast):
        res = re.search(r"^\d{6}$", ast.value)
        if res:
            return int(str(res[0]))
        else:
            raise EH.customError("Ошибка", f"введите корректный индекс (6 цифр)")

    @staticmethod
    def parse_value(value):
        res = re.search(r"^\d{6}$", value)
        if res:
            return int(res[0])
        else:
            raise EH.customError("Ошибка", f"введите корректный индекс (6 цифр)")


class CardNumber(Scalar):
    @staticmethod
    def serialize(value):
        res = re.search(r"^\d{12,20}$", value)
        if res:
            return res[0]
        else:
            raise ValueError(f"введите корректный номер карты (12-20 цифр)")

    @staticmethod
    def parse_literal(ast):
        res = re.search(r"^\d{12,20}$", ast.value)
        if res:
            return str(res[0])
        else:
            raise ValueError(f"введите корректный номер карты (12-20 цифр)")

    @staticmethod
    def parse_value(value):
        res = re.search(r"^\d{12,20}$", value)
        if res:
            return res[0]
        else:
            raise ValueError(f"введите корректный номер карты (12-20 цифр)")


def validate_inn(inn: str) -> bool:
    # Проверка контрольной суммы
    n1 = int(inn[0])
    n2 = int(inn[1])
    n3 = int(inn[2])
    n4 = int(inn[3])
    n5 = int(inn[4])
    n6 = int(inn[5])
    n7 = int(inn[6])
    n8 = int(inn[7])
    n9 = int(inn[8])
    n10 = int(inn[9])
    n11 = int(inn[10])
    n12 = int(inn[11])

    m1 = 7 * n1 + 2 * n2 + 4 * n3 + 10 * n4 + 3 * n5 + 5 * n6 + 9 * n7 + 4 * n8 + 6 * n9 + 8 * n10
    m1_mod_11 = m1 % 11
    check_digit1 = m1_mod_11 if m1_mod_11 < 10 else 0

    if check_digit1 != n11:
        return False

    m2 = 3 * n1 + 7 * n2 + 2 * n3 + 4 * n4 + 10 * n5 + 3 * n6 + 5 * n7 + 9 * n8 + 4 * n9 + 6 * n10 + 8 * n11
    m2_mod_11 = m2 % 11
    check_digit2 = m2_mod_11 if m2_mod_11 < 10 else 0

    if check_digit2 != n12:
        return False

    return True


if __name__ == "__main__":
    print(validate_inn("666000569105"))
