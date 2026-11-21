# Git / GitHub — Cineva

## Repositorio
- **GitHub:** https://github.com/One-For-All-Cuba/Cineva
- **Branch:** `master`
- **Código vivo:** Alwaysdata `/home/oneforall/apps/Cineva`

## En Alwaysdata
```bash
cd /home/oneforall/apps/Cineva
git status
git add -A
git commit -m "mensaje"
# Push requiere credencial (HTTPS token o deploy key SSH)
git push -u origin master
```

## Estado
- `git init` hecho en Alwaysdata (rama master).
- `origin` → `https://github.com/One-For-All-Cuba/Cineva.git`
- `.gitignore` excluye `db.sqlite3`, `data/`, `packages/`, `.env`, logs.
- Sync inicial a GitHub vía API.
- Para push completo desde Alwaysdata: configurar **deploy key** o credential helper con PAT.

## No hacer
- No clonar ni trabajar Cineva en el VPS OneForAll.
