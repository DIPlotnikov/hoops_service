from django.contrib import admin

from executor.models import Metrics


@admin.register(Metrics)
class MetricsAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = [
        "executor",
        "last_request_task",
    ]
