# TP integrador — AyED C2 2026

Repositorio del grupo. Partir de este esqueleto. ## Limitaciones

- La búsqueda binaria solo funciona si la colección está ordenada.
- Los textos del archivo binario se cortan si superan su largo fijo (título 60 bytes, artista y álbum 40, género 20).
- Las bajas en el binario son lógicas: el archivo no se compacta.
- Las listas enlazadas no tienen puntero al final, por eso encolar e insertar al final recorren toda la lista.
- Las versiones (covers, vivos, remixes) se leen solo de `data/versiones.txt` y no se guardan en el binario.
- La playlist tiene un tope de 10 canciones.
## Entregas

Cada vencimiento se marca con un tag. Ver `GIT.md`.

| Tag | Vence |
| --- | --- |
| `preentrega` (opcional, solo repo) | domingo 30-ago-2026 23:59 |
| `entrega-1` | domingo 06-sep-2026 23:59 |
| `entrega-2` | domingo 20-sep-2026 23:59 |
| `entrega-3` | domingo 04-oct-2026 23:59 |
| `entrega-4` | domingo 01-nov-2026 23:59 |
| `entrega-5` | domingo 15-nov-2026 23:59 |
| `entrega-6` | domingo 22-nov-2026 23:59 |

Defensa oral (reemplaza el 2do parcial): 25 y 27-nov-2026.

La cátedra corrige el **tag**, no el último commit suelto de `main`.

El grupo se avisa por mail a diego.ambrossio@unab.edu.ar **y** angel.bianco@unab.edu.ar. Ver `GIT.md`.
