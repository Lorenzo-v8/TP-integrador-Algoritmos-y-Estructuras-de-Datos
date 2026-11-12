import os
import struct

from src.dominio.cancion import Cancion
from src.excepciones import ArchivoInvalidoError

MAGIC = b"CTLG"
VERSION = 1
HEADER = struct.Struct("<4sHHI")
REGISTRO = struct.Struct("<I60s40s40s20sHH?")


def _txt(s, n):
    return s.encode("utf-8")[:n]  # struct rellena con \0 si es más corto


def _dec(b):
    return b.rstrip(b"\0").decode("utf-8", errors="ignore")


def _pack(c, activo=True):
    return REGISTRO.pack(c.id, _txt(c.titulo, 60), _txt(c.artista, 40),
                         _txt(c.album, 40), _txt(c.genero, 20),
                         c.anio, c.duracion_seg, activo)


def _unpack(data):
    i, t, ar, al, g, anio, dur, activo = REGISTRO.unpack(data)
    return Cancion(i, _dec(t), _dec(ar), _dec(al), _dec(g), anio, dur), activo


def _offset(pos):
    return HEADER.size + pos * REGISTRO.size


def _leer_header(f):
    """Valida el header y devuelve la cantidad de registros."""
    raw = f.read(HEADER.size)
    if len(raw) < HEADER.size:
        raise ArchivoInvalidoError("Archivo más corto que el header")
    magia, version, tam, cant = HEADER.unpack(raw)
    if magia != MAGIC:
        raise ArchivoInvalidoError("Magia incorrecta")
    if tam != REGISTRO.size:
        raise ArchivoInvalidoError("Tamaño de registro incompatible")
    if os.fstat(f.fileno()).st_size < HEADER.size + cant * tam:
        raise ArchivoInvalidoError("Archivo truncado")
    return cant


def guardar_binario(path, canciones):
    canciones = list(canciones)
    with open(path, "wb") as f:
        f.write(HEADER.pack(MAGIC, VERSION, REGISTRO.size, len(canciones)))
        for c in canciones:
            f.write(_pack(c))


def cargar_binario(path):
    """Devuelve la lista de canciones activas (ignora las bajas lógicas)."""
    with open(path, "rb") as f:
        cant = _leer_header(f)
        regs = (_unpack(f.read(REGISTRO.size)) for _ in range(cant))
        return [c for c, activo in regs if activo]


def buscar_posicion(path, id_cancion):
    """Posición (0-based) del registro activo con ese id, o None."""
    with open(path, "rb") as f:
        cant = _leer_header(f)
        for pos in range(cant):
            i, *_, activo = REGISTRO.unpack(f.read(REGISTRO.size))
            if i == id_cancion and activo:
                return pos
    return None


def actualizar_registro(path, pos, cancion):
    """Reescribe SOLO el registro `pos` usando seek (no toca el resto)."""
    with open(path, "r+b") as f:
        cant = _leer_header(f)
        if not 0 <= pos < cant:
            raise IndexError("Posición fuera de rango")
        f.seek(_offset(pos))
        f.write(_pack(cancion))


def baja_registro(path, pos):
    """Baja lógica: marca activo=False sin mover ni reescribir el resto."""
    with open(path, "r+b") as f:
        cant = _leer_header(f)
        if not 0 <= pos < cant:
            raise IndexError("Posición fuera de rango")
        f.seek(_offset(pos))
        c, _ = _unpack(f.read(REGISTRO.size))
        f.seek(_offset(pos))
        f.write(_pack(c, activo=False))


def alta_registro(path, cancion):
    """Agrega un registro al final y actualiza la cantidad en el header."""
    with open(path, "r+b") as f:
        cant = _leer_header(f)
        f.seek(0, os.SEEK_END)
        f.write(_pack(cancion))
        f.seek(0)
        f.write(HEADER.pack(MAGIC, VERSION, REGISTRO.size, cant + 1))