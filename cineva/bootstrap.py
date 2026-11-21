"""Admin por defecto, Site, config y proveedores."""
from __future__ import annotations

import logging
import os

log = logging.getLogger(__name__)

# Servidores alternativos basados en análisis de cuevana3t.pro y mirrors comunes.
# Plantillas usan {id} (TMDB o stream_id) y {type} (movie|tv).
DEFAULT_PROVIDERS = [
    {
        "key": "vidlink",
        "name": "VidLink",
        "description": "Embed multilenguaje (vidlink.pro). Buena cobertura de películas/series.",
        "enabled": True,
        "catalog_url": "",
        "embed_url": "https://vidlink.pro/{type}/{id}?sub_label=Spanish&player=jw&autoplay=true",
        "trailer_url": "https://www.youtube.com/embed/{trailer_key}",
        "download_url": "",
        "priority": 10,
    },
    {
        "key": "vsembed",
        "name": "VSEmbed",
        "description": "Embed Latino/Castellano (vsembed.ru).",
        "enabled": True,
        "catalog_url": "",
        "embed_url": "https://vsembed.ru/embed/{type}?tmdb={id}&ds_lang=es",
        "trailer_url": "",
        "download_url": "",
        "priority": 20,
    },
    {
        "key": "vidapi",
        "name": "VidAPI",
        "description": "Player alternativo (vidapi.xyz).",
        "enabled": True,
        "catalog_url": "",
        "embed_url": "https://vidapi.xyz/embed/{type}/{id}",
        "trailer_url": "",
        "download_url": "",
        "priority": 30,
    },
    {
        "key": "videasy",
        "name": "Videasy",
        "description": "Player.videasy.net — otro mirror de embeds.",
        "enabled": True,
        "catalog_url": "",
        "embed_url": "https://player.videasy.net/{type}/{id}",
        "trailer_url": "",
        "download_url": "",
        "priority": 40,
    },
    {
        "key": "custom_json",
        "name": "API JSON propia",
        "description": (
            "Catálogo desde tu endpoint HTTPS. "
            "JSON: {movies:[], series:[], anime:[], trending:[]}. "
            "Cada ítem: id, title, poster, overview, year, media_type, trailer_key, download_url opcional."
        ),
        "enabled": False,
        "catalog_url": "",
        "embed_url": "",
        "trailer_url": "https://www.youtube.com/embed/{trailer_key}",
        "download_url": "",
        "priority": 5,
    },
    {
        "key": "youtube_trailer",
        "name": "YouTube tráilers",
        "description": "Reproduce tráilers oficiales cuando el ítem trae trailer_key.",
        "enabled": True,
        "catalog_url": "",
        "embed_url": "",
        "trailer_url": "https://www.youtube.com/embed/{trailer_key}",
        "download_url": "",
        "priority": 90,
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
        defaults = {
            "name": p["name"],
            "description": p["description"],
            "enabled": p["enabled"],
            "catalog_url": p.get("catalog_url") or "",
            "embed_url": p.get("embed_url") or "",
            "trailer_url": p.get("trailer_url") or "",
            "download_url": p.get("download_url") or "",
            "priority": p["priority"],
        }
        obj, created = ProviderPlugin.objects.get_or_create(key=p["key"], defaults=defaults)
        if not created:
            update_fields = []
            if p.get("embed_url") and not obj.embed_url:
                obj.embed_url = p["embed_url"]
                update_fields.append("embed_url")
            if p.get("download_url") and not obj.download_url:
                obj.download_url = p["download_url"]
                update_fields.append("download_url")
            if p.get("trailer_url") and not obj.trailer_url:
                obj.trailer_url = p["trailer_url"]
                update_fields.append("trailer_url")
            if p["key"] in ("vidlink", "vsembed", "vidapi", "videasy") and not obj.enabled:
                if obj.priority == 100 and not obj.embed_url:
                    obj.enabled = True
                    obj.priority = p["priority"]
                    obj.embed_url = p.get("embed_url") or ""
                    update_fields.extend(["enabled", "priority", "embed_url"])
            if update_fields:
                obj.save(update_fields=list(set(update_fields)))


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
