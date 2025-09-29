from django.db import models

from settings.choices import TypeVar


def get_nds():
    res = Variable.objects.filter(key__icontains="NDS").last()
    assert res, "НДС не установлен"
    return res.get_value()


def get_remuneration():
    res = Variable.objects.filter(key__icontains="REMUNERATION").last()
    assert res, "Вознаграждение не установлено"
    return int(res.value)


class Variable(models.Model):
    value = models.CharField(max_length=255)
    key = models.CharField(max_length=255, choices=TypeVar.choices, default=TypeVar.NDS_INT)

    def __str__(self):
        return self.key

    def get_value(self):
        if self.key == TypeVar.NDS_INT:
            return int(self.value)
        if self.key == TypeVar.NDS_FLOAT:
            return float(self.value)
        return self.value

    class Meta:
        verbose_name = "Переменная"
        verbose_name_plural = "Переменные"
