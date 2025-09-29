import os
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os.path import basename

from core.celery import app


@app.task
def send_simple_message(*, email, Name, url: str, text=""):
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

    body = f"Привет! Вас пригласили в HOOPS Work! Для подтверждения регистрации перейдите по ссылке {url}/new/{text}/{toaddr} :)"
    msg.attach(MIMEText(body, "plain"))

    server = smtplib.SMTP_SSL(host="smtp.mail.ru", port=465)
    server.login(fromaddr, mypass)

    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()


@app.task
def send_bill(*, email, file: str):
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

    body = f"Привет! Для подтверждения указанных реквизитов в профиле необходимо оплатить счёт :)"
    msg.attach(MIMEText(body, "plain"))

    with open(file, "rb") as fil:
        part = MIMEApplication(fil.read(), Name=basename(file))
    part["Content-Disposition"] = 'attachment; filename="%s"' % basename(file)
    msg.attach(part)

    server = smtplib.SMTP_SSL(host="smtp.mail.ru", port=465)
    server.login(fromaddr, mypass)

    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()
