import time
from src.dominio.biblioteca import Biblioteca
from src.algoritmos.busqueda import busqueda_lineal, busqueda_binaria
from src.algoritmos.ordenamiento import ordenar_seleccion, ordenar_insercion

biblioteca = Biblioteca()
catalogo = biblioteca.listar()          # catálogo original

clave = lambda c: c.titulo
NO_EXISTE = "ZZZ no existe"             # peor caso: recorre todo el catálogo


def medir(funcion, *args, repeticiones=100):
    # repite y se queda con el mejor tiempo, para evitar ruido de la máquina
    mejor = None
    for _ in range(repeticiones):
        inicio = time.perf_counter()
        funcion(*args)
        tiempo = time.perf_counter() - inicio
        if mejor is None or tiempo < mejor:
            mejor = tiempo
    return mejor


print("| Operación | n | segundos |")
print("|---|---|---|")

for factor in (1, 10, 50):
    datos = catalogo * factor           # copia agrandada
    n = len(datos)
    ordenado = ordenar_insercion(datos, clave)  # la binaria necesita orden

    # --- Búsqueda lineal ---
    t = medir(busqueda_lineal, datos, NO_EXISTE, clave)
    print(f"| búsqueda lineal | {n} | {t:.6f} |")

    # --- Búsqueda binaria ---
    t = medir(busqueda_binaria, ordenado, NO_EXISTE, clave)
    print(f"| búsqueda binaria | {n} | {t:.6f} |")

    # --- Ordenar por selección ---
    t = medir(ordenar_seleccion, datos, clave, repeticiones=3)
    print(f"| ordenar selección | {n} | {t:.6f} |")

    # --- Ordenar por inserción ---
    t = medir(ordenar_insercion, datos, clave, repeticiones=3)
    print(f"| ordenar inserción | {n} | {t:.6f} |")