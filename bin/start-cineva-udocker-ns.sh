#!/usr/bin/env bash
# Cineva en udocker DENTRO de ofa-namespace, código en montaje 1gb.
set -Eeuo pipefail
HOME_DIR="${HOME:-/home/oneforall}"
BIN="$HOME_DIR/bin"
export PATH="$BIN:/usr/bin:/bin"
export UDOCKER_DIR="${UDOCKER_DIR:-/tmp/udocker-home}"
export TMPDIR=/tmp
LOG="$HOME_DIR/logs/cineva-udocker-ns.log"
PIDFILE="/tmp/cineva-udocker-ns.pid"
mkdir -p "$HOME_DIR/logs"

cmd="${1:-start}"
if [[ "$cmd" == "stop" ]]; then
  [[ -f "$PIDFILE" ]] && kill "$(cat "$PIDFILE")" 2>/dev/null || true
  rm -f "$PIDFILE"
  # matar gunicorn cineva y proot asociado (best effort)
  for p in $(pgrep -u "$(whoami)" -f "cineva.wsgi" || true); do kill "$p" 2>/dev/null || true; done
  echo "Cineva udocker-ns detenido"
  exit 0
fi

if [[ "$cmd" == "status" ]]; then
  [[ -f "$PIDFILE" ]] && echo "PID $(cat $PIDFILE)" || echo "no pidfile"
  ss -tlnp 2>/dev/null | grep 8000 || true
  pgrep -af "cineva.wsgi|ofa-combined|Cineva:/app" || true
  exit 0
fi

INNER=/tmp/cineva-udocker-inner.sh
cat > "$INNER" << 'INNER'
set -Eeuo pipefail
export HOME=/home/oneforall
export PATH=/home/oneforall/bin:/usr/bin:/bin
export UDOCKER_DIR=/tmp/udocker-home
export TMPDIR=/tmp
LOG=/home/oneforall/logs/cineva-udocker-ns.log
APP=/home/oneforall/mnt/1gb/Cineva
DATA=/home/oneforall/mnt/1gb/Cineva/data
PKG=/home/oneforall/mnt/1gb/Cineva/packages
mkdir -p "$DATA" "$PKG"
echo "[cineva-ns] mounts:" >> "$LOG"
mountpoint /home/oneforall/mnt/1gb >> "$LOG" 2>&1 || true
ls -la /home/oneforall/mnt/1gb/Cineva >> "$LOG" 2>&1 || true

# Preferir imagen/container cineva si existe; fallback bash run
if [[ -x /tmp/udocker-home/bin/udocker ]] || command -v udocker >/dev/null 2>&1; then
  UDOCKER_BIN=$(command -v udocker || echo /tmp/udocker-home/udocker)
  # path típico en este host
  export PYTHONPATH="/home/oneforall/mnt/1gb/udocker/pkg:${PYTHONPATH:-}"
  if [[ -d /tmp/udocker-1.3.17 ]]; then
    export PYTHONPATH="/tmp/udocker-1.3.17:$PYTHONPATH"
  fi
fi

# Arranque udocker con volúmenes en 1gb montado
python3 - << 'PY'
import os, sys
sys.path.insert(0, "/tmp/udocker-1.3.17")
sys.path.insert(0, "/home/oneforall/mnt/1gb/udocker/pkg")
os.environ["TMPDIR"] = "/tmp"
os.environ["UDOCKER_DIR"] = "/tmp/udocker-home"
try:
    from udocker.umain import UMain
except ImportError:
    # fallback: gunicorn host si hay paquete
    os.execvp("python3", ["python3", "-m", "gunicorn", "cineva.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2", "--chdir", "/home/oneforall/mnt/1gb/Cineva"])
argv = [
  "udocker", "--allow-root", "run",
  "--hostenv",
  "-v", "/home/oneforall/mnt/1gb/Cineva:/app",
  "-v", "/home/oneforall/mnt/1gb/Cineva/data:/data",
  "-v", "/home/oneforall/mnt/1gb/Cineva/packages:/packages",
  "-v", "/home/oneforall:/hosthome",
  "-v", "/home/oneforall/mnt/1gb:/mnt/1gb",
  "-v", "/tmp:/tmp",
  "-e", "HOME=/hosthome",
  "-e", "PYTHONPATH=/packages:/app",
  "-e", "DJANGO_SETTINGS_MODULE=cineva.settings",
  "-e", "CINEVA_DB_PATH=/data/db.sqlite3",
  "cineva",
  "bash", "-c",
  "export DJANGO_SECRET_KEY=$(cat /data/secret_key 2>/dev/null || echo fallback-secret); "
  "export PYTHONPATH=/packages:/app; export CINEVA_DB_PATH=/data/db.sqlite3; cd /app; "
  "python3 -m pip install -q --target /packages gunicorn django django-allauth requests 2>/dev/null || true; "
  "python3 manage.py migrate --noinput || true; "
  "exec python3 -m gunicorn cineva.wsgi:application --bind 0.0.0.0:8000 --workers 2 --access-logfile - --error-logfile -"
]
sys.argv = argv
sys.exit(UMain(sys.argv).execute() or 0)
PY
INNER

# Fix: the INNER heredoc is literal so PATH is fine
nohup "$BIN/ofa-namespace" bash "$INNER" >> "$LOG" 2>&1 &
echo $! > "$PIDFILE"
sleep 15
echo "Cineva udocker-ns PID $(cat $PIDFILE) log=$LOG"
ss -tlnp 2>/dev/null | grep 8000 || true
tail -30 "$LOG" || true
