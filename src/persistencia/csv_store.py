import csv
from excepciones import ArchivoInvalidoError

COLUMNAS = ["id", "titulo", "artista", "duracion"]

def guardar_csv(path, canciones):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(COLUMNAS)
        for c in canciones:
            w.writerow([c.id, c.titulo, c.artista, c.duracion])

def cargar_csv(path):
    try:
        with open(path, newline="", encoding="utf-8") as f:
            r = csv.reader(f)
            if next(r, None) != COLUMNAS:
                raise ArchivoInvalidoError("Header CSV incorrecto")
            return [Cancion(int(i), t, a, int(d)) for i, t, a, d in r]
    except (ValueError, csv.Error) as e:   # fila rota: faltan columnas, int inválido
        raise ArchivoInvalidoError(f"CSV roto: {e}")