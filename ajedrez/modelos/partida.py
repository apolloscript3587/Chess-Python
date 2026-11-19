"""Modelo de una partida de ajedrez.

La biblioteca python-chess valida las reglas oficiales. Esta clase encapsula
el tablero y ofrece una API sencilla para que la interfaz no manipule sus
estructuras internas.
"""

from __future__ import annotations

import chess


class Partida:
    """Administra el estado, los movimientos y el historial de una partida."""

    def __init__(self) -> None:
        self.__tablero = chess.Board()
        self.__historial_san: list[str] = []
        self.__ultimo_movimiento: chess.Move | None = None

    @property
    def turno(self) -> str:
        """Devuelve el color que debe mover."""
        return "Blancas" if self.__tablero.turn == chess.WHITE else "Negras"

    @property
    def color_en_turno(self) -> chess.Color:
        """Devuelve la constante de color de python-chess."""
        return self.__tablero.turn

    @property
    def ultimo_movimiento(self) -> chess.Move | None:
        return self.__ultimo_movimiento

    @property
    def jaque(self) -> bool:
        return self.__tablero.is_check()

    @property
    def rey_en_jaque(self) -> chess.Square | None:
        """Casilla del rey en jaque, si existe."""
        return self.__tablero.king(self.__tablero.turn) if self.jaque else None

    @property
    def terminada(self) -> bool:
        return self.__tablero.is_game_over()

    @property
    def resultado(self) -> str:
        """Devuelve el resultado en notación estándar o una cadena vacía."""
        if not self.terminada:
            return ""
        return self.__tablero.result()

    @property
    def historial(self) -> list[str]:
        """Devuelve una copia del historial en notación algebraica (SAN)."""
        return self.__historial_san.copy()

    def pieza_en(self, casilla: chess.Square) -> chess.Piece | None:
        """Consulta una casilla sin exponer el tablero interno."""
        return self.__tablero.piece_at(casilla)

    def movimientos_legales_desde(self, origen: chess.Square) -> set[chess.Square]:
        """Obtiene los destinos legales de la pieza situada en origen."""
        if self.terminada:
            return set()
        pieza = self.__tablero.piece_at(origen)
        if pieza is None or pieza.color != self.__tablero.turn:
            return set()
        return {
            movimiento.to_square
            for movimiento in self.__tablero.legal_moves
            if movimiento.from_square == origen
        }

    def mover(
        self,
        origen: chess.Square,
        destino: chess.Square,
        promocion: chess.PieceType = chess.QUEEN,
    ) -> tuple[bool, str]:
        """Intenta realizar un movimiento y devuelve (éxito, mensaje)."""
        if self.terminada:
            return False, "La partida ya terminó. Inicia una nueva para continuar."

        pieza = self.__tablero.piece_at(origen)
        if pieza is None:
            return False, "Selecciona una casilla que contenga una pieza."
        if pieza.color != self.__tablero.turn:
            return False, "Espera tu turno para mover esa pieza."

        es_promocion = (
            pieza.piece_type == chess.PAWN
            and chess.square_rank(destino) in (0, 7)
        )
        movimiento = chess.Move(
            origen,
            destino,
            promotion=promocion if es_promocion else None,
        )

        if movimiento not in self.__tablero.legal_moves:
            return False, "Movimiento no válido. Revisa las reglas de la pieza."

        notacion = self.__tablero.san(movimiento)
        self.__tablero.push(movimiento)
        self.__historial_san.append(notacion)
        self.__ultimo_movimiento = movimiento
        return True, "Movimiento realizado."

    def deshacer(self) -> bool:
        """Deshace el último movimiento."""
        if not self.__historial_san:
            return False
        self.__tablero.pop()
        self.__historial_san.pop()
        self.__ultimo_movimiento = (
            self.__tablero.peek() if self.__tablero.move_stack else None
        )
        return True

    def nueva_partida(self) -> None:
        """Reinicia el tablero y el historial."""
        self.__tablero.reset()
        self.__historial_san.clear()
        self.__ultimo_movimiento = None

    def historial_formateado(self) -> list[str]:
        """Agrupa las jugadas blancas y negras para mostrarlas en la interfaz."""
        lineas: list[str] = []
        for indice in range(0, len(self.__historial_san), 2):
            numero = indice // 2 + 1
            blanca = self.__historial_san[indice]
            negra = self.__historial_san[indice + 1] if indice + 1 < len(self.__historial_san) else ""
            lineas.append(f"{numero:>2}. {blanca:<8} {negra}")
        return lineas

    def mensaje_estado(self) -> str:
        """Construye el mensaje visible de estado de la partida."""
        if self.__tablero.is_checkmate():
            ganador = "Negras" if self.__tablero.turn == chess.WHITE else "Blancas"
            return f"¡Jaque mate! Ganan {ganador}."
        if self.__tablero.is_stalemate():
            return "Tablas por rey ahogado."
        if self.__tablero.is_insufficient_material():
            return "Tablas por material insuficiente."
        if self.__tablero.is_fivefold_repetition():
            return "Tablas por repetición quíntuple."
        if self.__tablero.is_seventyfive_moves():
            return "Tablas por la regla de 75 movimientos."
        if self.jaque:
            return f"¡Jaque! Turno de {self.turno}."
        return f"Turno de {self.turno}."
