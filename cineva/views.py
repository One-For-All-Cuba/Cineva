"""Vistas Cineva — catálogo profesional con filtros."""
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
VERSION = "0.7.0"


def _source() -> str:
    return "tmdb" if tmdb.available() else "demo"


def _filters_from_request(request):
    return {
        "genre": (request.GET.get("genero") or request.GET.get("genre") or "").strip(),
        "year": (request.GET.get("ano") or request.GET.get("year") or "").strip(),
        "letter": (request.GET.get("letra") or request.GET.get("letter") or "").strip(),
        "orden": (request.GET.get("orden") or "rating").strip(),
    }


def health(request):
    return JsonResponse(
        {
            "status": "ok",
            "app": "Cineva",
            "version": VERSION,
            "catalog": _source(),
            "tmdb": tmdb.available(),
            "items_demo": len(demo.all_items()),
        }
    )


def home(request):
    if tmdb.available():
        trending = tmdb.trending("all", "week")[:18]
        movies = tmdb.trending("movie", "week")[:18]
        series = tmdb.trending("tv", "week")[:18]
        anime = tmdb.anime_discover()[:18]
        popular = trending[:8]
        hero = next((c for c in (trending or movies) if c.get("backdrop") or c.get("poster")), None)
        genres = []
    else:
        trending = demo.trending()
        movies = demo.movies()
        series = demo.series()
        anime = demo.anime()
        popular = trending[:8]
        hero = trending[0] if trending else None
        genres = demo.genres_for(demo.all_items())
    return render(
        request,
        "home.html",
        {
            "user": request.user,
            "hero": hero,
            "trending": trending[:16],
            "movies": movies,
            "series": series,
            "anime": anime,
            "popular": popular,
            "genres": genres,
            "catalog_source": _source(),
            "version": VERSION,
        },
    )


def _list_page(request, title: str, items: list[dict], kind: str):
    f = _filters_from_request(request)
    filtered = demo.filter_catalog(
        items,
        genre=f["genre"],
        year=f["year"],
        letter=f["letter"],
        orden=f["orden"],
    )
    return render(
        request,
        "list.html",
        {
            "title": title,
            "items": filtered,
            "all_count": len(items),
            "user": request.user,
            "kind": kind,
            "genres": demo.genres_for(items),
            "years": demo.years_for(items),
            "letters": list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"),
            "filters": f,
            "catalog_source": _source(),
            "version": VERSION,
            "popular": demo.trending()[:6],
        },
    )


@require_GET
def movies_page(request):
    items = demo.movies() if not tmdb.available() else tmdb.trending("movie", "week")
    return _list_page(request, "Todas las películas", items, "movie")


@require_GET
def series_page(request):
    items = demo.series() if not tmdb.available() else tmdb.trending("tv", "week")
    return _list_page(request, "Todas las series", items, "tv")


@require_GET
def anime_page(request):
    items = demo.anime() if not tmdb.available() else tmdb.anime_discover()
    return _list_page(request, "Anime y animación", items, "tv")


@require_GET
def search(request):
    query = (request.GET.get("q") or "").strip()
    f = _filters_from_request(request)
    if tmdb.available() and query:
        results = tmdb.search_multi(query)
    else:
        base = demo.search(query) if query else demo.trending()
        results = demo.filter_catalog(
            base, genre=f["genre"], year=f["year"], letter=f["letter"], orden=f["orden"]
        )
    return render(
        request,
        "list.html",
        {
            "title": f"Resultados: {query}" if query else "Explorar catálogo",
            "items": results,
            "all_count": len(results),
            "query": query,
            "user": request.user,
            "kind": "all",
            "genres": demo.genres_for(demo.all_items()),
            "years": demo.years_for(demo.all_items()),
            "letters": list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"),
            "filters": f,
            "catalog_source": _source(),
            "version": VERSION,
            "popular": demo.trending()[:6],
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
        {
            "item": item,
            "type": item.get("media_type") or "movie",
            "user": request.user,
            "related": [x for x in demo.movies() if x["id"] != tmdb_id][:8],
            "catalog_source": _source(),
            "version": VERSION,
        },
    )


@require_GET
def tv_detail(request, tmdb_id: int):
    item = tmdb.tv_detail(tmdb_id) if tmdb.available() else None
    if not item or not item.get("id"):
        item = demo.by_id(tmdb_id) or {}
    pool = demo.anime() if item.get("is_anime") else demo.series()
    return render(
        request,
        "detail.html",
        {
            "item": item,
            "type": item.get("media_type") or "tv",
            "user": request.user,
            "related": [x for x in pool if x["id"] != tmdb_id][:8],
            "catalog_source": _source(),
            "version": VERSION,
        },
    )


@require_GET
def watch(request, media_type: str, tmdb_id: int):
    item = demo.by_id(tmdb_id) or {}
    if tmdb.available():
        remote = tmdb.movie_detail(tmdb_id) if media_type == "movie" else tmdb.tv_detail(tmdb_id)
        if remote and remote.get("id"):
            item = remote
    media_type = item.get("media_type") or media_type
    return render(
        request,
        "watch.html",
        {"item": item, "type": media_type, "user": request.user, "version": VERSION, "catalog_source": _source()},
    )


@require_GET
def api_catalog(request):
    kind = (request.GET.get("kind") or "trending").lower()
    q = (request.GET.get("q") or "").strip()
    f = _filters_from_request(request)
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
    results = demo.filter_catalog(
        results, genre=f["genre"], year=f["year"], letter=f["letter"], orden=f["orden"]
    )
    return JsonResponse({"kind": kind, "source": _source(), "count": len(results), "results": results})


def qvapay_login(request):
    return JsonResponse({"status": "use_sdk", "hint": "QvaPay.auth.requestLogin()"})


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
    return HttpResponse("ok")
