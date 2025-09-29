from django.db import models
from django.utils.translation import gettext_lazy as _


class TypeVar(models.TextChoices):
    NDS_INT = "NDS_INT", _("НДС целое число")
    NDS_FLOAT = "NDS_FLOAT", _("НДС дробное число")
    NDS_NONE = "NDS_NONE", _("НДС отсутствует")
    SHARE_OF_REMUNERATION = "SHARE_OF_REMUNERATION", _("Доля вознаграждения за поручение по заявкам в процентах")
