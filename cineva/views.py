"""Vistas Cineva — puente de metadata, trailers y login."""
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

from . import tmdb

log = logging.getLogger(__name__)
VERSION = "0.3.0"


def health(request):
    return JsonResponse(
        {
            "status": "ok",
            "app": "Cineva",
            "version": VERSION,
            "tmdb": tmdb.available(),
            "qvapay_configured": bool(getattr(settings, "QVAPAY_APP_SECRET", "")),
        }
    )


def home(request):
    trending = tmdb.trending("all", "week") if tmdb.available() else []
    movies = tmdb.trending("movie", "week") if tmdb.available() else []
    series = tmdb.trending("tv", "week") if tmdb.available() else []
    anime = tmdb.anime_discover() if tmdb.available() else []
    return render(
        request,
        "home.html",
        {
            "user": request.user,
            "trending": trending[:12],
            "movies": movies[:10],
            "series": series[:10],
            "anime": anime[:10],
            "tmdb_ok": tmdb.available(),
            "version": VERSION,
        },
    )


@require_GET
def search(request):
    query = (request.GET.get("q") or "").strip()
    results = tmdb.search_multi(query) if query and tmdb.available() else []
    return render(
        request,
        "search.html",
        {"query": query, "results": results, "tmdb_ok": tmdb.available()},
    )


@require_GET
def movie_detail(request, tmdb_id: int):
    item = tmdb.movie_detail(tmdb_id)
    return render(request, "detail.html", {"item": item, "type": "movie"})


@require_GET
def tv_detail(request, tmdb_id: int):
    item = tmdb.tv_detail(tmdb_id)
    return render(request, "detail.html", {"item": item, "type": "tv"})


@require_GET
def watch(request, media_type: str, tmdb_id: int):
    """Página puente: trailer + metadatos. Reproducción completa solo con fuentes legales."""
    if media_type == "movie":
        item = tmdb.movie_detail(tmdb_id)
    else:
        item = tmdb.tv_detail(tmdb_id)
        media_type = "tv"
    return render(
        request,
        "watch.html",
        {"item": item, "type": media_type, "bridge": True},
    )


@require_GET
def api_catalog(request):
    kind = (request.GET.get("kind") or "trending").lower()
    q = (request.GET.get("q") or "").strip()
    if not tmdb.available():
        return JsonResponse({"error": "TMDB_API_KEY no configurada", "results": []}, status=503)
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
    return JsonResponse({"kind": kind, "count": len(results), "results": results})


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
        log.warning("QvaPay webhook firma inválida")
        return HttpResponse(status=401)
    try:
        data = json.loads(body.decode() or "{}")
    except json.JSONDecodeError:
        return HttpResponse(status=400)
    log.info("QvaPay webhook status=%s remote_id=%s", data.get("status"), data.get("remote_id"))
    # TODO: activar premium cuando status == paid
    return HttpResponse("ok")
