"""Vistas Cineva — UI profesional con catálogo demo."""
from __future__ import annotations

import hashlib
import hmac
import json
import logging

from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from . import demo_catalog as demo
from . import tmdb

log = logging.getLogger(__name__)
VERSION = "0.5.0-demo"


def _catalog_source():
    """TMDB si hay clave; si no, catálogo demo visual."""
    if tmdb.available():
        return "tmdb"
    return "demo"


def health(request):
    return JsonResponse(
        {
            "status": "ok",
            "app": "Cineva",
            "version": VERSION,
            "catalog": _catalog_source(),
            "tmdb": tmdb.available(),
            "qvapay_configured": bool(getattr(settings, "QVAPAY_APP_SECRET", "")),
        }
    )


def home(request):
    if tmdb.available():
        trending = tmdb.trending("all", "week")[:16]
        movies = tmdb.trending("movie", "week")[:16]
        series = tmdb.trending("tv", "week")[:16]
        anime = tmdb.anime_discover()[:16]
        hero = next((c for c in (trending or movies) if c.get("backdrop") or c.get("poster")), None)
        source = "tmdb"
    else:
        trending = demo.trending()[:16]
        movies = demo.movies()
        series = demo.series()
        anime = demo.anime()
        hero = trending[0] if trending else None
        source = "demo"
    return render(
        request,
        "home.html",
        {
            "user": request.user,
            "hero": hero,
            "trending": trending,
            "movies": movies,
            "series": series,
            "anime": anime,
            "tmdb_ok": tmdb.available(),
            "catalog_source": source,
            "version": VERSION,
        },
    )


@require_GET
def search(request):
    query = (request.GET.get("q") or "").strip()
    if tmdb.available() and query:
        results = tmdb.search_multi(query)
        source = "tmdb"
    else:
        results = demo.search(query) if query else demo.trending()[:12]
        source = "demo"
    return render(
        request,
        "search.html",
        {
            "query": query,
            "results": results,
            "tmdb_ok": tmdb.available(),
            "catalog_source": source,
            "user": request.user,
        },
    )


@require_GET
def movie_detail(request, tmdb_id: int):
    item = tmdb.movie_detail(tmdb_id) if tmdb.available() else None
    if not item or not item.get("id"):
        item = demo.by_id(tmdb_id) or {}
    return render(
        request,
        "detail.html",
        {"item": item, "type": item.get("media_type") or "movie", "user": request.user},
    )


@require_GET
def tv_detail(request, tmdb_id: int):
    item = tmdb.tv_detail(tmdb_id) if tmdb.available() else None
    if not item or not item.get("id"):
        item = demo.by_id(tmdb_id) or {}
    return render(
        request,
        "detail.html",
        {"item": item, "type": item.get("media_type") or "tv", "user": request.user},
    )


@require_GET
def watch(request, media_type: str, tmdb_id: int):
    item = None
    if tmdb.available():
        item = tmdb.movie_detail(tmdb_id) if media_type == "movie" else tmdb.tv_detail(tmdb_id)
    if not item or not item.get("id"):
        item = demo.by_id(tmdb_id) or {}
        media_type = item.get("media_type") or media_type
    return render(
        request,
        "watch.html",
        {"item": item, "type": media_type, "bridge": True, "user": request.user},
    )


@require_GET
def movies_page(request):
    items = demo.movies() if not tmdb.available() else tmdb.trending("movie", "week")
    return render(
        request,
        "list.html",
        {"title": "Películas", "items": items, "user": request.user, "kind": "movie"},
    )


@require_GET
def series_page(request):
    items = demo.series() if not tmdb.available() else tmdb.trending("tv", "week")
    return render(
        request,
        "list.html",
        {"title": "Series", "items": items, "user": request.user, "kind": "tv"},
    )


@require_GET
def anime_page(request):
    items = demo.anime() if not tmdb.available() else tmdb.anime_discover()
    return render(
        request,
        "list.html",
        {"title": "Anime y animación", "items": items, "user": request.user, "kind": "tv"},
    )


@require_GET
def api_catalog(request):
    kind = (request.GET.get("kind") or "trending").lower()
    q = (request.GET.get("q") or "").strip()
    if tmdb.available():
        if kind == "search" and q:
            results = tmdb.search_multi(q)
        elif kind == "anime":
            results = tmdb.anime_discover()
        elif kind == "movie":
            results = tmdb.trending("movie")
        elif kind == "tv":
            results = tmdb.trending("tv")
        else:
            results = tmdb.trending("all")
        source = "tmdb"
    else:
        if kind == "search" and q:
            results = demo.search(q)
        elif kind == "anime":
            results = demo.anime()
        elif kind == "movie":
            results = demo.movies()
        elif kind == "tv":
            results = demo.series()
        else:
            results = demo.trending()
        source = "demo"
    return JsonResponse({"kind": kind, "source": source, "count": len(results), "results": results})


def qvapay_login(request):
    return JsonResponse(
        {
            "status": "use_sdk",
            "hint": "En el frontend: QvaPay.auth.requestLogin() dentro de la mini-app",
        }
    )


@csrf_exempt
@require_POST
def qvapay_webhook(request):
    secret = getattr(settings, "QVAPAY_APP_SECRET", "") or ""
    if not secret:
        return HttpResponse("qvapay not configured", status=503)
    signature = request.headers.get("x-qvapay-signature", "")
    body = request.body
    expected = "sha256=" + hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(signature, expected):
        return HttpResponse(status=401)
    try:
        data = json.loads(body.decode() or "{}")
    except json.JSONDecodeError:
        return HttpResponse(status=400)
    log.info("QvaPay webhook status=%s", data.get("status"))
    return HttpResponse("ok")
