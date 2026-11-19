"""Pruebas del contrato abstracto y el polimorfismo de los temas."""

import unittest

from ajedrez.interfaz.tema import TemaClasico, TemaOscuro, TemaTablero


class TestTemas(unittest.TestCase):
    def test_tema_base_es_abstracto(self) -> None:
        with self.assertRaises(TypeError):
            TemaTablero()

    def test_temas_implementan_el_contrato(self) -> None:
        self.assertIsInstance(TemaClasico(), TemaTablero)
        self.assertIsInstance(TemaOscuro(), TemaTablero)

    def test_polimorfismo_de_paletas(self) -> None:
        temas: list[TemaTablero] = [TemaClasico(), TemaOscuro()]
        paletas = [tema.colores_casillas() for tema in temas]
        self.assertNotEqual(paletas[0], paletas[1])
        self.assertEqual(len(paletas[0]), 2)
        self.assertEqual(len(paletas[1]), 2)


if __name__ == "__main__":
    unittest.main()
