import logging
from uuid import uuid4

import requests
from django.conf import settings

logger = logging.getLogger(__name__)


class JumpFinance:
    """
    Взаимодействие с JumpFinance
    """

    __headers = {
        "Client-Key": settings.JUMP_FINANCE_CLIENT_KEY,
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    endpoint = settings.JUMP_FINANCE_ROOT_ENDPOINT

    urls = {
        "create_executor": "contractors",
        "create_payment": "payments",
        "get_payment": "payments",
        "get_executor_selfemployer": "contractors/{}/selfemployer",
        "sync_executor_selfemployer": "contractors/{}/selfemployer/sync",
    }

    def __handler_exception(self, res):
        if res.status_code != 200:
            if not res.headers.get("content-type") == "application/json":
                raise ValueError("Ошибка JumpFinance:" + res.text)
            title = res.json().get("error", {}).get("title", "Ошибка")
            detail = res.json().get("error", {}).get("detail", "неизвестная ошибка")
            code = res.json().get("error", {}).get("code", -1)
            fields = res.json().get("error", {}).get("fields", [])
            uuid = uuid4()
            text_error = f"{title}: {detail} ({code}).\r\nКод ошибки {uuid} \r\n{fields}"

            logger.error(text_error + str(res.json()))
            raise ValueError(text_error)
        return res

    def __get_request(self, url):
        try:
            res = requests.get(self.endpoint + url, headers=self.__headers)
        except Exception as e:
            logger.error(e)
            raise ValueError("Ошибка подключения к JumpFinance")
        return self.__handler_exception(res)

    def __post_request(self, url, data=None):
        if data is None:
            data = {}
        try:
            res = requests.post(self.endpoint + url, json=data, headers=self.__headers)
        except Exception as e:
            logger.error(e)
            raise ValueError("Ошибка подключения к JumpFinance")
        return self.__handler_exception(res)

    def create_executor(self, *, phone, last_name, first_name, miidle_name, inn):
        data = {
            "phone": phone,
            "last_name": last_name,
            "first_name": first_name,
            "middle_name": miidle_name,
            "legal_form_id": 2,  # САМОЗАНЯТЫЙ
            "company_agrees_pay_taxes": True,
            "inn": inn,
            "agent_id": settings.JF_AGENT_ID,  # 10640,
            # "group_id": 1
        }

        res = self.__post_request(self.urls["create_executor"], data=data)
        id_executor_in_jumpfiance = res.json().get("item", {}).get("id", None)
        return id_executor_in_jumpfiance

    def create_payment(self, *, contractor_id: int, account_number: str, amount: int, purpose: str, id_payment: str):
        data = {
            "requisite": {
                "type_id": 8,
                "account_number": account_number,
            },
            "contractor_id": contractor_id,
            # 'customer_payment_id':id_payment,
            "amount": amount,
            "agent_id": settings.JF_AGENT_ID,
            "service_name": purpose,
            "payment_purpose": purpose,
        }

        res = self.__post_request(self.urls["create_payment"], data=data)
        payment_dict = res.json().get("item", {})
        return payment_dict

    def get_payment(self, *, id_payment: str):
        res = self.__get_request(self.urls["create_payment"] + f"/{id_payment}")
        payment_dict = res.json().get("item", {})
        return payment_dict

    def get_status_selfemployer_of_executor(self, *, contractor_id: int) -> dict:
        """
        Запрос статуса Исполнителя в области налоговой (статус самозанятого и тп)
        @param contractor_id: Идентификатор исполнителя в системе JumpFinance
        @return: Сообщение статуса Исполнителя и флаги его состояния
        """
        res = self.__get_request(self.urls.get("get_executor_selfemployer").format(contractor_id))
        status_dict = res.json().get("item", {})
        return status_dict

    def sync_status_selfemployer_of_executor(self, *, contractor_id: int) -> dict:
        """
        Отправляет запрос в налоговую, для того чтобы проверить, подтвердил ли самозанятый необходимые разрешения.
        @param contractor_id: Идентификатор исполнителя в системе JumpFinance
        @return: Сообщение статуса Исполнителя и флаги его состояния
        """
        res = self.__post_request(
            self.urls.get("sync_executor_selfemployer").format(contractor_id),
        )
        status_dict = res.json().get("item", {})
        return status_dict
