from .celery import app as celery_app

__all__ = ("celery_app",)

from django_celery_results.apps import CeleryResultConfig

CeleryResultConfig.verbose_name = "Фоновые задачи"
