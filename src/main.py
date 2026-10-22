from src.config import TEMA
from src.dominio.biblioteca import Biblioteca, versiones_de
from src.dominio.playlist import Playlist
from src.tads.pila import Pila
from src.tads.cola import Cola
from src.excepciones import (
    PilaVaciaError,
    ColaVaciaError,
    ColeccionLlenaError,
    ColeccionVaciaError,
)
from src.algoritmos.busqueda import busqueda_lineal, busqueda_binaria
from src.algoritmos.ordenamiento import ordenar_seleccion, ordenar_insercion

TEMAS = {
    "pokedex": "Pokédex",
    "recetario": "Recetario",
    "musica": "Biblioteca musical",
}

biblioteca = Biblioteca()
playlist = Playlist(capacidad_maxima=10)
historial = Pila()
cola_reproduccion = Cola()

catalogo_actual = biblioteca.listar()
ordenado_por = None  # None, "titulo" o "anio"

CRITERIOS = {
    "1": ("titulo", lambda c: c.titulo),
    "2": ("anio", lambda c: c.anio),
}


def pendiente():
    print("Todavía no está implementado. Completar en la entrega que corresponde.")


def listar_catalogo():
    print()
    for i, cancion in enumerate(catalogo_actual, start=1):
        print(f"{i}. {cancion}")


def mostrar_recursion():
    print()
    entrada = input("Ingresá el id de una canción: ").strip()
    if not entrada.isdigit():
        print("Id inválido.")
        return
    id_cancion = int(entrada)
    cancion = biblioteca.buscar(id_cancion)
    if cancion is None:
        print("No existe una canción con ese id.")
        return
    ids_versiones = versiones_de(biblioteca, id_cancion)
    if not ids_versiones:
        print(f"'{cancion.titulo}' no tiene versiones derivadas.")
        return
    print(f"Versiones derivadas de '{cancion.titulo}':")
    for vid in ids_versiones:
        version = biblioteca.buscar(vid)
        tipo = biblioteca.tipo_de_version(vid)
        print(f"  - {version} [{tipo}]")


def mostrar_playlist():
    print()
    entrada = input("Ingresá el id de una canción para agregar a la playlist: ").strip()
    if not entrada.isdigit():
        print("Id inválido.")
        return
    cancion = biblioteca.buscar(int(entrada))
    if cancion is None:
        print("No existe una canción con ese id.")
        return
    try:
        playlist.agregar(cancion)
        historial.apilar(cancion)
        print(f"Agregada a la playlist: {cancion}")
    except ColeccionLlenaError as e:
        print(f"No se pudo agregar: {e}")

    print()
    print(f"Playlist actual ({playlist.tamanio()}/10):")
    for c in playlist.listar():
        print(f"  - {c}")


def mostrar_historial():
    print()
    try:
        ultima = historial.desapilar()
        print(f"Última agregada (se saca del historial): {ultima}")
    except PilaVaciaError as e:
        print(f"No se pudo deshacer: {e}")


def mostrar_cola():
    print()
    opcion = input("¿(e)ncolar o (d)esencolar? ").strip().lower()
    if opcion == "e":
        entrada = input("Ingresá el id de una canción para encolar: ").strip()
        if not entrada.isdigit():
            print("Id inválido.")
            return
        cancion = biblioteca.buscar(int(entrada))
        if cancion is None:
            print("No existe una canción con ese id.")
            return
        cola_reproduccion.encolar(cancion)
        print(f"Encolada: {cancion}")
    elif opcion == "d":
        try:
            siguiente = cola_reproduccion.desencolar()
            print(f"Reproduciendo: {siguiente}")
        except ColaVaciaError as e:
            print(f"No se pudo desencolar: {e}")
    else:
        print("Opción inválida.")


def mostrar_buscar():
    print()
    print("Buscar por: 1) Título (lineal) 2) Título (binaria)")
    tipo = input("> ").strip()

    if tipo == "1":
        valor = input("Ingresá el título a buscar: ").strip()
        resultado = busqueda_lineal(catalogo_actual, valor, obtener_clave=lambda c: c.titulo)
    elif tipo == "2":
        if ordenado_por != "titulo":
            print("El catálogo no está ordenado por título. Ordenalo primero (opción 4).")
            return
        valor = input("Ingresá el título a buscar: ").strip()
        resultado = busqueda_binaria(catalogo_actual, valor, obtener_clave=lambda c: c.titulo)
    else:
        print("Opción inválida.")
        return

    if resultado is None:
        print("No encontrado.")
    else:
        print(f"Encontrado: {resultado}")


def mostrar_ordenar():
    global catalogo_actual, ordenado_por

    print()
    print("Ordenar por: 1) Título 2) Año")
    criterio_opcion = input("> ").strip()
    if criterio_opcion not in CRITERIOS:
        print("Opción inválida.")
        return
    nombre_criterio, clave = CRITERIOS[criterio_opcion]

    print("[1] Selección  [2] Inserción")
    metodo = input("> ").strip()
    if metodo == "1":
        catalogo_actual = ordenar_seleccion(catalogo_actual, clave)
        nombre_metodo = "selección"
    elif metodo == "2":
        catalogo_actual = ordenar_insercion(catalogo_actual, clave)
        nombre_metodo = "inserción"
    else:
        print("Opción inválida.")
        return

    ordenado_por = nombre_criterio
    print(f"Catálogo ordenado por {nombre_criterio} ({nombre_metodo}).")


def mostrar_menu():
    nombre = TEMAS.get(TEMA, TEMA or "(sin tema)")
    print()
    print(f"=== {nombre} — AyED C2 2026 ===")
    print("1. Listar catálogo")
    print("2. Ver detalle")
    print("3. Buscar")
    print("4. Ordenar")
    print("5. Operación recursiva")
    print("6. Colección principal (equipo / menú / playlist)")
    print("7. Historial (pila)")
    print("8. Cola")
    print("9. Guardar / cargar archivos")
    print("0. Salir")


def main():
    if TEMA not in TEMAS:
        print("Seteá TEMA en src/config.py: 'pokedex', 'recetario' o 'musica'.")
        return

    opcion = None
    while opcion != "0":
        mostrar_menu()
        opcion = input("> ").strip()
        if opcion == "0":
            print("Chau.")
        elif opcion == "1":
            listar_catalogo()
        elif opcion == "3":
            mostrar_buscar()
        elif opcion == "4":
            mostrar_ordenar()
        elif opcion == "5":
            mostrar_recursion()
        elif opcion == "6":
            mostrar_playlist()
        elif opcion == "7":
            mostrar_historial()
        elif opcion == "8":
            mostrar_cola()
        elif opcion in {"2", "9"}:
            pendiente()
        else:
            print("Opción inválida.")


if __name__ == "__main__":
    main()
