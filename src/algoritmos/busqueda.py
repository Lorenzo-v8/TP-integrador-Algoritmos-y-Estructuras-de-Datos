def busqueda_lineal(coleccion, clave, obtener_clave):
    """Devuelve el ítem cuya clave coincide, o None."""
    for elemento in coleccion:
        if obtener_clave(elemento) == clave:
            return elemento
    return None


def busqueda_binaria(coleccion_ordenada, clave, obtener_clave):
    """La colección tiene que estar ordenada por obtener_clave."""
    izq = 0
    der = len(coleccion_ordenada) - 1
    while izq <= der:
        medio = (izq + der) // 2
        valor = obtener_clave(coleccion_ordenada[medio])
        if valor == clave:
            return coleccion_ordenada[medio]
        elif valor < clave:
            izq = medio + 1
        else:
            der = medio - 1
    return None
