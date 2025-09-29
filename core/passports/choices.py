from django.db import models
from django.utils.translation import gettext_lazy as _
from graphene import Enum as GEnum


class CitizenshipOther(models.TextChoices):
    ARMENIA = "ARMENIA", _("Армения")
    BELARUS = "BELARUS", _("Беларусь")
    KAZAKHSTAN = "KAZAKHSTAN", _("Казахстан")
    KYRGYZSTAN = "KYRGYZSTAN", _("Киргизия")
    RVP = "RVP", _("РВП")
    VNJ = "VNJ", _("ВНЖ")


CitizenshipOtherG = GEnum.from_enum(CitizenshipOther, description="Тип гражданства")
