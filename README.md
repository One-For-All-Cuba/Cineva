# Cineva

Plataforma Django de OneForAll desplegada en AlwaysData (`oneforall.alwaysdata.net`).

## Arranque local

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Producción (AlwaysData)

El service `start-cineva-public.sh` hace `git pull` al arrancar y levanta Gunicorn + Caddy + MCP.
