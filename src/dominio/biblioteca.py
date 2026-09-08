from src.tads.lista_enlazada import ListaEnlazada


class Biblioteca:
    def __init__(self):
        self._canciones = ListaEnlazada()

    def agregar_cancion(self, cancion):
        self._canciones.insertar_al_final(cancion)

    def __iter__(self):
        return iter(self._canciones)
    