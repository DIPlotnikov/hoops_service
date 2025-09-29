import logging
import os
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from io import BytesIO
from os.path import basename
from typing import List, Union

import requests
from core.celery import app
from django.conf import settings

from .utils.fcm.fcm_utils import FcmUtils

logger = logging.getLogger(__name__)


@app.task
def send_simple_message(*, email, Name="", url: str, text=""):
    fromaddr = os.getenv("EMAIL_REGISTRATION_FROM")
    toaddr = email
    mypass = os.getenv("EMAIL_REGISTRATION_FROM_PASSWORD")

    assert all(
        [fromaddr, toaddr, mypass]
    ), "EMAIL_REGISTRATION_FROM, EMAIL_REGISTRATION_FROM_PASSWORD, EMAIL_REGISTRATION_TO must be set"

    msg = MIMEMultipart()
    msg["From"] = f"HOOPS <{fromaddr}>"

    msg["To"] = toaddr
    msg["Subject"] = "Добро пожаловать в HOOPS!"

    body = f"Привет! Вас пригласили в HOOPS Work! Для подтверждения регистрации перейдите по ссылке {url}/verification/{text}/{toaddr} :)"
    msg.attach(MIMEText(body, "plain"))

    server = smtplib.SMTP_SSL(host="smtp.mail.ru", port=465)
    server.login(fromaddr, mypass)

    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()


@app.task
def send_recovery_message(*, email, Name="", url: str, text=""):
    fromaddr = os.getenv("EMAIL_REGISTRATION_FROM")
    toaddr = email
    mypass = os.getenv("EMAIL_REGISTRATION_FROM_PASSWORD")
    assert all(
        [fromaddr, toaddr, mypass]
    ), "EMAIL_REGISTRATION_FROM, EMAIL_REGISTRATION_FROM_PASSWORD, EMAIL_REGISTRATION_TO must be set"

    msg = MIMEMultipart()
    msg["From"] = f"HOOPS <{fromaddr}>"

    msg["To"] = toaddr
    msg["Subject"] = "Восстановление пароля"

    body = (
        f"Привет! На Ваши данные поступил запрос восстановления пароля. Для установки нового пароля - перейдите по ссылке {url}/recovery/confirm/{text}/{toaddr} :)"
        f"\r Если Вы не запрашивали восстановление пароля - проигнорируйте данное сообщение!"
    )

    msg.attach(MIMEText(body, "plain"))

    server = smtplib.SMTP_SSL(host="smtp.mail.ru", port=465)
    server.login(fromaddr, mypass)

    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()


@app.task
def send_bill(*, email, file: Union[str, BytesIO], url: str):
    fromaddr = os.getenv("EMAIL_PAYMENT_FROM")
    toaddr = email
    mypass = os.getenv("EMAIL_PAYMENT_FROM_PASSWORD")

    assert all(
        [fromaddr, toaddr, mypass]
    ), "EMAIL_PAYMENT_FROM, EMAIL_PAYMENT_FROM_PASSWORD, EMAIL_PAYMENT_TO must be set"

    msg = MIMEMultipart()
    msg["From"] = f"HOOPS <{fromaddr}>"
    msg["To"] = toaddr
    msg["Subject"] = "Новый счет от HOOPS!"

    msg_html = MIMEText(
        f"""Привет! Для подтверждения указанных реквизитов в профиле необходимо оплатить счёт :)

        <p>С уважением, команда HOOPS Hotel Operation Supply</p><p><a href="{url}"><img src="https://api.hoopsservice.ru/hoops/media/banner.jpg" alt="ss"/> </a></p>""",
        "html",
    )
    msg.attach(msg_html)

    if type(file) == str:
        with open(file, "rb") as fil:
            part = MIMEApplication(fil.read(), Name=basename(file))
            part["Content-Disposition"] = 'attachment; filename="%s"' % basename(file)
    else:
        part = MIMEApplication(file.read(), Name=basename(file.name))
        part["Content-Disposition"] = 'attachment; filename="%s"' % basename(file.name)
    msg.attach(part)

    server = smtplib.SMTP_SSL(host="smtp.mail.ru", port=465)
    server.login(fromaddr, mypass)

    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()


# @app.task(name='sendSMS')
def send_sms_code(*, code: int, phonenumber: str, sender: str = "hoopswork") -> None:
    name = "HOOPS"
    pswd = os.getenv("SMSC_RU_PASSWORD")
    url = f"https://smsc.ru/sys/send.php?login={name}&psw={pswd}&phones=7{phonenumber}&mes=HOOPS code: {code}&sender={sender}"
    res = requests.get(url)
    logger.info(f"phonenumber:{phonenumber},code:{code},result:{res.text}")


@app.task(name="send_push_by_fcm_token")
def send_push(*, text: str, fcm_tokens: List[str], url: str):
    """
    Отправка PUSH уведомления через Firebase
    :param text: Текст уведомления
    :param fcm_tokens: Массив токенов получателя
    :param url: Урл для перехода при нажатии на пуш уведомление
    :return:
    """
    assert len(fcm_tokens), "Нет получателей push уведомления"
    logger.info(f"task send_push start: {text}, {fcm_tokens}, {url}")
    fcm_transport = FcmUtils()
    fcm_transport.send(receivers=fcm_tokens, title=settings.FCM_TITLE, body=text, url=url)
    logger.info(f"task send_push end: {text}, {fcm_tokens}, {url}")
