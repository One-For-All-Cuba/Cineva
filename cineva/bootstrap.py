"""Asegura admin por defecto, Site, plugins y Google SocialApp."""
from __future__ import annotations

import os
import logging

log = logging.getLogger(__name__)

DEFAULT_PLUGINS = [
    {
        "key": "tmdb",
        "name": "TMDB",
        "kind": "catalog",
        "description": "Metadata y portadas de películas/series vía The Movie Database.",
        "enabled": False,
        "config": {"api_key": "", "language": "es-ES"},
        "sort_order": 10,
    },
    {
        "key": "google",
        "name": "Google OAuth",
        "kind": "auth",
        "description": "Inicio de sesión con cuenta de Google (django-allauth).",
        "enabled": False,
        "config": {"client_id": "", "client_secret": ""},
        "sort_order": 20,
    },
    {
        "key": "qvapay",
        "name": "QvaPay Mini-App",
        "kind": "payment",
        "description": "Login y pagos dentro de la mini-app QvaPay.",
        "enabled": False,
        "config": {"app_id": "", "app_secret": ""},
        "sort_order": 30,
    },
    {
        "key": "player_embed",
        "name": "Reproductor embed",
        "kind": "player",
        "description": "Plantilla de embed de video (iframe). Configura la URL base.",
        "enabled": False,
        "config": {"embed_url": "", "note": "Sustituye {id} por el id del título"},
        "sort_order": 40,
    },
]


def ensure_defaults() -> None:
    from django.contrib.auth import get_user_model
    from django.contrib.sites.models import Site

    from .models import ProviderPlugin

    # Site
    try:
        site = Site.objects.get(id=1)
        site.domain = os.environ.get("CINEVA_SITE_DOMAIN", "oneforall.alwaysdata.net")
        site.name = "Cineva"
        site.save(update_fields=["domain", "name"])
    except Exception as e:
        log.debug("Site bootstrap: %s", e)

    # Superuser admin / admin
    User = get_user_model()
    try:
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "admin@cineva.local", "admin")
            log.info("Creado superuser admin/admin")
        else:
            u = User.objects.get(username="admin")
            if not u.is_superuser:
                u.is_superuser = True
                u.is_staff = True
                u.save(update_fields=["is_superuser", "is_staff"])
    except Exception as e:
        log.debug("Admin bootstrap: %s", e)

    # Plugins
    for p in DEFAULT_PLUGINS:
        ProviderPlugin.objects.get_or_create(
            key=p["key"],
            defaults={
                "name": p["name"],
                "kind": p["kind"],
                "description": p["description"],
                "enabled": p["enabled"],
                "config": p["config"],
                "sort_order": p["sort_order"],
            },
        )

    # Sincronizar secrets de entorno a plugins + SocialApp Google
    _sync_env_plugins()


def _sync_env_plugins() -> None:
    from .models import ProviderPlugin

    tmdb_key = os.environ.get("TMDB_API_KEY", "")
    if tmdb_key:
        pl, _ = ProviderPlugin.objects.get_or_create(key="tmdb")
        cfg = dict(pl.config or {})
        cfg["api_key"] = tmdb_key
        pl.config = cfg
        pl.enabled = True
        pl.save()

    gid = os.environ.get("GOOGLE_CLIENT_ID", "")
    gsec = os.environ.get("GOOGLE_CLIENT_SECRET", "")
    if gid and gsec:
        pl, _ = ProviderPlugin.objects.get_or_create(key="google")
        pl.config = {"client_id": gid, "client_secret": gsec}
        pl.enabled = True
        pl.save()
        _ensure_google_socialapp(gid, gsec)
    else:
        # Si el plugin ya tiene credenciales guardadas en BD
        try:
            pl = ProviderPlugin.objects.get(key="google")
            cfg = pl.config or {}
            if pl.enabled and cfg.get("client_id") and cfg.get("client_secret"):
                _ensure_google_socialapp(cfg["client_id"], cfg["client_secret"])
        except ProviderPlugin.DoesNotExist:
            pass

    qid = os.environ.get("QVAPAY_APP_ID", "")
    qsec = os.environ.get("QVAPAY_APP_SECRET", "")
    if qid or qsec:
        pl, _ = ProviderPlugin.objects.get_or_create(key="qvapay")
        cfg = dict(pl.config or {})
        if qid:
            cfg["app_id"] = qid
        if qsec:
            cfg["app_secret"] = qsec
        pl.config = cfg
        pl.enabled = True
        pl.save()


def _ensure_google_socialapp(client_id: str, client_secret: str) -> None:
    try:
        from django.contrib.sites.models import Site
        from allauth.socialaccount.models import SocialApp

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
