"""Punto de entrada de Ajedrez Offline."""

from ajedrez.interfaz.ventana import VentanaAjedrez


def main() -> None:
    """Inicia la aplicación de escritorio."""
    app = VentanaAjedrez()
    app.mainloop()


if __name__ == "__main__":
    main()
