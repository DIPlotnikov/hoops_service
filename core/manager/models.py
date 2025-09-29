from django.db import models

from hotels.models import Manager, Executer


class BlackList(models.Model):
    manager = models.ForeignKey(
        Manager, on_delete=models.CASCADE, help_text="Менеджер", verbose_name="Менеджер", null=False
    )
    executor = models.ForeignKey(
        Executer, on_delete=models.CASCADE, help_text="Исполнитель", verbose_name="Исполнитель", null=False
    )

    class Meta:
        verbose_name = "Черный список"
        verbose_name_plural = "Черный список"
