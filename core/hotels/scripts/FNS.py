from datetime import datetime

import requests


def check_inn_selfwork(inn: str) -> str:
    """
    Запрос в ФНС на статус самозанятого по ИНН
    :param inn: ИНН
    :return: Результат в виде строки для отображения
    """
    # ендпоинт запроса
    url = "https://statusnpd.nalog.ru/api/v1/tracker/taxpayer_status"
    # тело запроса
    data = {"inn": inn, "requestDate": datetime.now().date().isoformat()}
    # делаем запрос
    res = requests.post(url, json=data, timeout=30)
    # json результата
    res_json = res.json()
    # получаем статус проверки - по умолчанию False (не успех)
    status = res_json.get("status", False)
    # получаем текст результата
    message = res_json.get("message", "Проблема в опросе ФНС")
    # формируем результат
    return message if status else f"Ошибка: {message}"
