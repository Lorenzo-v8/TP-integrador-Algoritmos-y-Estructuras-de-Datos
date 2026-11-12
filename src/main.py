from src.config import TEMA
from src.dominio.cancion import Cancion
from src.dominio.biblioteca import Biblioteca, versiones_de
from src.dominio.playlist import Playlist
from src.tads.pila import Pila
from src.tads.cola import Cola
from src.excepciones import (
    PilaVaciaError,
    ColaVaciaError,
    ColeccionLlenaError,
    ColeccionVaciaError,
    ArchivoInvalidoError,
    ItemNoEncontradoError,
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


def refrescar_catalogo():
    """Vuelve a tomar el catálogo de la biblioteca (después de alta/baja/modificación/carga)."""
    global catalogo_actual, ordenado_por
    catalogo_actual = biblioteca.listar()
    ordenado_por = None


def pedir_texto(etiqueta, actual=None):
    sufijo = f" [{actual}]" if actual is not None else ""
    valor = input(f"{etiqueta}{sufijo}: ").strip()
    return valor if valor else actual


def pedir_numero(etiqueta, actual=None):
    sufijo = f" [{actual}]" if actual is not None else ""
    valor = input(f"{etiqueta}{sufijo}: ").strip()
    if not valor:
        return actual
    if not valor.isdigit():
        return None
    return int(valor)


def pedir_cancion(id_cancion, actual=None):
    """Pide los datos de una canción. Con `actual`, Enter conserva el valor."""
    titulo = pedir_texto("Título", actual.titulo if actual else None)
    artista = pedir_texto("Artista", actual.artista if actual else None)
    album = pedir_texto("Álbum", actual.album if actual else None)
    genero = pedir_texto("Género", actual.genero if actual else None)
    anio = pedir_numero("Año", actual.anio if actual else None)
    duracion = pedir_numero("Duración (seg)", actual.duracion_seg if actual else None)
    if not (titulo and artista and album and genero) or anio is None or duracion is None:
        return None
    if anio > 65535 or duracion > 65535:
        return None
    return Cancion(id_cancion, titulo, artista, album, genero, anio, duracion)


def mostrar_detalle():
    print()
    entrada = input("Ingresá el id de una canción: ").strip()
    if not entrada.isdigit():
        print("Id inválido.")
        return
    c = biblioteca.buscar(int(entrada))
    if c is None:
        print("No existe una canción con ese id.")
        return
    minutos, segundos = divmod(c.duracion_seg, 60)
    print(f"ID:        {c.id}")
    print(f"Título:    {c.titulo}")
    print(f"Artista:   {c.artista}")
    print(f"Álbum:     {c.album}")
    print(f"Género:    {c.genero}")
    print(f"Año:       {c.anio}")
    print(f"Duración:  {minutos}:{segundos:02d}")
    tipo = biblioteca.tipo_de_version(c.id)
    if tipo:
        print(f"Es una versión de tipo: {tipo}")


def alta_cancion():
    print()
    id_cancion = pedir_numero("Id")
    if id_cancion is None:
        print("Id inválido.")
        return
    if biblioteca.buscar(id_cancion) is not None:
        print("Ya existe una canción con ese id.")
        return
    nueva = pedir_cancion(id_cancion)
    if nueva is None:
        print("Datos inválidos.")
        return
    biblioteca.alta_cancion(nueva)
    refrescar_catalogo()
    print(f"Alta guardada en el binario: {nueva}")


def baja_cancion():
    print()
    id_cancion = pedir_numero("Id de la canción a dar de baja")
    if id_cancion is None:
        print("Id inválido.")
        return
    biblioteca.baja_cancion(id_cancion)
    refrescar_catalogo()
    print("Baja guardada en el binario.")


def modificar_cancion():
    print()
    id_cancion = pedir_numero("Id de la canción a modificar")
    if id_cancion is None:
        print("Id inválido.")
        return
    actual = biblioteca.buscar(id_cancion)
    if actual is None:
        print("No existe una canción con ese id.")
        return
    print("Enter conserva el valor actual.")
    nueva = pedir_cancion(id_cancion, actual)
    if nueva is None:
        print("Datos inválidos.")
        return
    biblioteca.modificar_cancion(id_cancion, nueva)
    refrescar_catalogo()
    print(f"Registro actualizado en el binario: {nueva}")


def mostrar_archivos():
    print()
    print("1. Guardar catálogo en CSV")
    print("2. Cargar catálogo desde CSV")
    print("3. Guardar catálogo en binario")
    print("4. Cargar catálogo desde binario")
    print("5. Alta de canción (persistente)")
    print("6. Baja de canción (persistente)")
    print("7. Modificar canción (persistente)")
    print("0. Volver")
    opcion = input("> ").strip()
    try:
        if opcion == "1":
            biblioteca.guardar_csv()
            print("Catálogo guardado en data/catalogo.csv.")
        elif opcion == "2":
            biblioteca.cargar_csv()
            refrescar_catalogo()
            print("Catálogo cargado desde data/catalogo.csv.")
        elif opcion == "3":
            biblioteca.guardar_binario()
            print("Catálogo guardado en data/catalogo.bin.")
        elif opcion == "4":
            biblioteca.cargar_binario()
            refrescar_catalogo()
            print("Catálogo cargado desde data/catalogo.bin.")
        elif opcion == "5":
            alta_cancion()
        elif opcion == "6":
            baja_cancion()
        elif opcion == "7":
            modificar_cancion()
        elif opcion == "0":
            return
        else:
            print("Opción inválida.")
    except (ArchivoInvalidoError, ItemNoEncontradoError, FileNotFoundError) as e:
        print(f"No se pudo completar la operación: {e}")


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
        elif opcion == "2":
            mostrar_detalle()
        elif opcion == "9":
            mostrar_archivos()
        else:
            print("Opción inválida.")


if __name__ == "__main__":
    main()