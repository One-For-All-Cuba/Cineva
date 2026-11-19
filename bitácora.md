# Bitácora Cineva

## 2026-11-18

- Se expandió el skeleton Django en el repositorio One-For-All-Cuba/Cineva.
- Añadido soporte de búsqueda TMDB (películas, series, anime), trailers YouTube.
- Configurado django-allauth para login con Google.
- Soporte base de QvaPay mini-app: SDK en frontend, webhook con verificación HMAC, variables de entorno.
- Creados doc_endpoints.md y esta bitácora.
- Trabajo realizado vía GitHub API para cumplir con el requisito de Alwaysdata (no en VPS local).
- **Push exitoso a https://github.com/One-For-All-Cuba/Cineva (commit 1a6045b...)**

## Notas
- El montaje 1gb en Alwaysdata debe usarse para el despliegue final.
- Configurar TMDB_API_KEY, credenciales Google OAuth y QvaPay app-id/secret.
- OFA shell actualmente no responde (502); clonar/pull manual en Alwaysdata cuando esté disponible.
