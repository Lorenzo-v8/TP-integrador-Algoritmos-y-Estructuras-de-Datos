from src.tads.lista_enlazada import ListaEnlazada
from src.excepciones import PilaVaciaError


class Pila:
    """TAD pila implementado sobre ListaEnlazada."""

    def __init__(self):
        self._datos = ListaEnlazada()

    def apilar(self, dato):
        self._datos.insertar_al_inicio(dato)

    def desapilar(self):
        if self.esta_vacia():
            raise PilaVaciaError("No se puede desapilar: la pila está vacía.")

        return self._datos.extraer_primero()

    def ver_tope(self):
        if self.esta_vacia():
            raise PilaVaciaError("No se puede ver el tope: la pila está vacía.")

        return self._datos.buscar_primero()

    def esta_vacia(self):
        return self._datos.esta_vacia()
