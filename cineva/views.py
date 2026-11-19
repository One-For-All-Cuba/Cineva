"""Vistas Cineva — sin TMDB; catálogo por proveedor o demo."""
from __future__ import annotations

import hashlib
import hmac
import logging

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_http_methods, require_POST

from . import demo_catalog as demo
from . import providers as prov
from .bootstrap import _ensure_google_socialapp
from .models import ProviderPlugin, SiteConfig

log = logging.getLogger(__name__)
VERSION = getattr(settings, "CINEVA_VERSION", "0.9.2")


def _filters_from_request(request):
    return {
        "genre": (request.GET.get("genero") or request.GET.get("genre") or "").strip(),
        "year": (request.GET.get("ano") or request.GET.get("year") or "").strip(),
        "letter": (request.GET.get("letra") or request.GET.get("letter") or "").strip(),
        "orden": (request.GET.get("orden") or "rating").strip(),
    }


def health(request):
    b = prov.catalog_bundle()
    return JsonResponse(
        {
            "status": "ok",
            "app": "Cineva",
            "version": VERSION,
            "catalog": b.get("source"),
            "items": len(b.get("all") or []),
        }
    )


def home(request):
    b = prov.catalog_bundle()
    movies = b.get("movies") or []
    series = b.get("series") or []
    anime = b.get("anime") or []
    trending = b.get("trending") or []
    popular = trending[:8] or movies[:8]
    hero = trending[0] if trending else (movies[0] if movies else None)
    genres = demo.genres_for(b.get("all") or [])
    return render(
        request,
        "home.html",
        {
            "hero": hero,
            "movies": movies,
            "series": series,
            "anime": anime,
            "popular": popular,
            "genres": genres,
            "catalog_source": b.get("source"),
            "version": VERSION,
        },
    )


def _list_page(request, title: str, items: list, kind: str):
    f = _filters_from_request(request)
    filtered = demo.filter_catalog(
        items, genre=f["genre"], year=f["year"], letter=f["letter"], orden=f["orden"]
    )
    b = prov.catalog_bundle()
    return render(
        request,
        "list.html",
        {
            "title": title,
            "items": filtered,
            "all_count": len(items),
            "kind": kind,
            "genres": demo.genres_for(items),
            "years": demo.years_for(items),
            "letters": list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"),
            "filters": f,
            "catalog_source": b.get("source"),
            "version": VERSION,
            "popular": (b.get("trending") or [])[:6],
        },
    )


@require_GET
def movies_page(request):
    return _list_page(request, "Todas las películas", prov.catalog_bundle().get("movies") or [], "movie")


@require_GET
def series_page(request):
    return _list_page(request, "Todas las series", prov.catalog_bundle().get("series") or [], "tv")


@require_GET
def anime_page(request):
    return _list_page(request, "Anime y animación", prov.catalog_bundle().get("anime") or [], "tv")


@require_GET
def search(request):
    query = (request.GET.get("q") or "").strip()
    f = _filters_from_request(request)
    b = prov.catalog_bundle()
    base = b.get("all") or []
    if query:
        q = query.lower()
        base = [x for x in base if q in f"{x.get('title','')} {x.get('overview','')}".lower()]
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
            "kind": "all",
            "genres": demo.genres_for(b.get("all") or []),
            "years": demo.years_for(b.get("all") or []),
            "letters": list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"),
            "filters": f,
            "catalog_source": b.get("source"),
            "version": VERSION,
            "popular": (b.get("trending") or [])[:6],
        },
    )


@require_GET
def movie_detail(request, tmdb_id: int):
    item = prov.by_id(tmdb_id) or {}
    b = prov.catalog_bundle()
    related = [x for x in (b.get("movies") or []) if str(x.get("id")) != str(tmdb_id)][:8]
    return render(
        request,
        "detail.html",
        {
            "item": item,
            "type": item.get("media_type") or "movie",
            "related": related,
            "catalog_source": b.get("source"),
            "version": VERSION,
            "trailer_url": prov.trailer_for(item),
        },
    )


@require_GET
def tv_detail(request, tmdb_id: int):
    item = prov.by_id(tmdb_id) or {}
    b = prov.catalog_bundle()
    pool = b.get("anime") if item.get("is_anime") else b.get("series")
    related = [x for x in (pool or []) if str(x.get("id")) != str(tmdb_id)][:8]
    return render(
        request,
        "detail.html",
        {
            "item": item,
            "type": item.get("media_type") or "tv",
            "related": related,
            "catalog_source": b.get("source"),
            "version": VERSION,
            "trailer_url": prov.trailer_for(item),
        },
    )


@require_GET
def watch(request, media_type: str, tmdb_id: int):
    item = prov.by_id(tmdb_id) or {}
    media_type = item.get("media_type") or media_type
    embed = prov.embed_for(item, media_type)
    trailer = prov.trailer_for(item)
    return render(
        request,
        "watch.html",
        {
            "item": item,
            "type": media_type,
            "version": VERSION,
            "catalog_source": prov.catalog_bundle().get("source"),
            "embed_url": embed,
            "trailer_url": trailer,
        },
    )


@require_GET
def api_catalog(request):
    b = prov.catalog_bundle()
    kind = (request.GET.get("kind") or "trending").lower()
    if kind == "movie":
        results = b.get("movies") or []
    elif kind == "tv":
        results = b.get("series") or []
    elif kind == "anime":
        results = b.get("anime") or []
    else:
        results = b.get("trending") or []
    return JsonResponse({"kind": kind, "source": b.get("source"), "count": len(results), "results": results})


def qvapay_login(request):
    return JsonResponse({"status": "use_sdk", "hint": "QvaPay.auth.requestLogin()"})


@csrf_exempt
@require_POST
def qvapay_webhook(request):
    secret = ""
    try:
        cfg = SiteConfig.get()
        secret = cfg.qvapay_app_secret or ""
    except Exception:
        pass
    if not secret:
        return HttpResponse("qvapay not configured", status=503)
    signature = request.headers.get("x-qvapay-signature", "")
    body = request.body
    expected = "sha256=" + hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(signature, expected):
        return HttpResponse(status=401)
    return HttpResponse("ok")


def staff_required(view):
    return login_required(user_passes_test(lambda u: u.is_staff)(view))


@staff_required
@require_http_methods(["GET", "POST"])
def panel_home(request):
    cfg = SiteConfig.get()
    if request.method == "POST" and request.POST.get("section") == "config":
        cfg.site_title = request.POST.get("site_title") or cfg.site_title
        cfg.google_client_id = request.POST.get("google_client_id", "").strip()
        cfg.google_client_secret = request.POST.get("google_client_secret", "").strip()
        cfg.qvapay_app_id = request.POST.get("qvapay_app_id", "").strip()
        cfg.qvapay_app_secret = request.POST.get("qvapay_app_secret", "").strip()
        cfg.save()
        if cfg.google_client_id and cfg.google_client_secret:
            _ensure_google_socialapp(cfg.google_client_id, cfg.google_client_secret)
        messages.success(request, "Configuración guardada")
        return redirect("panel_home")
    providers = list(ProviderPlugin.objects.all())
    b = prov.catalog_bundle()
    return render(
        request,
        "panel.html",
        {
            "cfg": cfg,
            "providers": providers,
            "version": VERSION,
            "catalog_source": b.get("source"),
            "google_redirect": "https://oneforall.alwaysdata.net/accounts/google/login/callback/",
        },
    )


@staff_required
@require_http_methods(["GET", "POST"])
def panel_plugin_edit(request, key: str):
    plugin = get_object_or_404(ProviderPlugin, key=key)
    if request.method == "POST":
        plugin.enabled = request.POST.get("enabled") == "on"
        plugin.name = request.POST.get("name") or plugin.name
        plugin.description = request.POST.get("description") or ""
        plugin.catalog_url = request.POST.get("catalog_url") or ""
        plugin.embed_url = request.POST.get("embed_url") or ""
        plugin.trailer_url = request.POST.get("trailer_url") or ""
        try:
            plugin.priority = int(request.POST.get("priority") or plugin.priority)
        except ValueError:
            pass
        plugin.save()
        messages.success(request, f"Proveedor «{plugin.name}» guardado")
        return redirect("panel_home")
    return render(request, "panel_plugin.html", {"plugin": plugin, "version": VERSION})
