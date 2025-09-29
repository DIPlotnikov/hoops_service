from django.db import models

from hotels.models import Executer


class Metrics(models.Model):
    executor = models.ForeignKey(Executer, on_delete=models.CASCADE, verbose_name="Исполнитель")
    last_request_task = models.DateTimeField(verbose_name="Последний отклик на заявку")

    class Meta:
        verbose_name = "Метрика"
        verbose_name_plural = "Метрики"

    def __str__(self):
        return f"{self.executor} - {self.last_request_task}"
