# ♟ Ajedrez Offline

Juego de ajedrez de escritorio para **dos jugadores en el mismo computador**, desarrollado en Python con programación orientada a objetos. Incluye una interfaz gráfica con Tkinter y valida los movimientos con `python-chess`.

La partida se juega localmente y no necesita conexión a Internet. La única dependencia externa se instala una vez antes de jugar; después de instalarla, el programa no realiza solicitudes de red.

## Características

- Tablero interactivo: selecciona una pieza y después una casilla de destino.
- Validación de movimientos legales y turnos.
- Reglas de jaque, jaque mate, rey ahogado, enroque, captura al paso y promoción.
- Elección de dama, torre, alfil o caballo al promocionar un peón.
- Historial de movimientos en notación algebraica (SAN).
- Deshacer el último movimiento, reiniciar y girar el tablero.
- Tema clásico y tema oscuro.
- Funcionamiento local, sin cuentas, servidor ni servicios en línea.

## Requisitos

- Python 3.10 o superior.
- Tkinter (incluido normalmente con Python; en algunas distribuciones Linux se instala por separado).
- Dependencia: `python-chess`.

## Instalación

```bash
git clone https://github.com/apolloscript3587/Chess-Python.git
cd Chess-Python
python -m venv .venv
```

Activar el entorno virtual:

**Windows (PowerShell):** `.venv\\Scripts\\Activate.ps1`

**Linux / macOS:** `source .venv/bin/activate`

Instalar dependencia:

```bash
python -m pip install -r requirements.txt
```

En Debian/Ubuntu, si Tkinter no está disponible: `sudo apt install python3-tk`.

## Ejecución

```bash
python main.py
```

## Manual de usuario

1. Haz clic sobre una pieza del color cuyo turno está activo. Las casillas legales se resaltan.
2. Haz clic en una casilla resaltada para completar el movimiento.
3. Consulta el turno y el historial en el panel lateral.
4. Usa **Nueva partida**, **Deshacer movimiento**, **Girar tablero** y **Cambiar tema** según lo necesites.
5. Cuando un peón llega a la última fila, elige la pieza en la ventana de promoción.

## Estructura

```text
Chess-Python/
├── main.py
├── ajedrez/
│   ├── modelos/partida.py
│   └── interfaz/
│       ├── tema.py
│       └── ventana.py
├── tests/test_partida.py
├── docs/
│   ├── INFORME_TECNICO.md
│   └── DIAGRAMA_CLASES.md
├── requirements.txt
└── .gitignore
```

## Pruebas

```bash
python -m unittest discover -s tests -v
```

Las pruebas verifican movimientos legales e ilegales, alternancia de turnos, deshacer, jaque mate, reinicio y abstracción y polimorfismo de los temas.

## Tecnologías

- **Python:** lenguaje principal.
- **Tkinter:** interfaz gráfica y eventos.
- **python-chess:** reglas, movimientos legales y notación algebraica.
- **unittest:** pruebas automatizadas.

## Alcance y limitaciones

- Modalidad local para dos personas; no incluye multijugador por Internet ni IA.
- No incorpora reloj, guardado de partidas, perfiles ni base de datos.
- No ofrece controles para acordar tablas o reclamar manualmente tablas por triple repetición o regla de 50 movimientos.
- La dependencia se instala antes del primer uso. Una vez instalada, el juego funciona sin Internet.

## Autor

Proyecto académico de Programación Orientada a Objetos con Python.
