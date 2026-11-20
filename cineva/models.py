from django.db import models


class SiteConfig(models.Model):
    """Configuración integrada del sitio (singleton id=1). Sin TMDB."""

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
    """Proveedor de contenido/video. Si está activo y tiene catalog_url, sustituye el demo."""

    key = models.SlugField(max_length=64, unique=True)
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    enabled = models.BooleanField(default=False)
    # Catálogo JSON propio: GET devuelve {movies:[], series:[], anime:[], trending:[]}
    catalog_url = models.CharField(
        max_length=500,
        blank=True,
        help_text="URL HTTPS de tu API de catálogo (JSON). Si está y enabled, no se usa demo.",
    )
    # Reproducción: plantilla con {id} {type} {slug}
    embed_url = models.CharField(max_length=500, blank=True)
    trailer_url = models.CharField(
        max_length=500,
        blank=True,
        help_text="Plantilla tráiler, p.ej. https://www.youtube.com/embed/{trailer_key}",
    )
    download_url = models.CharField(
        max_length=500,
        blank=True,
        help_text="Plantilla descarga, p.ej. https://servidor.externo/{id}.mp4 o con {type} {slug}",
    )
    priority = models.PositiveIntegerField(default=100)
    config = models.JSONField(default=dict, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["priority", "name"]
        verbose_name = "Proveedor"

    def __str__(self) -> str:
        return f"{self.name} ({'on' if self.enabled else 'off'})"
