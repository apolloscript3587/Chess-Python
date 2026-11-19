"""Ventana principal de Ajedrez Offline, construida con Tkinter."""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox
import sys

import chess

from ajedrez.modelos import Partida
from ajedrez.interfaz.tema import TemaClasico, TemaOscuro, TemaTablero


class VentanaAjedrez(tk.Tk):
    """Interfaz para jugar ajedrez local entre dos personas."""

    TAMANO_CASILLA = 76
    SIMBOLOS = {
        "P": "♙", "N": "♘", "B": "♗", "R": "♖", "Q": "♕", "K": "♔",
        "p": "♟", "n": "♞", "b": "♝", "r": "♜", "q": "♛", "k": "♚",
    }

    def __init__(self) -> None:
        super().__init__()
        self.title("Ajedrez Offline | Python")
        self.resizable(False, False)
        self.configure(bg="#202733")

        self.partida = Partida()
        self.tema: TemaTablero = TemaClasico()
        self.tema_oscuro = False
        self.casilla_seleccionada: chess.Square | None = None
        self.destinos_legales: set[chess.Square] = set()
        self.tablero_invertido = False

        self._crear_interfaz()
        self._dibujar_tablero()
        self._actualizar_panel()

    def _crear_interfaz(self) -> None:
        encabezado = tk.Frame(self, bg="#202733", padx=18, pady=14)
        encabezado.pack(fill="x")
        tk.Label(
            encabezado, text="♔  AJEDREZ OFFLINE", fg="#F4F1DE",
            bg="#202733", font=("Segoe UI", 19, "bold"),
        ).pack(side="left")
        tk.Label(
            encabezado, text="Dos jugadores · Sin conexión", fg="#B8C1CC",
            bg="#202733", font=("Segoe UI", 10),
        ).pack(side="right", padx=4)

        contenido = tk.Frame(self, bg="#202733", padx=18, pady=(0, 18))
        contenido.pack()
        tablero_frame = tk.Frame(contenido, bg="#202733", bd=0)
        tablero_frame.pack(side="left")

        dimension = self.TAMANO_CASILLA * 8
        self.canvas = tk.Canvas(
            tablero_frame, width=dimension, height=dimension,
            highlightthickness=3, highlightbackground="#566273", bd=0,
        )
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self._al_hacer_clic)

        panel = tk.Frame(contenido, bg="#2C3543", width=250, padx=15, pady=14)
        panel.pack(side="left", fill="y", padx=(16, 0))
        panel.pack_propagate(False)

        tk.Label(
            panel, text="ESTADO DE LA PARTIDA", bg="#2C3543", fg="#AEB8C6",
            font=("Segoe UI", 9, "bold"), anchor="w",
        ).pack(fill="x")
        self.etiqueta_estado = tk.Label(
            panel, text="Turno de Blancas.", bg="#2C3543", fg="#FFFFFF",
            font=("Segoe UI", 12, "bold"), wraplength=215, justify="left",
            anchor="w", pady=9,
        )
        self.etiqueta_estado.pack(fill="x")

        tk.Frame(panel, bg="#485365", height=1).pack(fill="x", pady=6)
        tk.Label(
            panel, text="HISTORIAL DE MOVIMIENTOS", bg="#2C3543", fg="#AEB8C6",
            font=("Segoe UI", 9, "bold"), anchor="w",
        ).pack(fill="x", pady=(3, 7))

        historial_frame = tk.Frame(panel, bg="#202733")
        historial_frame.pack(fill="both", expand=True)
        self.lista_movimientos = tk.Listbox(
            historial_frame, bg="#202733", fg="#F4F1DE",
            selectbackground="#526579", selectforeground="#FFFFFF",
            font=("Consolas", 10), relief="flat", activestyle="none",
            highlightthickness=0, height=17,
        )
        self.lista_movimientos.pack(side="left", fill="both", expand=True)
        scroll = tk.Scrollbar(historial_frame, command=self.lista_movimientos.yview)
        scroll.pack(side="right", fill="y")
        self.lista_movimientos.configure(yscrollcommand=scroll.set)

        botones = tk.Frame(panel, bg="#2C3543")
        botones.pack(fill="x", pady=(12, 0))
        self._boton(botones, "＋  Nueva partida", self._nueva_partida).pack(fill="x", pady=3)
        self._boton(botones, "↶  Deshacer movimiento", self._deshacer).pack(fill="x", pady=3)
        self._boton(botones, "⇄  Girar tablero", self._girar_tablero).pack(fill="x", pady=3)
        self._boton(botones, "◐  Cambiar tema", self._cambiar_tema).pack(fill="x", pady=3)

        tk.Label(
            self, text="Haz clic en una pieza y luego en una casilla resaltada para moverla.",
            bg="#202733", fg="#AEB8C6", font=("Segoe UI", 9), pady=0,
        ).pack(pady=(0, 14))

    @staticmethod
    def _boton(parent: tk.Widget, texto: str, comando) -> tk.Button:
        return tk.Button(
            parent, text=texto, command=comando, bg="#46566D", fg="#FFFFFF",
            activebackground="#60748F", activeforeground="#FFFFFF",
            relief="flat", bd=0, cursor="hand2", font=("Segoe UI", 9, "bold"),
            padx=8, pady=8,
        )

    def _casilla_desde_pantalla(self, x: int, y: int) -> chess.Square | None:
        columna = x // self.TAMANO_CASILLA
        fila = y // self.TAMANO_CASILLA
        if not (0 <= columna < 8 and 0 <= fila < 8):
            return None
        if self.tablero_invertido:
            archivo, rango = 7 - columna, fila
        else:
            archivo, rango = columna, 7 - fila
        return chess.square(archivo, rango)

    def _dibujar_tablero(self) -> None:
        self.canvas.delete("all")
        claro, oscuro = self.tema.colores_casillas()
        tamano = self.TAMANO_CASILLA
        ultimo = self.partida.ultimo_movimiento
        rey_jaque = self.partida.rey_en_jaque

        for fila in range(8):
            for columna in range(8):
                if self.tablero_invertido:
                    archivo, rango = 7 - columna, fila
                else:
                    archivo, rango = columna, 7 - fila
                casilla = chess.square(archivo, rango)
                x1, y1 = columna * tamano, fila * tamano
                x2, y2 = x1 + tamano, y1 + tamano
                color = claro if (archivo + rango) % 2 == 0 else oscuro
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=color)

                if ultimo and casilla in (ultimo.from_square, ultimo.to_square):
                    self.canvas.create_rectangle(
                        x1, y1, x2, y2, fill=self.tema.color_ultimo_movimiento(),
                        stipple="gray50", outline="",
                    )
                if casilla == rey_jaque:
                    self.canvas.create_rectangle(
                        x1, y1, x2, y2, fill=self.tema.color_rey_en_jaque(),
                        stipple="gray25", outline="",
                    )
                if casilla == self.casilla_seleccionada:
                    self.canvas.create_rectangle(
                        x1 + 2, y1 + 2, x2 - 2, y2 - 2,
                        outline=self.tema.color_seleccion(), width=4,
                    )

                if casilla in self.destinos_legales:
                    centro_x, centro_y = x1 + tamano / 2, y1 + tamano / 2
                    pieza_destino = self.partida.pieza_en(casilla)
                    if pieza_destino is None:
                        radio = 8
                        self.canvas.create_oval(
                            centro_x-radio, centro_y-radio, centro_x+radio, centro_y+radio,
                            fill="#536D55", outline="",
                        )
                    else:
                        self.canvas.create_oval(
                            x1 + 4, y1 + 4, x2 - 4, y2 - 4,
                            outline="#536D55", width=4,
                        )

                pieza = self.partida.pieza_en(casilla)
                if pieza:
                    simbolo = self.SIMBOLOS[pieza.symbol()]
                    color_texto = "#FFFDF7" if pieza.color == chess.WHITE else "#202733"
                    sombra = "#3B4654" if pieza.color == chess.WHITE else "#F2E8D5"
                    familia = "Segoe UI Symbol" if sys.platform == "win32" else "DejaVu Sans"
                    self.canvas.create_text(
                        x1 + tamano / 2 + 1, y1 + tamano / 2 + 2,
                        text=simbolo, font=(familia, 43), fill=sombra,
                    )
                    self.canvas.create_text(
                        x1 + tamano / 2, y1 + tamano / 2,
                        text=simbolo, font=(familia, 43), fill=color_texto,
                    )

        for indice in range(8):
            archivo = 7 - indice if self.tablero_invertido else indice
            rango = indice + 1 if self.tablero_invertido else 8 - indice
            self.canvas.create_text(
                indice * tamano + 7, 7,
                text=chess.FILE_NAMES[archivo], anchor="nw",
                font=("Segoe UI", 7, "bold"), fill="#5C6673",
            )
            self.canvas.create_text(
                4, indice * tamano + 4,
                text=str(rango), anchor="nw",
                font=("Segoe UI", 7, "bold"), fill="#5C6673",
            )

    def _al_hacer_clic(self, evento: tk.Event) -> None:
        if self.partida.terminada:
            return
        casilla = self._casilla_desde_pantalla(evento.x, evento.y)
        if casilla is None:
            return

        pieza = self.partida.pieza_en(casilla)
        if self.casilla_seleccionada is None:
            self._seleccionar(casilla)
            return

        if casilla == self.casilla_seleccionada:
            self._limpiar_seleccion()
            self._dibujar_tablero()
            return

        if pieza is not None and pieza.color == self.partida.color_en_turno:
            self._seleccionar(casilla)
            return

        promocion = self._dialogo_promocion() if self._es_promocion(casilla) else chess.QUEEN
        origen = self.casilla_seleccionada
        exito, mensaje = self.partida.mover(origen, casilla, promocion)
        self._limpiar_seleccion()
        self._actualizar_panel()
        self._dibujar_tablero()
        if not exito:
            self.etiqueta_estado.configure(text=mensaje)
        elif self.partida.terminada:
            messagebox.showinfo("Partida finalizada", self.partida.mensaje_estado(), parent=self)

    def _seleccionar(self, casilla: chess.Square) -> None:
        pieza = self.partida.pieza_en(casilla)
        if pieza is None or pieza.color != self.partida.color_en_turno:
            return
        self.casilla_seleccionada = casilla
        self.destinos_legales = self.partida.movimientos_legales_desde(casilla)
        self._dibujar_tablero()

    def _limpiar_seleccion(self) -> None:
        self.casilla_seleccionada = None
        self.destinos_legales.clear()

    def _es_promocion(self, destino: chess.Square) -> bool:
        if self.casilla_seleccionada is None:
            return False
        pieza = self.partida.pieza_en(self.casilla_seleccionada)
        return bool(
            pieza and pieza.piece_type == chess.PAWN
            and chess.square_rank(destino) in (0, 7)
        )

    def _dialogo_promocion(self) -> chess.PieceType:
        dialogo = tk.Toplevel(self)
        dialogo.title("Promoción de peón")
        dialogo.configure(bg="#2C3543")
        dialogo.resizable(False, False)
        dialogo.transient(self)
        dialogo.grab_set()
        tk.Label(
            dialogo, text="Elige la pieza para promocionar:",
            bg="#2C3543", fg="white", font=("Segoe UI", 10), padx=14, pady=12,
        ).pack()
        resultado = {"pieza": chess.QUEEN}
        opciones = tk.Frame(dialogo, bg="#2C3543")
        opciones.pack(padx=10, pady=(0, 12))
        for texto, tipo in (("Dama", chess.QUEEN), ("Torre", chess.ROOK),
                            ("Alfil", chess.BISHOP), ("Caballo", chess.KNIGHT)):
            tk.Button(
                opciones, text=texto,
                command=lambda p=tipo: (resultado.update(pieza=p), dialogo.destroy()),
                bg="#46566D", fg="white", relief="flat", padx=8, pady=6,
            ).pack(side="left", padx=3)
        dialogo.protocol(
            "WM_DELETE_WINDOW",
            lambda: (resultado.update(pieza=chess.QUEEN), dialogo.destroy()),
        )
        self.wait_window(dialogo)
        return resultado["pieza"]

    def _actualizar_panel(self) -> None:
        self.etiqueta_estado.configure(text=self.partida.mensaje_estado())
        self.lista_movimientos.delete(0, tk.END)
        for linea in self.partida.historial_formateado():
            self.lista_movimientos.insert(tk.END, linea)
        if self.lista_movimientos.size():
            self.lista_movimientos.see(tk.END)

    def _nueva_partida(self) -> None:
        if self.partida.historial and not messagebox.askyesno(
            "Nueva partida", "¿Deseas abandonar la partida actual e iniciar otra?", parent=self
        ):
            return
        self.partida.nueva_partida()
        self._limpiar_seleccion()
        self._actualizar_panel()
        self._dibujar_tablero()

    def _deshacer(self) -> None:
        if not self.partida.deshacer():
            self.etiqueta_estado.configure(text="No hay movimientos para deshacer.")
            return
        self._limpiar_seleccion()
        self._actualizar_panel()
        self._dibujar_tablero()

    def _girar_tablero(self) -> None:
        self.tablero_invertido = not self.tablero_invertido
        self._dibujar_tablero()

    def _cambiar_tema(self) -> None:
        self.tema_oscuro = not self.tema_oscuro
        self.tema = TemaOscuro() if self.tema_oscuro else TemaClasico()
        self._dibujar_tablero()
