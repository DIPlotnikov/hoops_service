from django.contrib.admin import register, ModelAdmin

from settings.models import Variable


@register(Variable)
class HotelAdmin(ModelAdmin):
    list_display = (
        "key",
        "value",
    )
    search_fields = ("key", "value")
