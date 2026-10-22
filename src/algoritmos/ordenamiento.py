def ordenar_seleccion(coleccion, clave):
    """Ordenamiento por selección. Devuelve una nueva secuencia, no usa sorted."""
    resultado = list(coleccion)
    n = len(resultado)
    for i in range(n - 1):
        pos_min = i
        for j in range(i + 1, n):
            if clave(resultado[j]) < clave(resultado[pos_min]):
                pos_min = j
        resultado[i], resultado[pos_min] = resultado[pos_min], resultado[i]
    return resultado


def ordenar_insercion(coleccion, clave):
    """Ordenamiento por inserción. Devuelve una nueva secuencia, no usa sorted."""
    resultado = list(coleccion)
    for i in range(1, len(resultado)):
        actual = resultado[i]
        j = i - 1
        while j >= 0 and clave(resultado[j]) > clave(actual):
            resultado[j + 1] = resultado[j]
            j -= 1
        resultado[j + 1] = actual
    return resultado
