"""Catálogo demo visual completo — portadas y metadatos para UI profesional."""
from __future__ import annotations

from typing import Iterable


def _poster(seed: str, w: int = 400, h: int = 600) -> str:
    # Imágenes estables por seed (aspecto de portada fotográfica)
    return f"https://picsum.photos/seed/cineva-{seed}/{w}/{h}"


def _backdrop(seed: str) -> str:
    return f"https://picsum.photos/seed/cineva-bg-{seed}/1280/720"


def _item(
    id: int,
    media_type: str,
    title: str,
    overview: str,
    year: str,
    vote: float,
    genres: list[str],
    *,
    runtime: int | None = None,
    seasons: int | None = None,
    episodes: int | None = None,
    tagline: str = "",
    cast: list[str] | None = None,
    is_anime: bool = False,
    quality: str = "HD",
) -> dict:
    seed = f"{id}-{title[:20].replace(' ', '')}"
    return {
        "id": id,
        "media_type": media_type,
        "title": title,
        "overview": overview,
        "poster": _poster(seed),
        "backdrop": _backdrop(seed),
        "vote": vote,
        "year": year,
        "genres": genres,
        "runtime": runtime,
        "seasons": seasons,
        "episodes": episodes,
        "tagline": tagline,
        "cast": [{"name": n} for n in (cast or [])],
        "trailers": [],
        "is_anime": is_anime,
        "quality": quality,
    }


DEMO: list[dict] = [
    # —— Películas ——
    _item(101, "movie", "Noche en La Habana",
          "Un detective regresa a la ciudad tras veinte años para resolver el misterio que marcó su juventud.",
          "2024", 8.2, ["Drama", "Thriller"], runtime=128,
          tagline="Algunos secretos no se quedan en el pasado.",
          cast=["Elena Ruiz", "Marco Vidal", "Sofía Méndez"]),
    _item(102, "movie", "Horizonte Rojo",
          "Una piloto de drones descubre que la guerra que combate se retransmite como entretenimiento.",
          "2025", 7.6, ["Ciencia ficción", "Acción"], runtime=142,
          tagline="La guerra también tiene audiencia.",
          cast=["Aya Okada", "Leo Brandt"]),
    _item(103, "movie", "El último café",
          "Tres amigos se reúnen en el local que heredaron. Una noche de lluvia saca a la luz promesas rotas.",
          "2023", 7.9, ["Drama", "Comedia"], runtime=104,
          cast=["Pablo Ortega", "Irene Soto"]),
    _item(104, "movie", "Marea viva",
          "Una bióloga marina rastrea una especie que solo aparece durante las tormentas.",
          "2024", 8.0, ["Aventura", "Misterio"], runtime=118,
          cast=["Clara Núñez"]),
    _item(105, "movie", "Códigos del sur",
          "Un ciberespecialista se infiltra en una red clandestina que opera desde el Caribe.",
          "2025", 7.4, ["Acción", "Thriller"], runtime=131,
          cast=["Diego Alarcón", "Nadia Cruz"]),
    _item(106, "movie", "Luces de mediana noche",
          "Una pianista pierde la capacidad de tocar tras un accidente y encuentra sentido enseñando a un niño prodigio.",
          "2022", 8.5, ["Drama", "Música"], runtime=112,
          cast=["Marina Beltrán"]),
    _item(107, "movie", "Desierto interior",
          "Dos hermanos cruzan el desierto para cumplir la última voluntad de su madre.",
          "2024", 7.8, ["Drama"], runtime=121,
          cast=["Tomás Rivas", "Julián Rivas"]),
    _item(108, "movie", "Satélite 9",
          "La tripulación de una estación orbital pierde el contacto con la Tierra.",
          "2025", 7.1, ["Ciencia ficción", "Suspense"], runtime=135,
          cast=["Hannah Cole", "Yuri Petrov"]),
    _item(109, "movie", "Cristal negro",
          "Una joyera descubre que las piedras que vende alteran los recuerdos de quien las lleva.",
          "2023", 7.3, ["Fantasía", "Drama"], runtime=110,
          cast=["Lina Vargas"]),
    _item(110, "movie", "Ruta 47",
          "Un camionero transporta un cargamento que no debería existir. Cada parada acerca más a quienes lo persiguen.",
          "2026", 7.7, ["Acción", "Suspense"], runtime=119,
          cast=["Andrés Melo"]),
    _item(111, "movie", "La casa del faro",
          "Una escritora hereda un faro aislado donde las noches traen visitas que no están en ningún registro.",
          "2021", 8.1, ["Terror", "Misterio"], runtime=98,
          cast=["Beatriz Sol"]),
    _item(112, "movie", "Golpe de sol",
          "Dos rivales de la alta cocina se ven obligados a compartir cocina en un concurso internacional.",
          "2024", 7.0, ["Comedia", "Romance"], runtime=106,
          cast=["Camila Ortiz", "Hugo Serra"]),
    # —— Series ——
    _item(201, "tv", "Barrio Norte",
          "Crónica coral de un vecindario donde todos se conocen demasiado.",
          "2023", 8.4, ["Drama", "Comedia"], seasons=3, episodes=24,
          cast=["Laura Pino", "Esteban Gil"]),
    _item(202, "tv", "Señal perdida",
          "Una periodista investiga desapariciones vinculadas a una frecuencia de radio ilegal.",
          "2024", 8.1, ["Thriller", "Misterio"], seasons=2, episodes=16,
          cast=["Valeria Gómez"]),
    _item(203, "tv", "Isla cero",
          "Supervivientes de un naufragio descubren que la isla no aparece en ningún mapa.",
          "2025", 7.7, ["Aventura", "Fantasía"], seasons=1, episodes=10,
          cast=["Omar Díaz", "Kim Seo"]),
    _item(204, "tv", "Oficina 12",
          "Empleados de un ministerio descubren un departamento que no debería existir.",
          "2022", 8.0, ["Comedia", "Fantasía"], seasons=2, episodes=18,
          cast=["Rocío Amenábar"]),
    _item(205, "tv", "Frontera azul",
          "Agentes de una unidad especial vigilan el tráfico marítimo ilegal.",
          "2024", 7.5, ["Crimen", "Drama"], seasons=2, episodes=14,
          cast=["Héctor Salas", "Ana Belén Cruz"]),
    _item(206, "tv", "Después del fuego",
          "Tras un incendio que destruye un pueblo, los vecinos reconstruyen más que casas.",
          "2023", 8.3, ["Drama"], seasons=1, episodes=8,
          cast=["Inés Marín"]),
    _item(207, "tv", "Protocolo Aurora",
          "Científicos intentan revertir un experimento climático que salió de control.",
          "2025", 7.6, ["Ciencia ficción", "Drama"], seasons=1, episodes=8,
          cast=["Noah Keller"]),
    _item(208, "tv", "Noches de feria",
          "La vida de una familia que monta atracciones ambulantes cambia cuando llega un forastero.",
          "2022", 7.8, ["Drama", "Misterio"], seasons=2, episodes=12,
          cast=["Rita Campos"]),
    # —— Anime ——
    _item(301, "tv", "Estrella de papel",
          "En una academia donde los hechizos se dibujan, una estudiante sin don aparente despierta un poder prohibido.",
          "2024", 8.6, ["Anime", "Fantasía"], seasons=2, episodes=24, is_anime=True,
          cast=["Yuki Hoshino"]),
    _item(302, "tv", "Mecha Distrito 7",
          "Pilotóles pilotean mechas urbanos para defender la ciudad entre torneos y secretos corporativos.",
          "2025", 7.9, ["Anime", "Acción"], seasons=1, episodes=12, is_anime=True,
          cast=["Ren Takahashi"]),
    _item(303, "tv", "Sakura Express",
          "Un tren que solo aparece en primavera conecta mundos paralelos.",
          "2023", 8.2, ["Anime", "Aventura"], seasons=1, episodes=13, is_anime=True,
          cast=["Aoi Fujimura"]),
    _item(304, "tv", "Sombras de Kioto",
          "Un exorcista moderno y un espíritu antiguo limpian maldiciones en la ciudad antigua.",
          "2024", 8.0, ["Anime", "Sobrenatural"], seasons=2, episodes=20, is_anime=True,
          cast=["Kenji Morita"]),
    _item(305, "tv", "Pixel Heart",
          "Jugadores atrapados en un MMO vintage deben completar la misión final antes del apagado.",
          "2025", 7.8, ["Anime", "Aventura"], seasons=1, episodes=12, is_anime=True,
          cast=["Mika Sato"]),
    _item(306, "tv", "Viento de acero",
          "En un archipiélago de islas flotantes, pilotos de planeadores compiten en carreras letales.",
          "2022", 8.4, ["Anime", "Acción"], seasons=3, episodes=36, is_anime=True,
          cast=["Sora Hayashi"]),
    _item(307, "tv", "Café Lunar",
          "Un café que solo abre de madrugada atiende a clientes que ya no están vivos… del todo.",
          "2026", 8.3, ["Anime", "Drama"], seasons=1, episodes=10, is_anime=True,
          cast=["Hana Aoki"]),
]


def all_items() -> list[dict]:
    return list(DEMO)


def movies() -> list[dict]:
    return [x for x in DEMO if x["media_type"] == "movie"]


def series() -> list[dict]:
    return [x for x in DEMO if x["media_type"] == "tv" and not x.get("is_anime")]


def anime() -> list[dict]:
    return [x for x in DEMO if x.get("is_anime")]


def by_id(item_id: int) -> dict | None:
    for x in DEMO:
        if x["id"] == item_id:
            return x
    return None


def search(q: str) -> list[dict]:
    q = (q or "").strip().lower()
    if not q:
        return []
    out = []
    for x in DEMO:
        blob = f"{x['title']} {x.get('overview','')} {' '.join(x.get('genres') or [])}".lower()
        if q in blob:
            out.append(x)
    return out


def trending() -> list[dict]:
    return sorted(DEMO, key=lambda x: x.get("vote") or 0, reverse=True)


def genres_for(items: Iterable[dict]) -> list[str]:
    g: set[str] = set()
    for x in items:
        for name in x.get("genres") or []:
            g.add(name)
    return sorted(g)


def years_for(items: Iterable[dict]) -> list[str]:
    return sorted({x.get("year") or "" for x in items if x.get("year")}, reverse=True)


def filter_catalog(
    items: list[dict],
    *,
    genre: str = "",
    year: str = "",
    letter: str = "",
    orden: str = "rating",
) -> list[dict]:
    out = list(items)
    if genre:
        g = genre.lower()
        out = [x for x in out if any(g == (gg or "").lower() for gg in (x.get("genres") or []))]
    if year:
        out = [x for x in out if (x.get("year") or "") == year]
    if letter:
        L = letter.upper()
        if L == "#":
            out = [x for x in out if not (x.get("title") or "A")[0].isalpha()]
        else:
            out = [x for x in out if (x.get("title") or "").upper().startswith(L)]
    orden = (orden or "rating").lower()
    if orden in ("rating", "nota", "score"):
        out.sort(key=lambda x: x.get("vote") or 0, reverse=True)
    elif orden in ("year", "año", "ano"):
        out.sort(key=lambda x: x.get("year") or "", reverse=True)
    elif orden in ("az", "a-z", "title"):
        out.sort(key=lambda x: (x.get("title") or "").lower())
    elif orden in ("za", "z-a"):
        out.sort(key=lambda x: (x.get("title") or "").lower(), reverse=True)
    return out
