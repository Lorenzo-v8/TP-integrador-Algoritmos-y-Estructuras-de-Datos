import os

from src.dominio.cancion import Cancion
from src.excepciones import ArchivoInvalidoError, ItemNoEncontradoError
from src.persistencia import binario, csv_store
from src.persistencia.texto import cargar_texto, DATA
from src.tads.lista_enlazada import ListaEnlazada

RUTA_CANCIONES = DATA / "canciones.txt"
RUTA_VERSIONES = DATA / "versiones.txt"
RUTA_CSV = DATA / "catalogo.csv"
RUTA_BIN = DATA / "catalogo.bin"


class Biblioteca:
    """Representa la biblioteca musical: el catálogo de canciones
    y las relaciones entre una canción y sus versiones derivadas
    (covers, en vivo, remixes)."""

    def __init__(self):
        self._canciones = ListaEnlazada()
        self._versiones = []
        self.cargar_desde_txt()
        # Si ya hay un catálogo binario guardado, tiene prioridad sobre el .txt
        # (así las altas/bajas/modificaciones siguen después de cerrar el programa).
        if os.path.exists(RUTA_BIN):
            try:
                self.cargar_binario()
            except ArchivoInvalidoError as e:
                print(f"Aviso: catálogo binario inválido ({e}). Se usa el .txt.")

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

    # ---------- Persistencia ----------

    def _reconstruir(self, canciones):
        self._canciones = ListaEnlazada()
        for c in canciones:
            self.agregar_cancion(c)

    def _asegurar_bin(self):
        if not os.path.exists(RUTA_BIN):
            self.guardar_binario()

    # 5.1 CSV
    def guardar_csv(self):
        csv_store.guardar_csv(RUTA_CSV, self._canciones)

    def cargar_csv(self):
        self._reconstruir(csv_store.cargar_csv(RUTA_CSV))

    # 5.2 binario completo
    def guardar_binario(self):
        binario.guardar_binario(RUTA_BIN, self._canciones)

    def cargar_binario(self):
        self._reconstruir(binario.cargar_binario(RUTA_BIN))

    # 5.3 / 5.4 ABM persistente
    def alta_cancion(self, cancion):
        self._asegurar_bin()
        self.agregar_cancion(cancion)
        binario.alta_registro(RUTA_BIN, cancion)

    def baja_cancion(self, id_cancion):
        if self.buscar(id_cancion) is None:
            raise ItemNoEncontradoError(f"No existe la canción {id_cancion}")
        self._asegurar_bin()
        pos = binario.buscar_posicion(RUTA_BIN, id_cancion)
        if pos is not None:
            binario.baja_registro(RUTA_BIN, pos)
        self._reconstruir([c for c in self._canciones if c.id != id_cancion])

    def modificar_cancion(self, id_cancion, nueva):
        if self.buscar(id_cancion) is None:
            raise ItemNoEncontradoError(f"No existe la canción {id_cancion}")
        self._asegurar_bin()
        pos = binario.buscar_posicion(RUTA_BIN, id_cancion)
        if pos is not None:
            binario.actualizar_registro(RUTA_BIN, pos, nueva)  # solo ese registro, con seek
        self._reconstruir([nueva if c.id == id_cancion else c for c in self._canciones])


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