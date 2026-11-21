"""
Cineva — configuración por grupos.
Sin sistema de plugins. Metadatos y trailers vía TMDB.
"""
import os
from pathlib import Path

# =============================================================================
# 1. RUTAS Y ENTORNO
# =============================================================================
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "dev-secret-change-me")
DEBUG = os.environ.get("DEBUG", "False").lower() in ("true", "1", "yes")
CINEVA_VERSION = "0.10.3"

ALLOWED_HOSTS = [
    "oneforall.alwaysdata.net",
    "services-oneforall.alwaysdata.net",
    "localhost",
    "127.0.0.1",
    "*",
]
