"""Admin por defecto, Site, config y proveedores de video."""
from __future__ import annotations

import logging
import os

log = logging.getLogger(__name__)

DEFAULT_PROVIDERS = [
    {
        "key": "embed_generic",
        "name": "Embed genérico",
        "description": "Iframe genérico. Usa embed_url con {id}.",
        "enabled": False,
        "embed_url": "",
        "priority": 10,
    },
    {
        "key": "youtube_trailer",
        "name": "YouTube tráiler",
        "description": "Solo tráilers oficiales cuando hay key de YouTube en el ítem.",
        "enabled": True,
        "embed_url": "https://www.youtube.com/embed/{id}",
        "priority": 20,
    },
]


def ensure_defaults() -> None:
    from django.contrib.auth import get_user_model
    from django.contrib.sites.models import Site

    from .models import ProviderPlugin, SiteConfig

    try:
        site = Site.objects.get(id=1)
        site.domain = os.environ.get("CINEVA_SITE_DOMAIN", "oneforall.alwaysdata.net")
        site.name = "Cineva"
        site.save(update_fields=["domain", "name"])
    except Exception as e:
        log.debug("Site: %s", e)

    User = get_user_model()
    try:
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "admin@cineva.local", "admin")
        else:
            u = User.objects.get(username="admin")
            changed = False
            if not u.is_superuser:
                u.is_superuser = True
                changed = True
            if not u.is_staff:
                u.is_staff = True
                changed = True
            if changed:
                u.save()
    except Exception as e:
        log.debug("Admin: %s", e)

    cfg = SiteConfig.get()
    changed = False
    if not cfg.tmdb_api_key and os.environ.get("TMDB_API_KEY"):
        cfg.tmdb_api_key = os.environ["TMDB_API_KEY"]
        changed = True
    if not cfg.google_client_id and os.environ.get("GOOGLE_CLIENT_ID"):
        cfg.google_client_id = os.environ["GOOGLE_CLIENT_ID"]
        changed = True
    if not cfg.google_client_secret and os.environ.get("GOOGLE_CLIENT_SECRET"):
        cfg.google_client_secret = os.environ["GOOGLE_CLIENT_SECRET"]
        changed = True
    if not cfg.qvapay_app_id and os.environ.get("QVAPAY_APP_ID"):
        cfg.qvapay_app_id = os.environ["QVAPAY_APP_ID"]
        changed = True
    if not cfg.qvapay_app_secret and os.environ.get("QVAPAY_APP_SECRET"):
        cfg.qvapay_app_secret = os.environ["QVAPAY_APP_SECRET"]
        changed = True
    if changed:
        cfg.save()

    if cfg.google_client_id and cfg.google_client_secret:
        _ensure_google_socialapp(cfg.google_client_id, cfg.google_client_secret)

    for p in DEFAULT_PROVIDERS:
        ProviderPlugin.objects.get_or_create(
            key=p["key"],
            defaults={
                "name": p["name"],
                "description": p["description"],
                "enabled": p["enabled"],
                "embed_url": p["embed_url"],
                "priority": p["priority"],
            },
        )


def _ensure_google_socialapp(client_id: str, client_secret: str) -> None:
    try:
        from allauth.socialaccount.models import SocialApp
        from django.contrib.sites.models import Site

        site = Site.objects.get_current()
        app, created = SocialApp.objects.get_or_create(
            provider="google",
            defaults={"name": "Google", "client_id": client_id, "secret": client_secret},
        )
        if not created:
            app.client_id = client_id
            app.secret = client_secret
            app.name = "Google"
            app.save()
        if site not in app.sites.all():
            app.sites.add(site)
    except Exception as e:
        log.warning("Google SocialApp: %s", e)
