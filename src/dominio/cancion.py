class Cancion:
    """Representa una canción de la biblioteca musical."""

    def __init__(self, titulo, artista, album, año, duracion_seg):
        self.titulo = titulo
        self.artista = artista
        self.album = album
        self.año = año
        self.duracion_seg = duracion_seg

    def __str__(self):
        return f"{self.titulo} — {self.artista} ({self.año})"
