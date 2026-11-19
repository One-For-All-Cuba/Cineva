# Bitácora Cineva

## 2026-11-19 — v0.9.0 sidebar, panel plugins, admin, Google

### Cambios
- Layout con **sidebar** fijo en PC y menú hamburguesa en móvil.
- Cuenta **admin / admin** creada automáticamente (`bootstrap.ensure_defaults`).
- Panel `/panel/` (solo staff) para activar/configurar **plugins de proveedores** (TMDB, Google, QvaPay, player embed).
- Google OAuth: Site domain, SocialApp desde plugin/env, `SOCIALACCOUNT_LOGIN_ON_GET`, redirect documentado.
- Migración `ProviderPlugin`.
- Servicio reiniciado (gunicorn HUP) → health **0.9.0**.

### Rutas nuevas
- `/panel/` — administración del sitio
- `/panel/plugin/<key>/` — editar plugin

### Google
Redirect URI: `https://oneforall.alwaysdata.net/accounts/google/login/callback/`
Configurar `client_id` y `client_secret` en el plugin Google del panel o env `GOOGLE_CLIENT_ID` / `GOOGLE_CLIENT_SECRET`.

### Nota dominio público
Si el panel Alwaysdata aún sirve 0.2, reiniciar el servicio del sitio (puerto 8300).
