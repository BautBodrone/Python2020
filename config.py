import PySimpleGUI as sg
from Configuracion import config_dictionary as Configuracion


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

    def botones_por_defecto():
        return [
            sg.Button("Confirmar", key="boton_confirmar"),
            sg.Button("Por defecto", key="boton_por_defecto"),
            sg.Button("Cancelar", button_color=("white", "red"), key="boton_cancelar")
        ]

    def PopUp_confirmar(titulo, string):
        """Mensaje que permite al usuario confirmar una acción o cancelarla.
        El mensaje y título del Popup es personalizable"""
        layout = [
            [
                sg.T(string)
            ],
            [
                sg.Button('Confirmar', key='boton_confirmar'),
                sg.Button('Cancelar', key='boton_cancelar'),
            ]
        ]

        window = sg.Window(titulo).Layout(layout)
        confirmar = window.Read()
        window.Close()
        return confirmar

    def columna_derecha(opcion, configuracion):
        """Genera la columna derecha según la opción actual"""

        def dificultad_y_valor_de_fichas(configuracion):

            def_facil=False
            def_medio=False
            def_dificil=False

            if configuracion.dificultad == "facil":
                def_facil=True
            elif configuracion.dificultad == "medio":
                def_medio=True
            else:
                def_dificil=True

            dificultad_layout = [
                [
                    sg.Radio("Facil", "dificultad",default=def_facil, key="dificultad_facil",
                             tooltip="Se puede colocar cualquier tipo de palabra"),
                ],
                [
                    sg.Radio("Medio", "dificultad", default=def_medio, key="dificultad_medio",
                             tooltip="Solo se pueden colocar verbos y sustantivos")
                ],
                [
                    sg.Radio("Dificil        ", "dificultad", default=def_dificil, key="dificultad_dificil",
                             tooltip="Solo se pueden colocar palabras de una categoria elegida al azar")
                ],
            ]

            tiempo_layout = [
                [sg.Slider(
                    default_value=configuracion.tiempo,
                    range=(2, 60), orientation="h",
                    size=(10, 20),
                    key="cant_minutos"
                )]
            ]

            blanco= " "
            columna_dif_tiempo = [
                [
                    sg.Frame("Dificultad", dificultad_layout)
                ],
                [
                    sg.Frame("Tiempo", tiempo_layout)
                ]
            ]

            valor_fichas_layout = [[sg.Text("A, E, O, S, I, U, N, L, R, T", key="valor_text1"),
                                    sg.Slider(
                                        default_value=configuracion.valor_fichas["A, E, O, S, I, U, N, L, R, T"],
                                        range=(1, 50), orientation="h",
                                        size=(10, 20),
                                        key="valor_ficha1"
                                    )],
                                   [sg.Text("C, D, G", key="valor_text2"), sg.Text(blanco*24),
                                    sg.Slider(
                                        default_value=configuracion.valor_fichas["C, D, G"],
                                        range=(2, 50), orientation="h",
                                        size=(10, 20),
                                        key="valor_ficha2"
                                    )],
                                   [sg.Text("M, B, P", key="valor_text3"), sg.Text(blanco*24),
                                    sg.Slider(
                                        default_value=configuracion.valor_fichas["M, B, P"],
                                        range=(2, 50), orientation="h",
                                        size=(10, 20),
                                        key="valor_ficha3"
                                    )],
                                   [sg.Text("F, H, V, Y", key="valor_text4"), sg.Text(blanco*20),
                                    sg.Slider(
                                        default_value=configuracion.valor_fichas["F, H, V, Y"],
                                        range=(2, 50), orientation="h",
                                        size=(10, 20),
                                        key="valor_ficha4"
                                    )],
                                   [sg.Text("J", key="valor_text5"), sg.Text(blanco*34),
                                    sg.Slider(
                                        default_value=configuracion.valor_fichas["J"],
                                        range=(2, 50), orientation="h",
                                        size=(10, 20),
                                        key="valor_ficha5"
                                    )],
                                   [sg.Text("K, LL, Ñ, Q, RR, W, X", key="valor_text6"), sg.Text(blanco*3),
                                    sg.Slider(
                                        default_value=configuracion.valor_fichas["K, LL, Ñ, Q, RR, W, X"],
                                        range=(2, 50), orientation="h",
                                        size=(10, 20),
                                        key="valor_ficha6"
                                    )],
                                   [sg.Text("Z", key="valor_text7"), sg.Text(blanco*33),
                                    sg.Slider(
                                        default_value=configuracion.valor_fichas["Z"],
                                        range=(2, 50), orientation="h",
                                        size=(10, 20),
                                        key="valor_ficha7"
                                    )]
                                   ]

            columna_valor_fichas = [[sg.Frame("Cambiar valor", valor_fichas_layout)]]

            layout_dif_valor = [[sg.Column(columna_dif_tiempo), sg.Column(columna_valor_fichas)],botones_por_defecto()]

            return layout_dif_valor

        def slider_cant_fichas(configuracion):
            """crea lineas que contiene 3 sliders cada una y lo agraga a una lista que retorna para ser mostrada"""
            lista_sliders = []
            x = ord("A")
            while x < ord("Z"):
                if chr(x + 2) != "[": slider = [
                    sg.Text(chr(x) + ": "), sg.Slider(default_value=configuracion.cantidad_fichas[chr(x)],
                                                      range=(0, 100), orientation="h",size=(10, 20), key=chr(x)
                                                      ),
                    sg.Text(chr(x + 1) + ": "), sg.Slider(default_value=configuracion.cantidad_fichas[chr(x+1)],
                                                          range=(0, 100), orientation="h", size=(10, 20), key=chr(x + 1)
                                                          ),
                    sg.Text(chr(x + 2) + ": "), sg.Slider(default_value=configuracion.cantidad_fichas[chr(x+2)],
                                                          range=(0, 100), orientation="h", size=(10, 20), key=chr(x + 2)
                                                          )
                    ]
                else:slider = [
                    sg.Text(chr(x) + ": "), sg.Slider(default_value= configuracion.cantidad_fichas[chr(x)],
                                                      range=(0, 100), orientation="h", size=(10, 20), key=chr(x)
                                                      ),
                    sg.Text(chr(x + 1) + ": "), sg.Slider(default_value= configuracion.cantidad_fichas[chr(x+1)],
                                                          range=(0, 100), orientation="h",size=(10, 20), key=chr(x + 1)
                                                          )
                ]

                x += 3
                lista_sliders.append(slider)
            return lista_sliders

        def cantidad_de_fichas(configuracion):  # se puede implementar por codigo con un sumador de char+1
            cantidad_de_fichas_layout = slider_cant_fichas(configuracion)
            return [[sg.Frame("Cantidad de Ficha por Letra", cantidad_de_fichas_layout)],botones_por_defecto()]

        # COLUMNA DERECHA
        retorno = []
        if opcion == "dificultad_y_valor_de_fichas":  # buscar case
            return dificultad_y_valor_de_fichas(configuracion)
        elif opcion == "cantidad_de_fichas":
            return cantidad_de_fichas(configuracion)

    def retorno_cantidad_fichas(value):
        retorno = {}
        for x in range(ord("A"), ord("Z")+1):
            retorno[chr(x)] = value[chr(x)]
        return retorno

    def retorno_valor_fichas(values):
        """devuelve un dicionario de los valores
            hecho de esta manera porque PysimpleGui text no funciona el get"""
        retorno = {}
        retorno["A, E, O, S, I, U, N, L, R, T"] = values["valor_ficha1"]
        retorno["C, D, G"] = values["valor_ficha2"]
        retorno["M, B, P"] = values["valor_ficha3"]
        retorno["F, H, V, Y"] = values["valor_ficha4"]
        retorno["J"] = values["valor_ficha5"]
        retorno["K, LL, Ñ, Q, RR, W, X"] = values["valor_ficha6"]
        retorno["Z"] = values["valor_ficha7"]
        return retorno

    def layout_principal(lista_de_opciones, opcion_actual, configuracion):
        """Genera la Interfaz Gráfica de Configuracion"""
        layout = [
            [  # Título
                sg.Text("ScrabbleAR"),
            ],
            [sg.Text('_' * 88)],
            [
                sg.Column(columna_izquierda(lista_de_opciones)),
                sg.VSeperator(),
                sg.Column(columna_derecha(opcion_actual, configuracion))
            ]
        ]

        return layout

    def PopUp_guardar_y_salir(configuracion):
        '''Mensaje que consulta al usuario si desea salir sin guardar o guardar antes de salir.
        Retorna si se guardaron o no los cambios'''
        layout = [
            [
                sg.T('Hay cambios que no ha guardado, ¿Desea guardar los cambios antes de salir?')
            ],
            [
                sg.Button('Guardar y salir', key='boton_confirmar'),
                sg.Button('Salir', key='boton_cancelar'),
            ]
        ]

        window = sg.Window('Cambios sin guardar').Layout(layout)
        event, values = window.Read()
        window.Close()

        guardado = False

        if event == 'boton_confirmar':
            guardado = Configuracion.guardar_configuracion(user_config)
            if guardado:
                sg.PopupOK('Los cambios se han guardado con éxito.')
            else:
                sg.PopupOK(
                    'Un error ocurrió mientras intentábamos guardar la configuración. No se guardaron los cambios')

        return guardado

    lista_de_opciones = [
        "dificultad_y_valor_de_fichas",
        "cantidad_de_fichas",
    ]

    opcion_actual = lista_de_opciones[0]

    user_config = Configuracion.obtener_config()
    default_config = Configuracion.Configuracion()

    guardado = True

    while True:
        window = sg.Window("Configuracion").Layout(layout_principal(lista_de_opciones, opcion_actual, user_config))

        event, values = window.Read()

        # Salir de la configuración
        if event is None or event == "Salir":
            if not guardado:
                PopUp_guardar_y_salir(user_config)
            window.Close()
            break

        # Seleccionar opción
        elif event in lista_de_opciones:
            opcion_actual = event

        if event == 'boton_por_defecto':

            if PopUp_confirmar("Valores por defecto", "Continuar restablecerá todas las opciones de " +
                               opcion_actual.capitalize().replace("_", " ") + " a sus valores por defecto."
                                                                              "\n¿Seguro que desea continuar?"):

                if opcion_actual == "dificultad_y_valor_de_fichas":
                    user_config.tiempo = default_config.get_tiempo()
                    user_config.dificultad = default_config.get_dificultad()
                    user_config.valor_fichas = default_config.get_valor_fichas()

                if opcion_actual == "cantidad_de_fichas":
                    user_config.cantidad_fichas = default_config.get_cantidad_fichas()

                sg.PopupOK('Valores por defecto reestablecidos.')

        if event == 'boton_confirmar':
            guardado = False

            if opcion_actual == "cantidad_de_fichas":
                user_config.cantidad_fichas = retorno_cantidad_fichas(values)

            if opcion_actual == "dificultad_y_valor_de_fichas":
                user_config.valor_fichas = retorno_valor_fichas(values)
                if values["dificultad_facil"]:
                    user_config.dificultad = "facil"
                elif values["dificultad_medio"]:
                    user_config.dificultad = "medio"
                else:
                    user_config.dificultad = "dificil"
                user_config.tiempo = values ["cant_minutos"]

        if event == 'Guardar':
            guardado = Configuracion.guardar_configuracion(user_config)

            if guardado:
                sg.PopupOK('Los cambios se han guardado con éxito.')
            else:
                sg.PopupOK('Un error ocurrió mientras intentábamos guardar la configuración. No se guardaron los cambios')

        window.Close()


if __name__ == "__main__":
    abrir_configuracion()
