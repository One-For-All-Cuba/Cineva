from django.contrib import admin

from .models import ProviderPlugin, SiteConfig


@admin.register(ProviderPlugin)
class ProviderPluginAdmin(admin.ModelAdmin):
    list_display = ("name", "key", "enabled", "priority", "updated_at")
    list_filter = ("enabled",)
    search_fields = ("name", "key")


@admin.register(SiteConfig)
class SiteConfigAdmin(admin.ModelAdmin):
    list_display = ("site_title", "updated_at")
