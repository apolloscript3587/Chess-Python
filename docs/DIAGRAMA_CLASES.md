# Diagrama de clases

```mermaid
classDiagram
    class Partida {
        -Board __tablero
        -list __historial_san
        -Move __ultimo_movimiento
        +turno str
        +jaque bool
        +terminada bool
        +pieza_en(casilla)
        +movimientos_legales_desde(origen)
        +mover(origen, destino, promocion)
        +deshacer() bool
        +nueva_partida()
        +historial_formateado() list
        +mensaje_estado() str
    }

    class TemaTablero {
        <<abstract>>
        +colores_casillas()* tuple
        +color_seleccion()* str
        +color_ultimo_movimiento()* str
        +color_rey_en_jaque()* str
    }

    class TemaClasico {
        +colores_casillas() tuple
        +color_seleccion() str
        +color_ultimo_movimiento() str
        +color_rey_en_jaque() str
    }

    class TemaOscuro {
        +colores_casillas() tuple
        +color_seleccion() str
        +color_ultimo_movimiento() str
        +color_rey_en_jaque() str
    }

    class VentanaAjedrez {
        -Partida partida
        -TemaTablero tema
        -Square casilla_seleccionada
        -set destinos_legales
        +_al_hacer_clic(evento)
        +_dibujar_tablero()
        +_actualizar_panel()
        +_nueva_partida()
        +_deshacer()
        +_girar_tablero()
        +_cambiar_tema()
    }

    TemaTablero <|-- TemaClasico
    TemaTablero <|-- TemaOscuro
    VentanaAjedrez *-- Partida
    VentanaAjedrez *-- TemaTablero
```

`TemaTablero` define el contrato visual. `TemaClasico` y `TemaOscuro` lo implementan, y `VentanaAjedrez` trabaja contra la abstracción. La ventana contiene una partida y el tema que se encuentra activo.
