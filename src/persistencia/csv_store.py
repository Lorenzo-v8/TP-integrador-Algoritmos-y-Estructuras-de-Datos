import csv

from src.dominio.cancion import Cancion
from src.excepciones import ArchivoInvalidoError

COLUMNAS = ["id", "titulo", "artista", "album", "genero", "anio", "duracion_seg"]


def guardar_csv(path, canciones):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(COLUMNAS)
        for c in canciones:
            w.writerow([c.id, c.titulo, c.artista, c.album, c.genero, c.anio, c.duracion_seg])


def cargar_csv(path):
    """Carga secuencial del CSV. Lanza ArchivoInvalidoError si está roto."""
    try:
        with open(path, newline="", encoding="utf-8-sig") as f:
            r = csv.reader(f)
            if next(r, None) != COLUMNAS:
                raise ArchivoInvalidoError("Header CSV incorrecto")
            canciones = []
            for fila in r:
                if not fila:  # línea en blanco
                    continue
                i, t, ar, al, g, a, d = fila  # ValueError si faltan o sobran columnas
                canciones.append(Cancion(int(i), t, ar, al, g, int(a), int(d)))
            return canciones
    except (ValueError, csv.Error, UnicodeDecodeError) as e:
        raise ArchivoInvalidoError(f"CSV roto: {e}")