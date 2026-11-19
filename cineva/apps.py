from django.apps import AppConfig


class CinevaConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "cineva"

    def ready(self):
        # Import diferido para no romper migraciones
        try:
            from .bootstrap import ensure_defaults

            ensure_defaults()
        except Exception:
            pass
