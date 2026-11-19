from django.conf import settings


def cineva_globals(request):
    version = getattr(settings, "CINEVA_VERSION", "0.9.0")
    return {
        "version": version,
        "catalog_source": "demo" if not getattr(settings, "TMDB_API_KEY", "") else "tmdb",
    }
