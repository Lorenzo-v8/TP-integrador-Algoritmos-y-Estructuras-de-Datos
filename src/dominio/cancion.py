class Cancion:
    """Representa una canción de la biblioteca musical."""

    def __init__(self, id, titulo, artista, album, genero, anio, duracion_seg):
        self.id = id
        self.titulo = titulo
        self.artista = artista
        self.album = album
        self.genero = genero
        self.anio = anio
        self.duracion_seg = duracion_seg

    def __str__(self):
        return f"{self.titulo} — {self.artista} ({self.anio})"
