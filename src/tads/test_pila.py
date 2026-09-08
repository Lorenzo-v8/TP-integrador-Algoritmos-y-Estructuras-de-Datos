print("INICIO DE TEST PILA")
from src.tads.pila import Pila


pila = Pila()

print("¿Está vacía?", pila.esta_vacia())

pila.apilar("A")
pila.apilar("B")
pila.apilar("C")

print("¿Está vacía?", pila.esta_vacia())
print("Tope:", pila.ver_tope())

print("Desapilar:", pila.desapilar())
print("Nuevo tope:", pila.ver_tope())

print("Desapilar:", pila.desapilar())
print("Desapilar:", pila.desapilar())

print("¿Está vacía?", pila.esta_vacia())
print("Desapilar pila vacía:", pila.desapilar())
