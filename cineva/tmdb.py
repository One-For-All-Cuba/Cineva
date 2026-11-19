"""Cliente TMDB con manejo de errores y helpers."""
from __future__ import annotations

import logging
from typing import Any

import requests
from django.conf import settings

log = logging.getLogger(__name__)
BASE = "https://api.themoviedb.org/3"
IMG = "https://image.tmdb.org/t/p"


def _key() -> str:
    return (getattr(settings, "TMDB_API_KEY", None) or "").strip()


def available() -> bool:
    return bool(_key())


def get(path: str, params: dict | None = None, timeout: int = 12) -> dict[str, Any]:
    key = _key()
    if not key:
        return {}
    p = dict(params or {})
    p.setdefault("api_key", key)
    p.setdefault("language", "es-ES")
    try:
        r = requests.get(f"{BASE}{path}", params=p, timeout=timeout)
        if r.ok:
            return r.json()
        log.warning("TMDB %s -> %s", path, r.status_code)
    except requests.RequestException as e:
        log.warning("TMDB error %s: %s", path, e)
    return {}


def poster_url(path: str | None, size: str = "w342") -> str:
    if not path:
        return ""
    return f"{IMG}/{size}{path}"


def backdrop_url(path: str | None, size: str = "w780") -> str:
    if not path:
        return ""
    return f"{IMG}/{size}{path}"


def search_multi(query: str, page: int = 1) -> list[dict]:
    data = get("/search/multi", {"query": query, "page": page, "include_adult": "false"})
    results = []
    for item in data.get("results") or []:
        mt = item.get("media_type")
        if mt not in ("movie", "tv"):
            continue
        results.append(normalize(item))
    return results


def trending(media: str = "all", window: str = "week") -> list[dict]:
    data = get(f"/trending/{media}/{window}")
    out = []
    for item in data.get("results") or []:
        if not item.get("media_type"):
            item["media_type"] = "movie" if media == "movie" else "tv" if media == "tv" else item.get("media_type")
        if item.get("media_type") in ("movie", "tv") or media in ("movie", "tv"):
            if media == "movie":
                item["media_type"] = "movie"
            elif media == "tv":
                item["media_type"] = "tv"
            out.append(normalize(item))
    return out[:20]


def anime_discover(page: int = 1) -> list[dict]:
    """Series animación / anime (genre 16 Animation + original language ja opcional)."""
    data = get(
        "/discover/tv",
        {
            "with_genres": "16",
            "sort_by": "popularity.desc",
            "page": page,
        },
    )
    out = []
    for item in data.get("results") or []:
        item["media_type"] = "tv"
        out.append(normalize(item))
    return out


def movie_detail(tmdb_id: int) -> dict:
    data = get(f"/movie/{tmdb_id}", {"append_to_response": "videos,credits"})
    if not data:
        return {}
    data["media_type"] = "movie"
    return enrich_detail(data)


def tv_detail(tmdb_id: int) -> dict:
    data = get(f"/tv/{tmdb_id}", {"append_to_response": "videos,credits"})
    if not data:
        return {}
    data["media_type"] = "tv"
    return enrich_detail(data)


def normalize(item: dict) -> dict:
    mt = item.get("media_type") or ("movie" if "title" in item else "tv")
    title = item.get("title") or item.get("name") or ""
    date = item.get("release_date") or item.get("first_air_date") or ""
    return {
        "id": item.get("id"),
        "media_type": mt,
        "title": title,
        "overview": (item.get("overview") or "")[:400],
        "poster": poster_url(item.get("poster_path")),
        "backdrop": backdrop_url(item.get("backdrop_path")),
        "vote": item.get("vote_average") or 0,
        "year": (date[:4] if date else ""),
        "date": date,
    }


def enrich_detail(data: dict) -> dict:
    n = normalize({**data, "media_type": data.get("media_type")})
    trailers = []
    for v in (data.get("videos") or {}).get("results") or []:
        if v.get("site") == "YouTube" and v.get("type") in ("Trailer", "Teaser"):
            trailers.append({"key": v.get("key"), "name": v.get("name"), "type": v.get("type")})
    cast = []
    for c in ((data.get("credits") or {}).get("cast") or [])[:8]:
        cast.append({"name": c.get("name"), "character": c.get("character")})
    n.update(
        {
            "runtime": data.get("runtime") or None,
            "genres": [g.get("name") for g in (data.get("genres") or [])],
            "trailers": trailers,
            "cast": cast,
            "tagline": data.get("tagline") or "",
            "status": data.get("status") or "",
            "seasons": data.get("number_of_seasons"),
            "episodes": data.get("number_of_episodes"),
            "raw": data,
        }
    )
    return n
