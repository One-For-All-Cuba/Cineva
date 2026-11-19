from django.db import models


class SiteConfig(models.Model):
    """Configuración integrada del sitio (singleton id=1)."""

    tmdb_api_key = models.CharField(max_length=128, blank=True)
    google_client_id = models.CharField(max_length=255, blank=True)
    google_client_secret = models.CharField(max_length=255, blank=True)
    qvapay_app_id = models.CharField(max_length=128, blank=True)
    qvapay_app_secret = models.CharField(max_length=255, blank=True)
    site_title = models.CharField(max_length=120, default="Cineva")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Configuración del sitio"

    def __str__(self):
        return "SiteConfig"

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class ProviderPlugin(models.Model):
    """Solo proveedores de video/reproducción (plugins)."""

    key = models.SlugField(max_length=64, unique=True)
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    enabled = models.BooleanField(default=False)
    # URL con {id} y opcionalmente {type}
    embed_url = models.CharField(max_length=500, blank=True)
    priority = models.PositiveIntegerField(default=100)
    config = models.JSONField(default=dict, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["priority", "name"]
        verbose_name = "Proveedor de video"

    def __str__(self) -> str:
        return f"{self.name} ({'on' if self.enabled else 'off'})"
