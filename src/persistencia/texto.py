from pathlib import Path
from src.excepciones import ArchivoInvalidoError

# texto.py está en src/persistencia/, subimos 3 niveles hasta la raíz del repo
RAIZ = Path(__file__).resolve().parents[2]
DATA = RAIZ / "data"


def cargar_texto(ruta):
    """Carga secuencial de un .txt: un registro por línea, separado por coma.
    Devuelve una lista de dicts. Si el archivo no existe o una línea está
    rota, lanza ArchivoInvalidoError."""
    ruta = Path(ruta)
    if not ruta.exists():
        raise ArchivoInvalidoError(f"No existe el archivo: {ruta}")

    filas = []
    with ruta.open("r", encoding="utf-8") as archivo:
        encabezado = archivo.readline().strip().split(",")
        for linea in archivo:
            linea = linea.strip()
            if not linea:
                continue
            valores = linea.split(",")
            if len(valores) != len(encabezado):
                raise ArchivoInvalidoError(
                    f"Línea con {len(valores)} campos "
                    f"(se esperaban {len(encabezado)}): {linea}"
                )
            filas.append(dict(zip(encabezado, valores)))
    return filas


def guardar_texto(ruta, filas, encabezados):
    """Escribe el catálogo en .txt con la primera línea de encabezados."""
    ruta = Path(ruta)
    with ruta.open("w", encoding="utf-8", newline="") as archivo:
        archivo.write(",".join(encabezados) + "\n")
        for fila in filas:
            campos = [str(fila[clave]) for clave in encabezados]
            archivo.write(",".join(campos) + "\n")
