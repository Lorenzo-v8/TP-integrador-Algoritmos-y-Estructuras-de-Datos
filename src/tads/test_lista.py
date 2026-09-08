from src.tads.lista_enlazada import ListaEnlazada


lista = ListaEnlazada()

print("¿Está vacía?", lista.esta_vacia())
print("Tamaño:", lista.tamanio())

lista.insertar_al_final("A")
lista.insertar_al_final("B")
lista.insertar_al_inicio("Inicio")

print("Después de insertar:")
print("¿Está vacía?", lista.esta_vacia())
print("Tamaño:", lista.tamanio())

print("Elementos:")
for elemento in lista:
    print(elemento)

print("Buscar B:", lista.buscar("B"))
print("Buscar X:", lista.buscar("X"))

lista.eliminar("B")

print("Después de eliminar B:")
for elemento in lista:
    print(elemento)

print("Tamaño final:", lista.tamanio())