import random

import requests
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from urllib.parse import urlparse


class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    attempts = models.IntegerField(default=0)

    def verify(self, code: str):
        if self.attempts >= 3:
            # Безопасная отправка уведомления в TG: если TG_KEY не задан/некорректен, просто пропускаем
            _safe_tg_post(
                settings.TG_KEY,
                data={
                    "chat_id": getattr(self.user, "telegram_id", None) or self.user.email.split("@")[0],
                    "text": f"Слишком много попыток входа `{self.user.username}`: `{self.attempts}`",
                    "parse_mode": "MarkdownV2",
                },
            )
            raise PermissionError("Too many attempts")
        if self.otp == code:
            if self.created_at < timezone.now() - timezone.timedelta(hours=2):
                self.delete()
                return False
            self.delete()
            return True
        self.attempts += 1
        self.save()
        return False

    def save(self):
        self.otp = str(random.randint(100000, 999999))
        super().save()
        # В DEV-режиме выводим OTP в консоль для удобства
        if getattr(settings, "DEBUG", False):
            print(f"[DEV] OTP для пользователя {self.user.username}: {self.otp}")
        # Безопасная отправка кода в TG: в DEV/без ключей не падаем
        _safe_tg_post(
            settings.TG_KEY,
            data={
                "chat_id": self.user.email.split("@")[0],
                "text": f"Код для пользователя `{self.user.username}`: `{self.otp}`",
                "parse_mode": "MarkdownV2",
            },
        )

    def __str__(self):
        return self.otp

    class Meta:
        verbose_name = "OTP"
        verbose_name_plural = "OTPs"


def _safe_tg_post(url: str | None, data: dict) -> None:
    """Безопасная отправка HTTP POST в Telegram.
    - Пропускает вызов, если URL пустой или без схемы.
    - Не роняет приложение при сетевых ошибках.
    - Ограничивает время ожидания.
    """
    try:
        if not url:
            return
        parsed = urlparse(url)
        if parsed.scheme not in ("http", "https"):
            return
        # Таймаут небольшой, чтобы не блокировать поток
        requests.post(url, data=data, timeout=5)
    except Exception:
        # В DEV без внешних интеграций молча игнорируем ошибки
        return
