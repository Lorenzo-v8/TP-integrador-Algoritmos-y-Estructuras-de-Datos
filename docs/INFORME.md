# Informe del TP

## 1. Grupo y tema

* **Tema:** Biblioteca musical

* **Por qué lo eligieron:**
  Elegimos el tema Biblioteca musical porque nos permite trabajar con una entidad clara y fácil de representar mediante estructuras de datos. Una canción posee información concreta como título, artista, álbum, año y duración. Además, el dominio permite incorporar las estructuras requeridas por el trabajo práctico de manera natural: una lista enlazada para el catálogo, una playlist como colección principal, una pila para el historial de reproducción y una cola para las canciones pendientes. También permite implementar posteriormente una relación recursiva mediante las distintas versiones de una canción, como covers, versiones en vivo y remixes.

## 2. Modelo

Un ítem del catálogo es una **Canción**.

Cada canción contiene:

* título
* artista
* álbum
* año
* duración en segundos

El catálogo se representa mediante una **ListaEnlazada**, que contiene las canciones disponibles en la biblioteca.

La colección principal del dominio será una **Playlist**, también implementada mediante una estructura enlazada.

La **Pila** se utilizará para representar el historial de reproducción. La última canción reproducida será la primera que se pueda retirar.

La **Cola** representará las canciones pendientes de reproducción. La primera canción agregada será la primera en salir.

### Relación entre las estructuras

```text
                    Biblioteca
                        │
                        ▼
                 ListaEnlazada
                        │
                        ▼
                     Canción
                        │
          ┌─────────────┼─────────────┐
          ▼             ▼             ▼
      Playlist         Pila          Cola
     (principal)    (historial)   (pendientes)
```

### Tipos utilizados y mutabilidad

| Elemento               | Tipo / estructura | Uso                                  |
| ---------------------- | ----------------- | ------------------------------------ |
| Canción                | Clase             | Representa cada canción del catálogo |
| Catálogo               | ListaEnlazada     | Almacena las canciones               |
| Playlist               | ListaEnlazada     | Representa la colección principal    |
| Historial              | Pila              | Almacena las canciones reproducidas  |
| Cola de reproducción   | Cola              | Almacena las canciones pendientes    |
| Título, artista, álbum | `str`             | Almacenan información textual        |
| Año, duración          | `int`             | Almacenan información numérica       |

Las estructuras de datos utilizadas son **mutables**, ya que durante la ejecución pueden agregarse o eliminarse elementos.

Los valores de tipo `str` e `int` utilizados como atributos de las canciones son **inmutables** en Python.

La clase `Cancion` es mutable porque sus atributos pueden modificarse después de crear el objeto.

## 3. Recursión (E2)

**Función:** `versiones_de(biblioteca, id_cancion)`

- **Caso base:** si la canción no tiene versiones derivadas (`versiones_directas` devuelve una lista vacía) → se devuelve `[]`.
- **Caso recursivo:** se devuelven las versiones directas, más el resultado de aplicar `versiones_de` a cada una de esas versiones (por si a su vez tienen sus propias versiones derivadas).

### Traza para la canción 12 ("Jijiji", Patricio Rey y sus Redonditos de Ricota)

Dato real de `data/versiones.txt`: `13,12,live` → la canción 13 ("Ji Ji Ji", en vivo) es una versión live de la 12.

## 4. TADs (E3)

### Análisis de las mediciones

Medimos con `time.perf_counter`, repitiendo cada medición y tomando el mejor
tiempo, sobre el catálogo original (67 canciones) y copias agrandadas ×10 (670)
y ×50 (3350). Las búsquedas se midieron con un título inexistente para forzar
el peor caso.

- La búsqueda lineal creció en proporción al tamaño (de 3 µs a 30 µs al
  multiplicar n por 10), consistente con O(n).
- La búsqueda binaria casi no cambió (1-2 µs en los tres tamaños), consistente
  con O(log n): cada comparación descarta la mitad del rango.
- Selección e inserción se dispararon: al multiplicar n por 10 el tiempo se
  multiplicó por ~100, consistente con O(n²). Inserción resultó algo más rápida
  que selección porque su bucle interno corta apenas encuentra el lugar,
  mientras que selección siempre recorre lo que queda.

las copias agrandadas repiten las mismas canciones, y la binaria
requiere que la colección esté ordenada (el costo de ordenar no está incluido
en su tiempo).

## 5. Complejidad (E4)

Pendiente para la Entrega 4.

| Operación | Tiempo    | Espacio   | Por qué   |
| --------- | --------- | --------- | --------- |
| Pendiente | Pendiente | Pendiente | Pendiente |

### Mediciones (`time.perf_counter`)

| Operación |  n | segundos |
| --------- | -: | -------: |
| Pendiente |  — |        — |

## 6. Persistencia (E5)

Pendiente para la Entrega 5.

* **Layout del registro binario:** Pendiente.
* **Header:** Pendiente.
* **Cómo se actualiza un registro por posición:** Pendiente.

## Integrantes

| Integrante     | Participación en E1                | Qué puede defender                              |
| -------------- | ---------------------------------- | ----------------------------------------------- |
| Lorenzo Ciprés | Desarrollo y revisión del proyecto | Estructura del proyecto, catálogo, modelo y CLI |
| Camila Poggi   | Desarrollo y revisión del proyecto |Estructura del proyecto, catálogo, modelo y CLI|

Ambos integrantes deben poder explicar cualquier archivo incluido en el tag de la entrega.
