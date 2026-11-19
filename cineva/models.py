from django.db import models


class ProviderPlugin(models.Model):
    """Proveedor configurable como plugin (TMDB, Google, QvaPay, video…)."""

    KIND_CHOICES = [
        ("catalog", "Catálogo / metadata"),
        ("auth", "Autenticación"),
        ("payment", "Pagos"),
        ("player", "Reproductor / video"),
        ("other", "Otro"),
    ]

    key = models.SlugField(max_length=64, unique=True)
    name = models.CharField(max_length=120)
    kind = models.CharField(max_length=20, choices=KIND_CHOICES, default="other")
    description = models.TextField(blank=True)
    enabled = models.BooleanField(default=False)
    config = models.JSONField(default=dict, blank=True)
    sort_order = models.PositiveIntegerField(default=100)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["sort_order", "name"]

    def __str__(self) -> str:
        return f"{self.name} ({'on' if self.enabled else 'off'})"
