from src.tads.lista_enlazada import ListaEnlazada
from src.dominio.cancion import Cancion
from src.persistencia.texto import cargar_texto, DATA

RUTA_CANCIONES = DATA / "canciones.txt"
RUTA_VERSIONES = DATA / "versiones.txt"


class Biblioteca:
    """Representa la biblioteca musical: el catálogo de canciones
    y las relaciones entre una canción y sus versiones derivadas
    (covers, en vivo, remixes)."""

    def __init__(self):
        self._canciones = ListaEnlazada()
        self._versiones = []
        self.cargar_desde_txt()

    def agregar_cancion(self, cancion):
        self._canciones.insertar_al_final(cancion)

    def __iter__(self):
        return iter(self._canciones)

    def cargar_desde_txt(self):
        """Arma el catálogo y las versiones leyendo data/*.txt."""
        self._canciones = ListaEnlazada()
        for fila in cargar_texto(RUTA_CANCIONES):
            self.agregar_cancion(Cancion(
                int(fila["id"]),
                fila["titulo"],
                fila["artista"],
                fila["album"],
                fila["genero"],
                int(fila["anio"]),
                int(fila["duracion_seg"]),
            ))
        self._versiones = [
            (int(f["cancion_id"]), int(f["version_de_id"]), f["tipo"])
            for f in cargar_texto(RUTA_VERSIONES)
        ]

    def listar(self):
        return list(self._canciones)

    def buscar(self, id_cancion):
        for c in self._canciones:
            if c.id == id_cancion:
                return c
        return None

    def versiones_directas(self, id_cancion):
        """IDs de canciones que son versión directa (cover/live/remix) de id_cancion."""
        return [cid for cid, original_id, tipo in self._versiones if original_id == id_cancion]

    def tipo_de_version(self, id_cancion):
        for cid, original_id, tipo in self._versiones:
            if cid == id_cancion:
                return tipo
        return None


def versiones_de(biblioteca, id_cancion):
    """Devuelve la lista de ids de todas las versiones derivadas de
    una canción: sus covers/vivos/remixes directos, y también las
    versiones de esas versiones (recursivo)."""
    directas = biblioteca.versiones_directas(id_cancion)
    if not directas:
        return []  # CASO BASE: no tiene versiones derivadas
    resultado = list(directas)
    for v in directas:  # CASO RECURSIVO
        resultado += versiones_de(biblioteca, v)
    return resultado
