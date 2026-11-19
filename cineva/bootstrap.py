"""Admin por defecto, Site, config y proveedores."""
from __future__ import annotations

import logging
import os

log = logging.getLogger(__name__)

DEFAULT_PROVIDERS = [
    {
        "key": "custom_json",
        "name": "API JSON propia",
        "description": (
            "Catálogo desde tu endpoint HTTPS. "
            "JSON: {movies:[], series:[], anime:[], trending:[]}. "
            "Cada ítem: id, title, poster, overview, year, media_type, trailer_key opcional."
        ),
        "enabled": False,
        "catalog_url": "",
        "embed_url": "",
        "trailer_url": "https://www.youtube.com/embed/{trailer_key}",
        "priority": 10,
    },
    {
        "key": "youtube_trailer",
        "name": "YouTube tráilers",
        "description": "Reproduce tráilers oficiales cuando el ítem trae trailer_key.",
        "enabled": True,
        "catalog_url": "",
        "embed_url": "",
        "trailer_url": "https://www.youtube.com/embed/{trailer_key}",
        "priority": 50,
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
            if not u.is_superuser or not u.is_staff:
                u.is_superuser = True
                u.is_staff = True
                u.save()
    except Exception as e:
        log.debug("Admin: %s", e)

    cfg = SiteConfig.get()
    changed = False
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
        obj, created = ProviderPlugin.objects.get_or_create(
            key=p["key"],
            defaults={
                "name": p["name"],
                "description": p["description"],
                "enabled": p["enabled"],
                "catalog_url": p.get("catalog_url") or "",
                "embed_url": p.get("embed_url") or "",
                "trailer_url": p.get("trailer_url") or "",
                "priority": p["priority"],
            },
        )
        if not created and p["key"] == "youtube_trailer" and not obj.trailer_url:
            obj.trailer_url = p["trailer_url"]
            obj.save(update_fields=["trailer_url"])


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
