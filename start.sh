#!/usr/bin/env bash
set -Eeuo pipefail
APP=/home/oneforall/mnt/1gb/Cineva
PKG=/home/oneforall/.local/cineva-packages
LOCAL_DATA=/home/oneforall/.local/share/cineva
CADDY_RUNTIME=/tmp/cineva-caddy
export PYTHONPATH="$PKG:$APP"
export CINEVA_DB_PATH="$LOCAL_DATA/db.sqlite3"
umask 077
mkdir -p "$LOCAL_DATA"
if [[ ! -s "$LOCAL_DATA/secret_key" ]]; then python3 -c 'import secrets; print(secrets.token_urlsafe(64))' > "$LOCAL_DATA/secret_key"; fi
export DJANGO_SECRET_KEY
DJANGO_SECRET_KEY="$(cat "$LOCAL_DATA/secret_key")"
cd "$APP"
python3 manage.py migrate --noinput
python3 -m gunicorn cineva.wsgi:application --bind 127.0.0.1:8000 --workers 2 --access-logfile - --error-logfile - &
GUNICORN_PID=$!
cleanup() { kill "$GUNICORN_PID" 2>/dev/null || true; wait "$GUNICORN_PID" 2>/dev/null || true; }
trap cleanup EXIT HUP INT TERM
for _ in $(seq 1 30); do if curl -fsS http://127.0.0.1:8000/health/ >/dev/null; then break; fi; sleep 1; done
curl -fsS http://127.0.0.1:8000/health/ >/dev/null
cp "$APP/bin/caddy" "$CADDY_RUNTIME"
chmod 700 "$CADDY_RUNTIME"
"$CADDY_RUNTIME" validate --config "$APP/Caddyfile" --adapter caddyfile
"$CADDY_RUNTIME" run --config "$APP/Caddyfile" --adapter caddyfile &
CADDY_PID=$!
wait "$CADDY_PID"
