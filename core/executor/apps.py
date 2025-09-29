from django.apps import AppConfig


class ExecutorConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "executor"
    verbose_name = "Исполнитель"
    verbose_name_plural = "Исполнители"

    def ready(self):
        # noinspection PyUnresolvedReferences
        from executor import signals
