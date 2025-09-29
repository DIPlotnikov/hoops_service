from django.db import models

from hotels.models import FileInfo
from passports.choices import CitizenshipOther


class PassportData(models.Model):
    """
    Паспорт
    """

    executer = models.CharField(max_length=255, null=False, default="")

    firstPage = models.OneToOneField(FileInfo, on_delete=models.CASCADE, null=True, related_name="firstPage")
    secondPage = models.OneToOneField(FileInfo, on_delete=models.CASCADE, null=True, related_name="secondPage")

    citizenship = models.CharField(max_length=50, null=False, default="РФ", help_text="Гражданство")
    citizenship_other = models.CharField(
        max_length=50, null=True, choices=CitizenshipOther.choices, default=None, help_text="Гражданство иное"
    )
    series = models.IntegerField(default=0, help_text="Серия", null=True)
    number = models.CharField(help_text="Номер", null=False, max_length=255, default="")
    issued_by = models.CharField(max_length=255, null=False, default="Отделом УФМС России", help_text="Кем выдан")
    date_of_issue = models.DateField()
    subdivision_code = models.CharField(max_length=7, default=None, help_text="Код подразделения", null=True)
    place_birth = models.CharField(max_length=255, null=False, default="Роддом", help_text="Место рождения")

    def __str__(self):
        return f"Паспорт №{self.id} исполнителя {self.executer}"

    @property
    def full_number(self):
        if self.series:
            series = str(self.series).zfill(4)
        else:
            series = ""
        return f"{series} {self.number}"

    class Meta:
        verbose_name = "Паспорт"
        verbose_name_plural = "Паспорта"
