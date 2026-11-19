from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.static import serve

from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("health/", views.health, name="health"),
    path("", views.home, name="home"),
    path("search/", views.search, name="search"),
    path("peliculas/", views.movies_page, name="movies_page"),
    path("series/", views.series_page, name="series_page"),
    path("anime/", views.anime_page, name="anime_page"),
    path("movie/<int:tmdb_id>/", views.movie_detail, name="movie_detail"),
    path("tv/<int:tmdb_id>/", views.tv_detail, name="tv_detail"),
    path("watch/<str:media_type>/<int:tmdb_id>/", views.watch, name="watch"),
    path("qvapay/login/", views.qvapay_login, name="qvapay_login"),
    path("qvapay/webhook/", views.qvapay_webhook, name="qvapay_webhook"),
    path("api/catalog/", views.api_catalog, name="api_catalog"),
    path("panel/", views.panel_home, name="panel_home"),
    path("panel/plugin/<slug:key>/", views.panel_plugin_edit, name="panel_plugin"),
    path("static/<path:path>", serve, {"document_root": settings.BASE_DIR / "static"}),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.BASE_DIR / "static")
