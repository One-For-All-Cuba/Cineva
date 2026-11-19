from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("health/", views.health, name="health"),
    path("", views.home, name="home"),
    path("search/", views.search, name="search"),
    path("movie/<int:tmdb_id>/", views.movie_detail, name="movie_detail"),
    path("tv/<int:tmdb_id>/", views.tv_detail, name="tv_detail"),
    path("watch/<str:media_type>/<int:tmdb_id>/", views.watch, name="watch"),
    path("qvapay/login/", views.qvapay_login, name="qvapay_login"),
    path("qvapay/webhook/", views.qvapay_webhook, name="qvapay_webhook"),
    path("api/catalog/", views.api_catalog, name="api_catalog"),
]
