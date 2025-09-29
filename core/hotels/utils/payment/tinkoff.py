import hashlib
import logging

import requests
from django.conf import settings

logger = logging.getLogger(__name__)


class TinkoffPayment(object):
    def __init__(self):
        self.__url = settings.TINKOFF_PAYMENT_URL
        self.__url_cancel = settings.TINKOFF_PAYMENT_CANCEL_URL
        self.__password_terminal = settings.PASSWORD_TERMINAL
        self.__terminal_key = settings.TERMINAL_KEY
        self.name = "Акцепт оферты и проверка данных ЛК"

    def __sign(self):
        sign_str = f"{str(self.payment_dict.get('Amount',''))}{self.payment_dict.get('Description','')}{self.payment_dict.get('OrderId','')}{self.__password_terminal}{self.payment_dict.get('PaymentId','')}{self.__terminal_key}"
        hash_object = hashlib.sha256(bytes(sign_str, "utf-8"))
        sign = hash_object.hexdigest()
        self.payment_dict["Token"] = sign

    def create(
        self,
        *,
        full_name: str,
        order_id: str,
        phone: str,
        email: str,
        success_url: str = "https://e.dev.hoopsservice.ru",
        success_path: str = "",
    ):
        self.payment_dict = {
            "TerminalKey": self.__terminal_key,
            "Amount": 1100,
            "OrderId": order_id,
            "Description": f"{self.name}: {full_name}",
            "SuccessURL": f"{success_url}{success_path}{order_id}",
            "PayType": "T",
            "Receipt": {
                "Email": email.strip(),
                "Phone": f"+7{phone}",
                "Taxation": "osn",
                "Items": [
                    {
                        "Name": full_name,
                        "Price": 1100,
                        "Quantity": 1.00,
                        "Amount": 1100,
                        "PaymentObject": "payment",
                        "Tax": "vat20",
                    },
                ],
            },
        }

        self.__sign()

    def cancel_by_payment_id(self, payment_id):
        self.payment_dict = {
            "TerminalKey": self.__terminal_key,
            "PaymentId": payment_id,
        }
        self.__sign()

        res = requests.post(self.__url_cancel, json=self.payment_dict, verify=settings.RUSSIAN_TRUST)
        assert res.status_code == 200, "Ошибка проверки оплаты!"
        return res.text

    def send(self):
        res = requests.post(self.__url, json=self.payment_dict, verify=settings.RUSSIAN_TRUST)
        data = res.json()
        return data
