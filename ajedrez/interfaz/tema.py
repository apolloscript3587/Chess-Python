"""Temas del tablero: ejemplo de abstracción, herencia y polimorfismo."""

from abc import ABC, abstractmethod


class TemaTablero(ABC):
    """Contrato para cualquier esquema visual del tablero."""

    @abstractmethod
    def colores_casillas(self) -> tuple[str, str]:
        """Retorna (color_claro, color_oscuro)."""
        raise NotImplementedError

    @abstractmethod
    def color_seleccion(self) -> str:
        """Color del borde de la casilla seleccionada."""
        raise NotImplementedError

    @abstractmethod
    def color_ultimo_movimiento(self) -> str:
        """Color de las casillas del último movimiento."""
        raise NotImplementedError

    @abstractmethod
    def color_rey_en_jaque(self) -> str:
        """Color de alerta para el rey en jaque."""
        raise NotImplementedError


class TemaClasico(TemaTablero):
    """Paleta clara de estilo clásico."""

    def colores_casillas(self) -> tuple[str, str]:
        return "#F0D9B5", "#B58863"

    def color_seleccion(self) -> str:
        return "#E8C547"

    def color_ultimo_movimiento(self) -> str:
        return "#C5D98B"

    def color_rey_en_jaque(self) -> str:
        return "#E57373"


class TemaOscuro(TemaTablero):
    """Paleta oscura de alto contraste."""

    def colores_casillas(self) -> tuple[str, str]:
        return "#D6D8DC", "#526579"

    def color_seleccion(self) -> str:
        return "#F4D35E"

    def color_ultimo_movimiento(self) -> str:
        return "#789B72"

    def color_rey_en_jaque(self) -> str:
        return "#C94C4C"
