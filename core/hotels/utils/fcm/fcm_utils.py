import logging
from typing import Union

FCM_TITLE = "HOOPS Service 🛎️"
if __name__ != "__main__":
    from django.conf import settings

    FCM_TITLE = settings.FCM_TITLE
from firebase_admin import credentials, initialize_app, messaging

logger = logging.getLogger(__name__)


def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return getinstance


@singleton
class FcmUtils:
    """
    Класс отправки push уведомлений на устройства (скопировано из сниппетов с репозитория)
    https://github.com/firebase/firebase-admin-python/blob/master/snippets/messaging/cloud_messaging.py
    """

    cred = {
        "type": "service_account",
        "project_id": "hoops-service",
        "private_key_id": "c82a7362a68f2d77c86d125813403390fc757e7f",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCyoNpNdv1BIA4B\nBba7Z4p6Wv4pZf1IuSeFMxYn3ZIrcro0V76MvTA7k3vFjAp5ctcXwHz+U/PKkiRr\n2lFjJp2CxuzFI8z2eQgp1ym5NQ8eKzRadAjmsMNHdjyVCNjPDHuqeX0j6JqbCsZR\n9D9EuNid/PGQZvTJSIyXb6bUJaofoDf+3gz5WlbS7XT4hb8vp0a3KPenv1uMHs0L\nLi9pzAs3gaBXKgg4ZW+ga/9XD7YdPF3FW6n2QBwhrt5LbxX8bTJVuwq/9GDHfOPV\nQe8qjTcbKM667Fbq3VQPClupu585XCTQYlmmgDZMe9VyfyKy3JJY1kkaUs/B4ke8\np3Ag/mO9AgMBAAECggEAATotnSvKOvUzYjMbWaPiW987es24FPcssiTacOxehUzm\nEP6JLqdby5dz2asH/bMVBQGQhCDP6sqR3lYjO2VuGYh/Cn0V+tbDWPEDdmktLpsm\nYoJnCqNTua5QAxbjgnLQn3dB1PaEz0H3HdpWUlP5aBpRrN32X233DymapARrnToT\nrK2N7q8Ydtr5APSovtmzRSXFpWv9i/xIBD/OPdTLGLi9Ub/TzyAdOeAPljxbcxGR\nwxZ3+zL18WFGnUQaYX8cGrZe6AGDYuE2Rro5ZH2gtaRdhf3mMV8QQojoABAeeTJL\nKScmIYbaWubL/5Zl8QARBeX42/Zpeve9zJE5WGCKkwKBgQDdEO9T0Nn7eJL+vg6w\nujN9Wms/h0xShHT3W6Ur04wrB+iYGmcjDXmkMBhI2dudqtc+8NfE5V2TplOrEF7R\n/I9v7yV+eNwQwpkWj3gz80vANj/OPCNepIg9mKA7EqZIWOeW8x+U8uCQ2qk2LhbC\npHecGTddiSxGwKQHB8TVUGOYswKBgQDO2yCxXn9l2vJjYDPrP0CXqDPxC9w2dkGi\n07IFNvnVDAaFJkOSmhJ/JmI7ffT3/ogStrtl/Mc0sItVTEfbLUSb/ltsRMHYW1Gp\nZqd8DOMle2bc/5r3KKTZuZsL2wtprZ17vrByOlAupe75qqb2+eZ362QPZp4YFcga\n9o+wqxnpzwKBgQDGlYfoSx0GAXJK1IBt0VafrLHbB7dQCRzpd7IQhKDNpvUSbeVo\nX5p+G5Y1Gz9liyqAp+msPj6pfCh86t/C0pYnfzS3P+qwQ58x3P+l61CJAjKfGPbM\n9hBNBOYrKr2lD/g6aXxdWTDR7xtCSHS5tPSdjSlnJOpZRIQUrK3s0aImcQKBgFCA\nhPOiJBBeqhA0o1/9CMU8p6I6jGQBl7+nhVN0NrxL5smwv4FxRpuHM5mVhl1xCEHI\nLZweSORfhIoYmqpYrqfK0IeNJqdtupUjpzCmz0uJ/9kn/IYNokI9cnKlt4ZUE8LR\nzldWDFhrKVquqDXbwW6QBCveMs6Kw4qCxB7sJ7SPAoGBANuncuDul4yc81NanRim\n8FUmqBrZCK3c9YvfRaF0uV7Mlek6UuB45smv/xsnTeqJJ9353dH8IrVg+cqWoAyV\nsT66KW2sTieX3ZzSWjnVEn153tAI8gkVPfLyInESTyrPxFxi8NdhWwTp0PjVvq8B\nAdoZiY81cI+GdmqlHULCyFn3\n-----END PRIVATE KEY-----\n",
        "client_email": "firebase-adminsdk-k2vjd@hoops-service.iam.gserviceaccount.com",
        "client_id": "112009478805614133663",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-k2vjd%40hoops-service.iam.gserviceaccount.com",
        "universe_domain": "googleapis.com",
    }

    def __init__(self):
        creds = credentials.Certificate(self.cred)
        initialize_app(creds)

    def send(
        self,
        receivers: Union[list, str],
        body: str,
        title: str = FCM_TITLE,
        url: str = "notifications",
    ) -> None:
        """
        Отправка пуш уведомления с выбором по списку получателей или одному получателю
        @param receivers: Получатели пуш уведомлений
        @param title: Заголовок
        @param body: Тело сообщения
        @param url: путь для перенаправления с нажатия на пуш
        """
        if isinstance(receivers, list):
            for receiver in receivers:
                try:
                    self.send_to_token(receiver, title, body, url)
                except:
                    pass
        elif isinstance(receivers, str):
            self.send_to_token(receivers, title, body, url)

    def send_to_token(self, registration_token: str, title: str, body: str, url="notifications") -> None:
        """
        Отправка одиночного пуша конкретному токену
        @param registration_token: токен получателя
        @param title: заголовок сообщения
        @param body: тело сообщения
        @param url: путь для перенаправления с нажатия на пуш
        """

        message = messaging.Message(
            android=messaging.AndroidConfig(
                notification=messaging.AndroidNotification(sound="sound.wav", channel_id="main"),
            ),
            apns=messaging.APNSConfig(
                payload=messaging.APNSPayload(
                    aps=messaging.Aps(
                        content_available=True,
                        badge=1,
                        sound="sound.wav",
                    ),
                ),
            ),
            token=registration_token,
            notification=messaging.Notification(body=body, title=title),
            data={"url": f"hoops://{url}"},
        )
        response = messaging.send(message)
        logger.info(f"FCM отправка одинарная:{response}, token:{registration_token}")

    def send_to_token_multicast(self, registration_tokens, title, body, url="notification") -> None:
        """
        Отправка пуш уведомления списку получателей
        @param registration_tokens: список токенов получателей
        @param title: заголовок сообщения
        @param body: тело сообщения
        @param url: путь для перенаправления с нажатия на пуш
        """
        assert isinstance(registration_tokens, list)
        for chunk in [registration_tokens[i : i + 500] for i in range(0, len(registration_tokens), 500)]:
            message = messaging.MulticastMessage(
                android=messaging.AndroidConfig(
                    notification=messaging.AndroidNotification(sound="sound.wav", channel_id="main"),
                ),
                apns=messaging.APNSConfig(
                    payload=messaging.APNSPayload(
                        aps=messaging.Aps(
                            content_available=True,
                            badge=1,
                            sound="sound.wav",
                        ),
                    ),
                ),
                tokens=chunk,
                notification=messaging.Notification(body=body, title=title),
                data={"url": f"hoops://{url}"},
            )
            response = messaging.send_multicast(message)
            logger.info(f"FCM отправка множественная:{response}")


if __name__ == "__main__":
    a = FcmUtils()
    a.send(
        receivers=[
            "fLPC6bP73kIJpvJ8_AKkwC:APA91bE4Q18plT9Ipx7k5g0BQPvddm9_IeBGZpEHqAYR6HjPr2601fuWIXRnOssCEjKdStgfz8pPu9AYYUYPbXeWSOYSyvINvwUAj-ZGdKTERkVqEeWtWH4",
        ],
        title=FCM_TITLE,
        body="Всем HOOPS",
        url="notifications",
    )
