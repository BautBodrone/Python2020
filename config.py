import PySimpleGUI as sg


def abrir_configuracion():
    """Función principal, abre y ejecuta todas las funciones para la GUI de la ventana de configuración."""

    def columna_izquierda(opciones):
        """Genera la columna izquierda. Recibe una lista de opciones, a las que da formato como botón."""
        lista = []
        for opcion in opciones:
            lista.append([sg.Button(opcion.capitalize().replace("_", " "), size=(22, 1), key=opcion)])

        columna_izquierda = lista + [[
            sg.Button("Guardar", size=(10, 1), key="Guardar", bind_return_key=True),
            sg.Button("Salir", size=(10, 1), key="Salir", )
        ]]

        return columna_izquierda

    def columna_derecha(opcion):
        """Genera la columna derecha según la opción actual"""

        def dificultad_y_valor_de_fichas():

            dificultad_layout = [
                [
                    sg.Radio("Facil", "dificultad", key="dificultad_facil"),
                ],
                [
                    sg.Radio("Medio", "dificultad", default=True, key="dificultad_medio")
                ],
                [
                    sg.Radio("Dificil", "dificultad", key="dificultad_dificil")
                ],
            ]

            tiempo_layout = [
                [sg.Slider(
                    default_value=20,
                    range=(2, 60), orientation="h",
                    size=(10, 20),
                    key="cant_minutos"
                )]
            ]

            columna_dif_tiempo = [
                [
                    sg.Frame("Dificultad", dificultad_layout)
                ],
                [
                    sg.Frame("Tiempo", tiempo_layout)
                ]
            ]

            valor_fichas_layout = [[sg.Text("A, E, O, S, I, U, N, L, R, T"),
                                    sg.Slider(
                                        default_value=1,
                                        range=(1, 50), orientation="h",
                                        size=(10, 20),
                                        key="valor_fichas1"
                                    )],
                                   [sg.Text("C, D, G                           "),
                                    sg.Slider(
                                        default_value=2,
                                        range=(2, 50), orientation="h",
                                        size=(10, 20),
                                        key="valor_ficha2"
                                    )],
                                   [sg.Text("M, B, P                           "),
                                    sg.Slider(
                                        default_value=3,
                                        range=(2, 50), orientation="h",
                                        size=(10, 20),
                                        key="valor_ficha3"
                                    )],
                                   [sg.Text("F, H, V, Y                       "),
                                    sg.Slider(
                                        default_value=4,
                                        range=(2, 50), orientation="h",
                                        size=(10, 20),
                                        key="valor_ficha4"
                                    )],
                                   [sg.Text("J                                     "),
                                    sg.Slider(
                                        default_value=6,
                                        range=(2, 50), orientation="h",
                                        size=(10, 20),
                                        key="valor_ficha5"
                                    )],
                                   [sg.Text("K, LL, Ñ, Q, RR, W, X      "),
                                    sg.Slider(
                                        default_value=8,
                                        range=(2, 50), orientation="h",
                                        size=(10, 20),
                                        key="valor_ficha6"
                                    )],
                                   [sg.Text("Z                                    "),
                                    sg.Slider(
                                        default_value=10,
                                        range=(2, 50), orientation="h",
                                        size=(10, 20),
                                        key="valor_ficha7"
                                    )]
                                   ]

            columna_valor_fichas = [[sg.Frame("Cambiar valor", valor_fichas_layout)]]

            layout_dif_valor = [[sg.Column(columna_dif_tiempo), sg.Column(columna_valor_fichas)]]

            return layout_dif_valor

        def cantidad_de_fichas():  # se puede implementar por codigo con un sumador de char+1
            cantidad_de_fichas_layout = [[sg.Text("A: "),
                                          sg.Slider(default_value=11, range=(0, 100), orientation="h",
                                                    size=(10, 20), key="a"),
                                          sg.Text("B: "),
                                          sg.Slider(default_value=11, range=(0, 100), orientation="h",
                                                    size=(10, 20), key="b"),
                                          sg.Text("C: "),
                                          sg.Slider(default_value=11, range=(0, 100), orientation="h",
                                                    size=(10, 20), key="c")],
                                         [sg.Text("D: "),
                                          sg.Slider(default_value=11, range=(0, 100), orientation="h",
                                                    size=(10, 20), key="d"),
                                          sg.Text("E: "),
                                          sg.Slider(default_value=11, range=(0, 100), orientation="h",
                                                    size=(10, 20), key="e"),
                                          sg.Text("F: "),
                                          sg.Slider(default_value=11, range=(0, 100), orientation="h",
                                                    size=(10, 20), key="f")],
                                         [sg.Text("G: "),
                                          sg.Slider(default_value=11, range=(0, 100), orientation="h",
                                                    size=(10, 20), key="g"),
                                          sg.Text("H: "),
                                          sg.Slider(default_value=11, range=(0, 100), orientation="h",
                                                    size=(10, 20), key="h"),
                                          sg.Text("I: "),
                                          sg.Slider(default_value=11, range=(0, 100), orientation="h",
                                                    size=(10, 20), key="i")],
                                         [sg.Text("J: "),
                                          sg.Slider(default_value=11, range=(0, 100), orientation="h",
                                                    size=(10, 20), key="j"),
                                          sg.Text("K: "),
                                          sg.Slider(default_value=11, range=(0, 100), orientation="h",
                                                    size=(10, 20), key="k"),
                                          sg.Text("L: "),
                                          sg.Slider(default_value=11, range=(0, 100), orientation="h",
                                                    size=(10, 20), key="l")],
                                         [sg.Text("M: "),
                                          sg.Slider(default_value=11, range=(0, 100), orientation="h",
                                                    size=(10, 20), key="m"),
                                          sg.Text("N: "),
                                          sg.Slider(default_value=11, range=(0, 100), orientation="h",
                                                    size=(10, 20), key="n"),
                                          sg.Text("Ñ: "),
                                          sg.Slider(default_value=11, range=(0, 100), orientation="h",
                                                    size=(10, 20), key="ñ")],
                                         [sg.Text("O: "),
                                          sg.Slider(default_value=11, range=(0, 100), orientation="h",
                                                    size=(10, 20), key="o"),
                                          sg.Text("P: "),
                                          sg.Slider(default_value=11, range=(0, 100), orientation="h",
                                                    size=(10, 20), key="p"),
                                          sg.Text("Q: "),
                                          sg.Slider(default_value=11, range=(0, 100), orientation="h",
                                                    size=(10, 20), key="q")],
                                         [sg.Text("R: "),
                                          sg.Slider(default_value=11, range=(0, 100), orientation="h",
                                                    size=(10, 20), key="r"),
                                          sg.Text("S: "),
                                          sg.Slider(default_value=11, range=(0, 100), orientation="h",
                                                    size=(10, 20), key="s"),
                                          sg.Text("T: "),
                                          sg.Slider(default_value=11, range=(0, 100), orientation="h",
                                                    size=(10, 20), key="t")],
                                         [sg.Text("U: "),
                                          sg.Slider(default_value=11, range=(0, 100), orientation="h",
                                                    size=(10, 20), key="u"),
                                          sg.Text("V: "),
                                          sg.Slider(default_value=11, range=(0, 100), orientation="h",
                                                    size=(10, 20), key="v"),
                                          sg.Text("X: "),
                                          sg.Slider(default_value=11, range=(0, 100), orientation="h",
                                                    size=(10, 20), key="x")],
                                         [sg.Text("Y: "),
                                          sg.Slider(default_value=11, range=(0, 100), orientation="h",
                                                    size=(10, 20), key="y"),
                                          sg.Text("Z: "),
                                          sg.Slider(default_value=11, range=(0, 100), orientation="h",
                                                    size=(10, 20), key="z")]
                                         ]

            return [[sg.Frame("Cantidad de Ficha por Letra", cantidad_de_fichas_layout)]]

        # COLUMNA DERECHA
        retorno = []
        if opcion == "dificultad_y_valor_de_fichas":  # buscar case
            return dificultad_y_valor_de_fichas()
        elif opcion == "cantidad_de_fichas":
            return cantidad_de_fichas()

    def layout_principal(lista_de_opciones, opcion_actual):
        """Genera la Interfaz Gráfica de Configuracion"""
        layout = [
            [  # Título
                sg.Text("ScrabbleAR"),
            ],
            [
                sg.T(''),
            ],
            [
                sg.Column(columna_izquierda(lista_de_opciones)),
                sg.Column(columna_derecha(opcion_actual))
            ]
        ]

        return layout

    lista_de_opciones = [
        "dificultad_y_valor_de_fichas",
        "cantidad_de_fichas",
    ]

    opcion_actual = lista_de_opciones[0]

    while True:
        window = sg.Window("Configuracion").Layout(layout_principal(lista_de_opciones, opcion_actual))
        event, values = window.Read()

        # Salir de la configuración
        if event is None or event == "Salir":
            window.Close()
            break

        # Seleccionar opción
        elif event in lista_de_opciones:
            opcion_actual = event

        window.Close()


if __name__ == "__main__":
    abrir_configuracion()
