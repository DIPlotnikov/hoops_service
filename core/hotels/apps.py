from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "authentication"


class authenticationConfig(AppConfig):
    name = "hotels"
    verbose_name = "Управление моделями"

    def ready(self):
        from . import signals

        print(signals)

        pass
