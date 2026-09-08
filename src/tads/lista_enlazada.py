from src.tads.nodo import Nodo
class ListaEnlazada:
    """TAD lista enlazada simple. No usar list de Python por debajo."""

    def __init__(self):
        self._primero = None
        self._tamanio = 0

    def esta_vacia(self):
        return self._primero is None

    def tamanio(self):
        return self._tamanio

    def insertar_al_inicio(self, dato):
        nuevo = Nodo(dato)
        nuevo.siguiente = self._primero
        self._primero = nuevo
        self._tamanio += 1

    def insertar_al_final(self, dato):
        nuevo = Nodo(dato)

        if self.esta_vacia():
            self._primero = nuevo
        else:
            actual = self._primero

            while actual.siguiente is not None:
                actual = actual.siguiente

            actual.siguiente = nuevo

        self._tamanio += 1

    def insertar_ordenado(self, dato, clave):
        nuevo = Nodo(dato)

        if self.esta_vacia():
            self._primero = nuevo
            self._tamanio += 1
            return

        if clave(dato) <= clave(self._primero.dato):
            nuevo.siguiente = self._primero
            self._primero = nuevo
            self._tamanio += 1
            return

        actual = self._primero

        while (
            actual.siguiente is not None
            and clave(actual.siguiente.dato) < clave(dato)
        ):
            actual = actual.siguiente

        nuevo.siguiente = actual.siguiente
        actual.siguiente = nuevo
        self._tamanio += 1

    def eliminar(self, dato):
        if self.esta_vacia():
            return False

        if self._primero.dato == dato:
            self._primero = self._primero.siguiente
            self._tamanio -= 1
            return True

        actual = self._primero

        while actual.siguiente is not None:
            if actual.siguiente.dato == dato:
                actual.siguiente = actual.siguiente.siguiente
                self._tamanio -= 1
                return True

            actual = actual.siguiente

        return False

    def buscar(self, dato):
        actual = self._primero

        while actual is not None:
            if actual.dato == dato:
                return actual.dato

            actual = actual.siguiente

        return None
    def __iter__(self):
        actual = self._primero

        while actual is not None:
            yield actual.dato
            actual = actual.siguiente