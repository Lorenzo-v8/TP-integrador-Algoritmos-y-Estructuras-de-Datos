import time
from src.dominio.biblioteca import Biblioteca
from src.algoritmos.busqueda import busqueda_lineal, busqueda_binaria
from src.algoritmos.ordenamiento import ordenar_seleccion, ordenar_insercion

biblioteca = Biblioteca()
catalogo = biblioteca.listar()          # 67 canciones (original)
catalogo_grande = catalogo * 10         # 670 canciones (agrandado x10)

clave = lambda c: c.titulo


def medir(funcion, *args):
    inicio = time.perf_counter()
    resultado = funcion(*args)
    fin = time.perf_counter()
    return fin - inicio


# --- Búsqueda lineal ---
t1 = medir(busqueda_lineal, catalogo, "As It Was", clave)
t2 = medir(busqueda_lineal, catalogo_grande, "As It Was", clave)
print(f"busqueda lineal (n={len(catalogo)}): {t1:.6f} s")
print(f"busqueda lineal (n={len(catalogo_grande)}): {t2:.6f} s")

# --- Preparar catálogos ordenados para la binaria ---
catalogo_ordenado = ordenar_seleccion(catalogo, clave)
catalogo_grande_ordenado = ordenar_seleccion(catalogo_grande, clave)

# --- Búsqueda binaria ---
t3 = medir(busqueda_binaria, catalogo_ordenado, "As It Was", clave)
t4 = medir(busqueda_binaria, catalogo_grande_ordenado, "As It Was", clave)
print(f"busqueda binaria (n={len(catalogo_ordenado)}): {t3:.6f} s")
print(f"busqueda binaria (n={len(catalogo_grande_ordenado)}): {t4:.6f} s")

# --- Ordenar por selección ---
t5 = medir(ordenar_seleccion, catalogo, clave)
t6 = medir(ordenar_seleccion, catalogo_grande, clave)
print(f"ordenar seleccion (n={len(catalogo)}): {t5:.6f} s")
print(f"ordenar seleccion (n={len(catalogo_grande)}): {t6:.6f} s")

# --- Ordenar por inserción ---
t7 = medir(ordenar_insercion, catalogo, clave)
t8 = medir(ordenar_insercion, catalogo_grande, clave)
print(f"ordenar insercion (n={len(catalogo)}): {t7:.6f} s")
print(f"ordenar insercion (n={len(catalogo_grande)}): {t8:.6f} s")
