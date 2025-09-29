from django.contrib import admin

from closing_documents.models import ClosingDocument


@admin.register(ClosingDocument)
class ClosingDocumentAdmin(admin.ModelAdmin):
    list_display = ["id", "is_paid", "is_sent", "is_archive", "admin"]
    search_fields = ("=id",)
    list_filter = ["is_paid", "is_sent", "is_archive", "admin"]
    date_hierarchy = "start_date"
    exclude = ("tasks", "file_path", "files")
