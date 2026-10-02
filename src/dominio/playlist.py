from src.tads.lista_enlazada import ListaEnlazada
from src.excepciones import ColeccionLlenaError, ColeccionVaciaError


class Playlist:
    """Colección principal del dominio: una playlist con tope máximo
    de canciones, construida sobre ListaEnlazada."""

    def __init__(self, capacidad_maxima=10):
        self._canciones = ListaEnlazada()
        self._capacidad_maxima = capacidad_maxima

    def agregar(self, cancion):
        if self._canciones.tamanio() >= self._capacidad_maxima:
            raise ColeccionLlenaError(
                f"La playlist ya tiene el máximo de {self._capacidad_maxima} canciones."
            )
        self._canciones.insertar_al_final(cancion)

    def quitar(self, cancion):
        if self._canciones.esta_vacia():
            raise ColeccionVaciaError("La playlist está vacía.")
        return self._canciones.eliminar(cancion)

    def listar(self):
        return list(self._canciones)

    def tamanio(self):
        return self._canciones.tamanio()

    def esta_vacia(self):
        return self._canciones.esta_vacia()

    def __iter__(self):
        return iter(self._canciones)
