# Endpoints y APIs de Cineva

## Internos (Django)

- GET / : Página principal con búsqueda y login.
- GET /health/ : Estado del servicio.
- GET /search/?q= : Búsqueda multi en TMDB (películas, series, anime).
- GET /movie/<id>/ : Detalle de película + trailer YouTube.
- GET /tv/<id>/ : Detalle de serie + trailer.
- GET /accounts/login/ : Login allauth.
- GET /accounts/google/login/ : Login Google.
- POST /qvapay/webhook/ : Webhook de pagos QvaPay (verifica firma HMAC).
- GET /qvapay/login/ : Placeholder para login mini-app.
- GET /api/catalog/ : API placeholder.

## Externas integradas

- TMDB API: metadata y trailers (requiere TMDB_API_KEY).
- QvaPay Mini-app SDK: window.QvaPay.auth.requestLogin(), QvaPay.payments.payInvoice().
  - Crear factura en backend con POST https://api.qvapay.com/v2/create_invoice (app-id/secret).
- Google OAuth via django-allauth.

## Pendiente

- Verificación de init_data de QvaPay en backend.
- Modelos de usuarios premium / acceso.
- Fuentes de streaming legal o embeds permitidos.
- Despliegue en Alwaysdata 1gb con udocker.
