# Informe técnico — Ajedrez Offline

## 1. Análisis del problema

Se propone una aplicación de escritorio que permita a dos personas jugar ajedrez en el mismo computador sin depender de Internet. El usuario necesita un tablero legible, controles sencillos y una validación confiable de las reglas para evitar movimientos ilegales.

**Público objetivo:** estudiantes y personas que quieran jugar una partida casual de ajedrez de forma local.

**Alcance funcional:** iniciar una partida, seleccionar y mover piezas, validar turnos y movimientos, consultar el historial, deshacer, girar el tablero, cambiar el tema y reconocer los principales estados de finalización.

**Limitaciones:** no tiene modo en línea, inteligencia artificial, reloj, cuentas, persistencia de partidas ni base de datos. Tampoco ofrece controles para acordar tablas o reclamar manualmente tablas por triple repetición o regla de 50 movimientos.

## 2. Diseño inicial

Se separaron dos responsabilidades principales:

1. **Modelo:** mantiene el estado de la partida, valida las acciones y expone operaciones de alto nivel.
2. **Interfaz:** presenta el tablero, recibe clics, muestra el estado y llama a los métodos del modelo.

También se definió una abstracción de tema visual para que la ventana pueda cambiar entre dos paletas sin conocer cómo se construye cada una.

## 3. Arquitectura

Se utiliza una arquitectura sencilla por capas, cercana a MVC:

- `ajedrez/modelos/partida.py`: lógica de aplicación y estado de la partida.
- `ajedrez/interfaz/tema.py`: abstracción de tema e implementaciones concretas.
- `ajedrez/interfaz/ventana.py`: ventana, tablero gráfico, eventos y controles.
- `main.py`: punto de entrada.
- `tests/test_partida.py`: pruebas automatizadas del modelo.

El modelo no depende de Tkinter. La interfaz depende del modelo, pero el modelo no necesita conocer los widgets. Esto facilita probar las reglas sin abrir una ventana.

## 4. Aplicación de programación orientada a objetos

| Concepto | Clase o método | Archivo | Aplicación |
|---|---|---|---|
| Clases y objetos | `Partida`, `VentanaAjedrez`, `TemaClasico` | `partida.py`, `ventana.py`, `tema.py` | Cada clase representa una responsabilidad; la ventana crea y utiliza los objetos del modelo y del tema. |
| Encapsulamiento | `Partida.__tablero`, `Partida.__historial_san` | `partida.py` | El estado interno se mantiene privado. Se consulta mediante propiedades y métodos controlados. El historial se entrega como copia. |
| Herencia | `TemaClasico(TemaTablero)`, `TemaOscuro(TemaTablero)` | `tema.py` | Ambos temas heredan el contrato definido por la clase abstracta. |
| Polimorfismo | `colores_casillas()`, `color_seleccion()` y otros métodos | `tema.py`, `ventana.py` | La ventana usa una referencia de tipo `TemaTablero`; el objeto concreto responde con los colores de su propia implementación. |
| Abstracción | `TemaTablero(ABC)` | `tema.py` | Define las operaciones que todo tema debe implementar, sin fijar sus colores concretos. |
| Composición | `VentanaAjedrez` contiene una instancia de `Partida` y una instancia de `TemaTablero` | `ventana.py` | La ventana coordina el modelo y el tema como partes de su funcionamiento. |
| Asociación | La interfaz invoca operaciones de `Partida` | `ventana.py`, `partida.py` | La interfaz conoce el modelo mediante su API pública y presenta los resultados. |

La biblioteca `python-chess` se ocupa de las reglas detalladas del ajedrez. La clase `Partida` encapsula su tablero y proporciona una API de la aplicación; así la interfaz no necesita manipular directamente el motor.

## 5. Construcción de la interfaz

**Biblioteca:** Tkinter, incluida en la biblioteca estándar de Python en la mayoría de las instalaciones.

**Componentes:** un `Canvas` representa el tablero y las piezas; etiquetas informan el turno y el estado; una lista muestra el historial; botones permiten reiniciar, deshacer, girar y cambiar el tema.

**Eventos y callbacks:** el evento `<Button-1>` del tablero llama a `_al_hacer_clic`. Los botones se conectan a métodos como `_nueva_partida`, `_deshacer`, `_girar_tablero` y `_cambiar_tema`. La interfaz traduce coordenadas de pantalla a casillas de ajedrez y solicita los movimientos al modelo.

**Comunicación:** la ventana consulta `pieza_en`, `movimientos_legales_desde`, `mover`, `deshacer` y `mensaje_estado`. No implementa por su cuenta las reglas de movimiento.

## 6. Bibliotecas utilizadas

| Biblioteca | Tipo | Uso | Motivo |
|---|---|---|---|
| `tkinter` | Estándar | Ventana, botones, etiquetas, lienzo y eventos | Permite una GUI de escritorio sin añadir otra dependencia visual. |
| `python-chess` | Externa | Reglas, movimientos legales, notación SAN, detección de jaque y finales | Evita reimplementar de forma incompleta reglas complejas como enroque, captura al paso y promoción. |
| `unittest` | Estándar | Pruebas del modelo | Permite validar el comportamiento con herramientas incluidas en Python. |

Instalación de la dependencia externa:

```bash
python -m pip install -r requirements.txt
```

La aplicación no realiza conexiones de red durante una partida. La conexión puede ser necesaria únicamente para descargar la dependencia durante la instalación inicial, si no está disponible localmente.

## 7. Proceso de desarrollo

1. Se delimitó el alcance a una partida local de dos jugadores.
2. Se identificaron el modelo de partida, el contrato de temas y la ventana principal.
3. Se implementó el modelo y su encapsulamiento.
4. Se construyó el tablero gráfico y la interacción mediante clics.
5. Se conectaron los controles con la lógica del modelo.
6. Se añadieron historial, deshacer, promoción, giro y temas.
7. Se prepararon pruebas unitarias y documentación de instalación y uso.

## 8. Pruebas

Las pruebas automatizadas están en `tests/test_partida.py` y se ejecutan con:

```bash
python -m unittest discover -s tests -v
```

| Prueba | Acción realizada | Resultado esperado |
|---|---|---|
| 1. Movimientos iniciales | Consultar destinos legales del peón de e2 y cantidad de movimientos iniciales | El peón de e2 tiene dos destinos legales y la posición inicial tiene veinte movimientos. |
| 2. Movimiento inválido | Intentar mover el peón de e2 a e5 | Se rechaza el movimiento y las blancas conservan el turno. |
| 3. Deshacer | Mover e2-e4 y deshacer | Se restaura el turno de blancas y se elimina la jugada del historial. |
| 4. Jaque mate | Ejecutar la secuencia del mate del pastor | La partida termina con resultado `0-1` y un mensaje de jaque mate. |
| 5. Nueva partida | Realizar una jugada y reiniciar | El historial queda vacío y se restaura la posición inicial. |

Las pruebas cubren la lógica del modelo; no simulan clics ni sustituyen una comprobación manual de la interfaz en el sistema operativo de entrega. Se deben ejecutar en un entorno que tenga instalada la dependencia `python-chess`.

## 9. Dificultades técnicas abordadas

**Validar correctamente las reglas de movimiento.** Implementar manualmente jaque, enroque, captura al paso y promoción aumentaría el riesgo de errores. Se integró `python-chess` y se encapsuló dentro de `Partida`, manteniendo separada la interfaz.

**Evitar que la interfaz modifique directamente el estado del juego.** Se creó una API pública en `Partida` para consultar piezas, obtener destinos legales, mover y deshacer. La ventana no necesita modificar el tablero interno.

**Cambiar la apariencia sin duplicar la lógica de dibujo.** Se definió `TemaTablero` como clase abstracta y se implementaron `TemaClasico` y `TemaOscuro`. La ventana usa polimorfismo para obtener colores desde el tema activo.

## 10. Conclusiones

El proyecto integra una interfaz gráfica de escritorio con una arquitectura orientada a objetos y separación entre presentación y lógica. Se aplican encapsulamiento, herencia, abstracción, polimorfismo y relaciones entre objetos en responsabilidades que participan en el funcionamiento.

Como mejoras futuras se podrían incorporar un reloj, guardado y recuperación de partidas, modo contra una IA local, soporte de accesibilidad y controles para reclamar tablas. Estas mejoras no son necesarias para el alcance básico.
