import os
import hmac
import hashlib
import json
import requests
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.conf import settings

def health(request):
    return JsonResponse({"status": "ok", "app": "Cineva", "version": "0.2"})

def home(request):
    return render(request, "home.html", {"user": request.user})

def search(request):
    query = request.GET.get("q", "")
    results = []
    if query and settings.TMDB_API_KEY:
        url = f"https://api.themoviedb.org/3/search/multi?api_key={settings.TMDB_API_KEY}&query={query}&language=es"
        try:
            r = requests.get(url, timeout=10)
            if r.ok:
                results = r.json().get("results", [])[:20]
        except Exception:
            pass
    return render(request, "search.html", {"query": query, "results": results})

def movie_detail(request, tmdb_id):
    data = {}
    if settings.TMDB_API_KEY:
        url = f"https://api.themoviedb.org/3/movie/{tmdb_id}?api_key={settings.TMDB_API_KEY}&language=es&append_to_response=videos"
        try:
            r = requests.get(url, timeout=10)
            if r.ok:
                data = r.json()
        except Exception:
            pass
    return render(request, "detail.html", {"item": data, "type": "movie"})

def tv_detail(request, tmdb_id):
    data = {}
    if settings.TMDB_API_KEY:
        url = f"https://api.themoviedb.org/3/tv/{tmdb_id}?api_key={settings.TMDB_API_KEY}&language=es&append_to_response=videos"
        try:
            r = requests.get(url, timeout=10)
            if r.ok:
                data = r.json()
        except Exception:
            pass
    return render(request, "detail.html", {"item": data, "type": "tv"})

def api_catalog(request):
    return JsonResponse({"message": "Catalog API - use TMDB key"})

def qvapay_login(request):
    return JsonResponse({"status": "use QvaPay SDK on frontend"})

@csrf_exempt
@require_POST
def qvapay_webhook(request):
    signature = request.headers.get("x-qvapay-signature", "")
    body = request.body
    if not settings.QVAPAY_APP_SECRET:
        return HttpResponse(status=500)
    expected = "sha256=" + hmac.new(
        settings.QVAPAY_APP_SECRET.encode(),
        body,
        hashlib.sha256
    ).hexdigest()
    if not hmac.compare_digest(signature, expected):
        return HttpResponse(status=401)
    data = json.loads(body)
    # Process payment: if data.get("status") == "paid": grant access
    return HttpResponse("ok")
