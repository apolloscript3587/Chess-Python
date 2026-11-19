"""Pruebas unitarias del modelo de partida."""

import unittest
import chess

from ajedrez.modelos import Partida


class TestPartida(unittest.TestCase):
    def setUp(self) -> None:
        self.partida = Partida()

    def test_tablero_inicial_tiene_veinte_movimientos_legales(self) -> None:
        self.assertEqual(len(self.partida.movimientos_legales_desde(chess.E2)), 2)
        self.assertEqual(len(list(chess.Board().legal_moves)), 20)

    def test_rechaza_movimiento_ilegal(self) -> None:
        exito, _ = self.partida.mover(chess.E2, chess.E5)
        self.assertFalse(exito)
        self.assertEqual(self.partida.turno, "Blancas")
        self.assertEqual(self.partida.historial, [])

    def test_mover_y_deshacer(self) -> None:
        exito, _ = self.partida.mover(chess.E2, chess.E4)
        self.assertTrue(exito)
        self.assertEqual(self.partida.turno, "Negras")
        self.assertTrue(self.partida.deshacer())
        self.assertEqual(self.partida.turno, "Blancas")
        self.assertEqual(self.partida.historial, [])

    def test_detecta_jaque_mate(self) -> None:
        secuencia = [
            (chess.F2, chess.F3), (chess.E7, chess.E5),
            (chess.G2, chess.G4), (chess.D8, chess.H4),
        ]
        for origen, destino in secuencia:
            exito, mensaje = self.partida.mover(origen, destino)
            self.assertTrue(exito, mensaje)
        self.assertTrue(self.partida.terminada)
        self.assertEqual(self.partida.resultado, "0-1")
        self.assertIn("Jaque mate", self.partida.mensaje_estado())

    def test_nueva_partida_limpia_el_historial(self) -> None:
        self.partida.mover(chess.E2, chess.E4)
        self.partida.nueva_partida()
        self.assertEqual(self.partida.historial, [])
        self.assertEqual(self.partida.turno, "Blancas")
        self.assertEqual(len(list(chess.Board().legal_moves)), 20)


if __name__ == "__main__":
    unittest.main()
