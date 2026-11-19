"""Resolución de catálogo y embeds desde proveedores activos (no demo si hay catálogo)."""
from __future__ import annotations

import logging
from typing import Any

import requests

from . import demo_catalog as demo
from .models import ProviderPlugin

log = logging.getLogger(__name__)


def active_catalog_provider() -> ProviderPlugin | None:
    return (
        ProviderPlugin.objects.filter(enabled=True)
        .exclude(catalog_url="")
        .order_by("priority")
        .first()
    )


def active_player_provider() -> ProviderPlugin | None:
    return (
        ProviderPlugin.objects.filter(enabled=True)
        .exclude(embed_url="")
        .order_by("priority")
        .first()
    )


def _normalize_item(raw: dict, default_type: str = "movie") -> dict:
    mt = raw.get("media_type") or raw.get("type") or default_type
    title = raw.get("title") or raw.get("name") or "Sin título"
    return {
        "id": raw.get("id") or raw.get("slug") or title,
        "media_type": "tv" if mt in ("tv", "serie", "series", "anime") else "movie",
        "title": title,
        "overview": raw.get("overview") or raw.get("description") or "",
        "poster": raw.get("poster") or raw.get("poster_url") or "",
        "backdrop": raw.get("backdrop") or raw.get("backdrop_url") or raw.get("poster") or "",
        "vote": float(raw.get("vote") or raw.get("rating") or 0),
        "year": str(raw.get("year") or "")[:4],
        "genres": raw.get("genres") or [],
        "runtime": raw.get("runtime"),
        "seasons": raw.get("seasons"),
        "episodes": raw.get("episodes"),
        "is_anime": bool(raw.get("is_anime") or mt == "anime"),
        "quality": raw.get("quality") or "HD",
        "trailer_key": raw.get("trailer_key") or raw.get("youtube") or "",
        "slug": raw.get("slug") or str(raw.get("id") or ""),
        "stream_id": raw.get("stream_id") or raw.get("id"),
    }


def fetch_catalog(provider: ProviderPlugin) -> dict[str, list[dict]]:
    url = (provider.catalog_url or "").strip()
    if not url:
        return {}
    try:
        r = requests.get(url, timeout=12, headers={"User-Agent": "Cineva/0.9"})
        if not r.ok:
            log.warning("Catalog provider %s -> %s", provider.key, r.status_code)
            return {}
        data = r.json()
    except Exception as e:
        log.warning("Catalog provider error %s: %s", provider.key, e)
        return {}

    def arr(key: str, default_type: str) -> list[dict]:
        items = data.get(key) or data.get(key.rstrip("s")) or []
        if not isinstance(items, list):
            return []
        return [_normalize_item(x, default_type) for x in items if isinstance(x, dict)]

    movies = arr("movies", "movie")
    series = arr("series", "tv")
    anime = arr("anime", "anime")
    trending = arr("trending", "movie")
    if not trending:
        trending = sorted(movies + series + anime, key=lambda x: x.get("vote") or 0, reverse=True)
    return {"movies": movies, "series": series, "anime": anime, "trending": trending, "all": movies + series + anime}


def catalog_bundle() -> dict[str, Any]:
    """Si hay proveedor de catálogo activo → su data; si no → demo."""
    pl = active_catalog_provider()
    if pl:
        data = fetch_catalog(pl)
        if data.get("all") or data.get("movies") or data.get("series"):
            return {"source": pl.key, "provider": pl, **data}
    return {
        "source": "demo",
        "provider": None,
        "movies": demo.movies(),
        "series": demo.series(),
        "anime": demo.anime(),
        "trending": demo.trending(),
        "all": demo.all_items(),
    }


def by_id(item_id) -> dict | None:
    bundle = catalog_bundle()
    sid = str(item_id)
    for x in bundle.get("all") or []:
        if str(x.get("id")) == sid or str(x.get("slug")) == sid:
            return x
    # fallback demo
    try:
        iid = int(item_id)
        return demo.by_id(iid)
    except (TypeError, ValueError):
        return None


def embed_for(item: dict, media_type: str) -> str:
    pl = active_player_provider()
    if not pl or not pl.embed_url:
        return ""
    return (
        pl.embed_url.replace("{id}", str(item.get("stream_id") or item.get("id") or ""))
        .replace("{type}", media_type)
        .replace("{slug}", str(item.get("slug") or ""))
    )


def trailer_for(item: dict) -> str:
    key = item.get("trailer_key") or ""
    if not key:
        return ""
    pl = active_player_provider()
    if pl and pl.trailer_url:
        return pl.trailer_url.replace("{trailer_key}", key).replace("{id}", key)
    return f"https://www.youtube.com/embed/{key}"
