from src.tads.lista_enlazada import ListaEnlazada
from src.excepciones import ColaVaciaError


class Cola:
    """TAD cola implementado sobre ListaEnlazada."""

    def __init__(self):
        self._datos = ListaEnlazada()

    def encolar(self, dato):
        self._datos.insertar_al_final(dato)

    def desencolar(self):
        if self.esta_vacia():
            raise ColaVaciaError("No se puede desencolar: la cola está vacía.")

        return self._datos.extraer_primero()

    def ver_frente(self):
        if self.esta_vacia():
            raise ColaVaciaError("No se puede ver el frente: la cola está vacía.")

        return self._datos.ver_primero()

    def esta_vacia(self):
        return self._datos.esta_vacia()
