from django.db import models
from django.utils import timezone


class ClosingDocumentFile(models.Model):
    """Файл закрывающего документа"""

    name = models.CharField(max_length=255, default="", null=False, blank=True, help_text="Наименование пункта")
    path = models.CharField(max_length=255, default="", null=False, blank=True, help_text="Путь к файлу")
    number = models.CharField(max_length=255, default="", null=False, blank=True, help_text="Номер документа")
    amount = models.FloatField(verbose_name="Сумма в документе", help_text="Сумма в документе")

    def __str__(self):
        return f"Файл закрывающего документа {self.name}"

    class Meta:
        verbose_name = "Файл закрывающего документа"
        verbose_name_plural = "Файлы закрывающих документов"
        db_table = "hotels_closingdocumentfile"


class ClosingDocument(models.Model):
    """Закрывающие документы"""

    admin = models.ForeignKey(
        "hotels.Admin", on_delete=models.SET_NULL, null=True, help_text="Админ", verbose_name="Админ"
    )
    tasks = models.ManyToManyField(
        "hotels.Task",
        blank=True,
        help_text="Участвующие заявки",
        verbose_name="Заявки",
        db_table="hotels_closingdocument_tasks",
    )
    file_path = models.CharField(
        max_length=255, default="", null=False, blank=True, help_text="Путь к файлу счет фактуры", verbose_name="Путь"
    )

    files = models.ManyToManyField(
        ClosingDocumentFile,
        blank=True,
        help_text="Файлы закрывающих документов",
        verbose_name="Файлы закрывающих документов",
        db_table="hotels_closingdocument_files",
    )
    start_date = models.DateTimeField(
        null=False, default=timezone.now, help_text="Начало периода", verbose_name="Начало периода"
    )
    end_date = models.DateTimeField(
        null=False, default=timezone.now, help_text="Конец периода", verbose_name="Конец периода"
    )
    closing_date = models.DateTimeField(null=True, help_text="Дата закрытия", verbose_name="Дата закрытия")
    create_at = models.DateTimeField(auto_now_add=True, help_text="Время создания", verbose_name="Время создания")

    is_archive = models.BooleanField(default=False, help_text="Флаг на архив", verbose_name="Флаг на архив")
    is_paid = models.BooleanField(default=False, help_text="Флаг оплаты", verbose_name="Флаг оплаты")
    is_sent = models.BooleanField(default=False, help_text="Флаг отправки", verbose_name="Флаг отправки")
    is_block = models.BooleanField(
        default=False,
        verbose_name="Период заблокирован",
        help_text="Флаг блокировки на передвижение заявок в заданном периоде",
    )

    def __str__(self):
        return f"Закрывающий документ {self.admin}"

    class Meta:
        verbose_name = "Закрывающий документ"
        verbose_name_plural = "Закрывающие документы"
        ordering = ["-id"]
        db_table = "hotels_closingdocument"
