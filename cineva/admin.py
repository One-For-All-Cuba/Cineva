from django.contrib import admin

from .models import ProviderPlugin


@admin.register(ProviderPlugin)
class ProviderPluginAdmin(admin.ModelAdmin):
    list_display = ("name", "key", "kind", "enabled", "sort_order", "updated_at")
    list_filter = ("kind", "enabled")
    search_fields = ("name", "key")
