from src.config import TEMA
from src.dominio.biblioteca import Biblioteca, versiones_de

TEMAS = {
    "pokedex": "Pokédex",
    "recetario": "Recetario",
    "musica": "Biblioteca musical",
}

biblioteca = Biblioteca()


def pendiente():
    print("Todavía no está implementado. Completar en la entrega que corresponde.")


def listar_catalogo():
    print()
    for i, cancion in enumerate(biblioteca.listar(), start=1):
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
        elif opcion == "5":
            mostrar_recursion()
        elif opcion in {"2", "3", "4", "6", "7", "8", "9"}:
            pendiente()
        else:
            print("Opción inválida.")


if __name__ == "__main__":
    main()
