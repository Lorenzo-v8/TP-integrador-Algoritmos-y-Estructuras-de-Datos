print("INICIO DE TEST COLA")
from src.tads.cola import Cola


cola = Cola()

print("¿Está vacía?", cola.esta_vacia())

cola.encolar("A")
cola.encolar("B")
cola.encolar("C")

print("¿Está vacía?", cola.esta_vacia())
print("Frente:", cola.ver_frente())

print("Desencolar:", cola.desencolar())
print("Nuevo frente:", cola.ver_frente())

print("Desencolar:", cola.desencolar())
print("Desencolar:", cola.desencolar())

print("¿Está vacía?", cola.esta_vacia())
print("Desencolar cola vacía:", cola.desencolar())