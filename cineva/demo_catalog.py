"""Catálogo de demostración visual — sin proveedor externo."""
from __future__ import annotations

# Pósters generados (placehold.co) con colores distintos para aspecto de catálogo real.

def _poster(seed: str, w: int = 400, h: int = 600) -> str:
    # seed en el texto del placeholder para variar color
    colors = {
        "a": "1a2744/7eb6ff",
        "b": "2a1540/e8a0ff",
        "c": "0f2a22/6ee7a8",
        "d": "3a1a1a/ffb4a2",
        "e": "1a2a3a/93c5fd",
        "f": "2a2010/fcd34d",
        "g": "1a1030/c4b5fd",
        "h": "102030/67e8f9",
    }
    c = colors.get(seed[0], "1a2744/9db8ff")
    return f"https://placehold.co/{w}x{h}/{c}/png?text={seed[:12]}"


def _backdrop(seed: str) -> str:
    return _poster(seed, 1280, 720)


DEMO = [
    {
        "id": 101,
        "media_type": "movie",
        "title": "Noche en La Habana",
        "overview": "Un detective regresa a la ciudad después de veinte años para resolver el misterio que marcó su juventud. Entre bares, jazz y secretos familiares, nada es lo que parece.",
        "poster": _poster("Habana", 400, 600),
        "backdrop": _backdrop("HabanaBG"),
        "vote": 8.2,
        "year": "2024",
        "genres": ["Drama", "Thriller"],
        "runtime": 128,
        "tagline": "Algunos secretos no se quedan en el pasado.",
        "cast": [{"name": "Elena Ruiz"}, {"name": "Marco Vidal"}, {"name": "Sofía Méndez"}],
        "trailers": [],
    },
    {
        "id": 102,
        "media_type": "movie",
        "title": "Horizonte Rojo",
        "overview": "En un futuro cercano, una piloto de drones descubre que la guerra que combate se retransmite como entretenimiento. Debe elegir entre el sistema y la verdad.",
        "poster": _poster("Rojo", 400, 600),
        "backdrop": _backdrop("RojoBG"),
        "vote": 7.6,
        "year": "2025",
        "genres": ["Ciencia ficción", "Acción"],
        "runtime": 142,
        "tagline": "La guerra también tiene audiencia.",
        "cast": [{"name": "Aya Okada"}, {"name": "Leo Brandt"}],
        "trailers": [],
    },
    {
        "id": 103,
        "media_type": "movie",
        "title": "El último café",
        "overview": "Tres amigos de infancia se reúnen en el local que heredaron. Una noche de lluvia saca a la luz promesas rotas y una decisión que cambiará sus vidas.",
        "poster": _poster("Cafe", 400, 600),
        "backdrop": _backdrop("CafeBG"),
        "vote": 7.9,
        "year": "2023",
        "genres": ["Drama", "Comedia"],
        "runtime": 104,
        "tagline": "Algunas historias solo se cuentan de madrugada.",
        "cast": [{"name": "Pablo Ortega"}, {"name": "Irene Soto"}],
        "trailers": [],
    },
    {
        "id": 104,
        "media_type": "movie",
        "title": "Marea viva",
        "overview": "Una bióloga marina rastrea una especie que solo aparece durante las tormentas. Lo que encuentra bajo el agua reescribe la historia del litoral.",
        "poster": _poster("Marea", 400, 600),
        "backdrop": _backdrop("MareaBG"),
        "vote": 8.0,
        "year": "2024",
        "genres": ["Aventura", "Misterio"],
        "runtime": 118,
        "tagline": "El océano guarda memoria.",
        "cast": [{"name": "Clara Núñez"}],
        "trailers": [],
    },
    {
        "id": 105,
        "media_type": "movie",
        "title": "Códigos del sur",
        "overview": "Un ciberespecialista debe infiltrarse en una red clandestina que opera desde el Caribe. Cada pista lo acerca más a un enemigo que conoce su pasado.",
        "poster": _poster("Codigos", 400, 600),
        "backdrop": _backdrop("CodigosBG"),
        "vote": 7.4,
        "year": "2025",
        "genres": ["Acción", "Thriller"],
        "runtime": 131,
        "tagline": "En la red, nadie es quien dice ser.",
        "cast": [{"name": "Diego Alarcón"}, {"name": "Nadia Cruz"}],
        "trailers": [],
    },
    {
        "id": 106,
        "media_type": "movie",
        "title": "Luces de mediana noche",
        "overview": "Una pianista pierde la capacidad de tocar tras un accidente. Su recuperación pasa por enseñar a un niño prodigio en un barrio que no perdona la fragilidad.",
        "poster": _poster("Luces", 400, 600),
        "backdrop": _backdrop("LucesBG"),
        "vote": 8.5,
        "year": "2022",
        "genres": ["Drama", "Música"],
        "runtime": 112,
        "tagline": "La música vuelve cuando menos lo esperas.",
        "cast": [{"name": "Marina Beltrán"}],
        "trailers": [],
    },
    {
        "id": 107,
        "media_type": "movie",
        "title": "Desierto interior",
        "overview": "Dos hermanos cruzan el desierto para cumplir la última voluntad de su madre. El camino revela una deuda familiar y una verdad incómoda.",
        "poster": _poster("Desierto", 400, 600),
        "backdrop": _backdrop("DesiertoBG"),
        "vote": 7.8,
        "year": "2024",
        "genres": ["Drama", "Road movie"],
        "runtime": 121,
        "tagline": "Hay caminos que solo se hacen juntos.",
        "cast": [{"name": "Tomás Rivas"}, {"name": "Julián Rivas"}],
        "trailers": [],
    },
    {
        "id": 108,
        "media_type": "movie",
        "title": "Satélite 9",
        "overview": "La tripulación de una estación orbital pierde el contacto con la Tierra. Aislados, descubren que el verdadero peligro no viene del espacio.",
        "poster": _poster("Satelite", 400, 600),
        "backdrop": _backdrop("SateliteBG"),
        "vote": 7.1,
        "year": "2025",
        "genres": ["Ciencia ficción", "Suspense"],
        "runtime": 135,
        "tagline": "El silencio también transmite.",
        "cast": [{"name": "Hannah Cole"}, {"name": "Yuri Petrov"}],
        "trailers": [],
    },
    {
        "id": 201,
        "media_type": "tv",
        "title": "Barrio Norte",
        "overview": "Crónica coral de un vecindario donde todos se conocen demasiado. Comedia y drama se cruzan en cada portal, cada tienda y cada azotea.",
        "poster": _poster("Barrio", 400, 600),
        "backdrop": _backdrop("BarrioBG"),
        "vote": 8.4,
        "year": "2023",
        "genres": ["Drama", "Comedia"],
        "seasons": 3,
        "episodes": 24,
        "tagline": "Tu vecino también tiene una serie.",
        "cast": [{"name": "Laura Pino"}, {"name": "Esteban Gil"}],
        "trailers": [],
    },
    {
        "id": 202,
        "media_type": "tv",
        "title": "Señal perdida",
        "overview": "Una periodista investiga desapariciones vinculadas a una frecuencia de radio ilegal. Cada episodio revela un nuevo oyente… y un nuevo riesgo.",
        "poster": _poster("Senal", 400, 600),
        "backdrop": _backdrop("SenalBG"),
        "vote": 8.1,
        "year": "2024",
        "genres": ["Thriller", "Misterio"],
        "seasons": 2,
        "episodes": 16,
        "tagline": "Si la oyes, ya es tarde.",
        "cast": [{"name": "Valeria Gómez"}],
        "trailers": [],
    },
    {
        "id": 203,
        "media_type": "tv",
        "title": "Isla cero",
        "overview": "Supervivientes de un naufragio descubren que la isla no aparece en ningún mapa. Las reglas del lugar cambian con la marea.",
        "poster": _poster("Isla", 400, 600),
        "backdrop": _backdrop("IslaBG"),
        "vote": 7.7,
        "year": "2025",
        "genres": ["Aventura", "Fantasía"],
        "seasons": 1,
        "episodes": 10,
        "tagline": "Nadie llega por accidente.",
        "cast": [{"name": "Omar Díaz"}, {"name": "Kim Seo"}],
        "trailers": [],
    },
    {
        "id": 204,
        "media_type": "tv",
        "title": "Oficina 12",
        "overview": "Empleados de un ministerio anodino descubren un departamento que no debería existir. La burocracia nunca fue tan peligrosa.",
        "poster": _poster("Oficina", 400, 600),
        "backdrop": _backdrop("OficinaBG"),
        "vote": 8.0,
        "year": "2022",
        "genres": ["Comedia", "Fantasía"],
        "seasons": 2,
        "episodes": 18,
        "tagline": "El formulario más importante no tiene casilla.",
        "cast": [{"name": "Rocío Amenábar"}],
        "trailers": [],
    },
    {
        "id": 205,
        "media_type": "tv",
        "title": "Frontera azul",
        "overview": "Agentes de una unidad especial vigilan el tráfico marítimo ilegal. La lealtad se pone a prueba cuando el caso toca a uno de los suyos.",
        "poster": _poster("Frontera", 400, 600),
        "backdrop": _backdrop("FronteraBG"),
        "vote": 7.5,
        "year": "2024",
        "genres": ["Crimen", "Drama"],
        "seasons": 2,
        "episodes": 14,
        "tagline": "La línea más delgada es la del deber.",
        "cast": [{"name": "Héctor Salas"}, {"name": "Ana Belén Cruz"}],
        "trailers": [],
    },
    {
        "id": 206,
        "media_type": "tv",
        "title": "Después del fuego",
        "overview": "Tras un incendio que destruye un pueblo, los vecinos reconstruyen más que casas: reescriben quiénes fueron y quiénes quieren ser.",
        "poster": _poster("Fuego", 400, 600),
        "backdrop": _backdrop("FuegoBG"),
        "vote": 8.3,
        "year": "2023",
        "genres": ["Drama"],
        "seasons": 1,
        "episodes": 8,
        "tagline": "De las cenizas también se escribe.",
        "cast": [{"name": "Inés Marín"}],
        "trailers": [],
    },
    {
        "id": 301,
        "media_type": "tv",
        "title": "Estrella de papel",
        "overview": "En una academia de magia donde los hechizos se dibujan, una estudiante sin don aparente descubre un poder prohibido ligado a los libros antiguos.",
        "poster": _poster("Estrella", 400, 600),
        "backdrop": _backdrop("EstrellaBG"),
        "vote": 8.6,
        "year": "2024",
        "genres": ["Anime", "Fantasía"],
        "seasons": 2,
        "episodes": 24,
        "tagline": "Cada página es un hechizo.",
        "cast": [{"name": "Yuki Hoshino"}],
        "trailers": [],
        "is_anime": True,
    },
    {
        "id": 302,
        "media_type": "tv",
        "title": "Mecha Distrito 7",
        "overview": "Pilotóles de instituto pilotean mechas urbanos para defender la ciudad. Entre torneos y secretos corporativos, la amistad es su única armadura.",
        "poster": _poster("Mecha", 400, 600),
        "backdrop": _backdrop("MechaBG"),
        "vote": 7.9,
        "year": "2025",
        "genres": ["Anime", "Acción"],
        "seasons": 1,
        "episodes": 12,
        "tagline": "El instituto nunca fue tan ruidoso.",
        "cast": [{"name": "Ren Takahashi"}],
        "trailers": [],
        "is_anime": True,
    },
    {
        "id": 303,
        "media_type": "tv",
        "title": "Sakura Express",
        "overview": "Un tren que solo aparece en primavera conecta mundos paralelos. Su conductora novata debe entregar cartas que cambian destinos.",
        "poster": _poster("Sakura", 400, 600),
        "backdrop": _backdrop("SakuraBG"),
        "vote": 8.2,
        "year": "2023",
        "genres": ["Anime", "Aventura"],
        "seasons": 1,
        "episodes": 13,
        "tagline": "El andén no está en ningún mapa.",
        "cast": [{"name": "Aoi Fujimura"}],
        "trailers": [],
        "is_anime": True,
    },
    {
        "id": 304,
        "media_type": "tv",
        "title": "Sombras de Kioto",
        "overview": "Un exorcista moderno y una espíritu antigua forman una alianza incómoda para limpiar maldiciones en la ciudad antigua.",
        "poster": _poster("Kioto", 400, 600),
        "backdrop": _backdrop("KiotoBG"),
        "vote": 8.0,
        "year": "2024",
        "genres": ["Anime", "Sobrenatural"],
        "seasons": 2,
        "episodes": 20,
        "tagline": "Lo invisible también deja huella.",
        "cast": [{"name": "Kenji Morita"}],
        "trailers": [],
        "is_anime": True,
    },
    {
        "id": 305,
        "media_type": "tv",
        "title": "Pixel Heart",
        "overview": "Jugadores atrapados en un MMO vintage deben completar la misión final antes de que los servidores se apaguen para siempre.",
        "poster": _poster("Pixel", 400, 600),
        "backdrop": _backdrop("PixelBG"),
        "vote": 7.8,
        "year": "2025",
        "genres": ["Anime", "Aventura"],
        "seasons": 1,
        "episodes": 12,
        "tagline": "Game over no es una opción.",
        "cast": [{"name": "Mika Sato"}],
        "trailers": [],
        "is_anime": True,
    },
    {
        "id": 306,
        "media_type": "tv",
        "title": "Viento de acero",
        "overview": "En un archipiélago de islas flotantes, pilotos de planeadores compiten en carreras letales mientras una rebelión se gesta en silencio.",
        "poster": _poster("Viento", 400, 600),
        "backdrop": _backdrop("VientoBG"),
        "vote": 8.4,
        "year": "2022",
        "genres": ["Anime", "Acción"],
        "seasons": 3,
        "episodes": 36,
        "tagline": "Quien controla el viento, controla el cielo.",
        "cast": [{"name": "Sora Hayashi"}],
        "trailers": [],
        "is_anime": True,
    },
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
    # mezcla ordenada por vote
    return sorted(DEMO, key=lambda x: x.get("vote") or 0, reverse=True)
