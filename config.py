# AUTORES:
# Bautista Jose Bodrone
# Javier Franco Jose Camacho Encinas
#
# GPL-3.0-or-later
import PySimpleGUI as sg
from Configuracion import config_dictionary as Configuracion
import config as gui_configuracion


def abrir_configuracion():
    """Función principal, abre y ejecuta todas las funciones para la GUI de la ventana de configuración."""

    def columna_izquierda(opciones):
        """Genera la columna izquierda. Recibe una lista de opciones, a las que da formato como botón."""
        lista = []
        for opcion in opciones:
            if opcion == "dificultad_y_valor_de_fichas":
                lista.append([sg.Button(opcion.capitalize().replace("_", " "), size=(22, 1), key=opcion, disabled=True)])
            else:
                lista.append([sg.Button(opcion.capitalize().replace("_", " "), size=(22, 1), key=opcion)])

        columna_izquierda = lista + [[
            sg.Button("Salir", size=(22, 1), key="Salir", )
        ]]

        return columna_izquierda

    def botones_por_defecto(variante):
        """son solo estos tres botones en una version anteriro tenian otro funcionamiento"""
        return [
            sg.Button("Guardar", key="boton_confirmar"+str(variante)),
            sg.Button("Por defecto", key="boton_por_defecto"+str(variante))
        ]

    def PopUp_confirmar(titulo, string):
        """Mensaje que permite al usuario confirmar una acción o cancelarla.
        El mensaje y título del Popup es personalizable"""
        layout = [
            [
                sg.Text(string)
            ],
            [
                sg.Button('Confirmar', key='boton_confirmar'),
                sg.Button('Cancelar', key='boton_cancelar'),
            ]
        ]

        window = sg.Window(titulo).Layout(layout)
        confirmar = window.Read()
        window.Close()
        if confirmar[0] =="boton_confirmar":
            return True
        else:
            return False

    def dificultad_y_valor_de_fichas(configuracion):
        """crea la layout para la pestaña/columna dificulta y valor de fichas"""

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

        layout_dif_valor = [[sg.Column(columna_dif_tiempo), sg.Column(columna_valor_fichas)], botones_por_defecto(1)]

        return layout_dif_valor

    def cantidad_de_fichas(configuracion):
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
        cantidad_de_fichas_layout= lista_sliders
        return [[sg.Frame("Cantidad de Ficha por Letra", cantidad_de_fichas_layout)], botones_por_defecto(2)]

    def retorno_cantidad_fichas(value):
        """busca el valor de los slider y lo devuelve en forma de diccionario"""
        retorno = {}
        for x in range(ord("A"), ord("Z")+1):
            retorno[chr(x)] = int(value[chr(x)])
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

    def layout_principal(lista_de_opciones, configuracion):
        """Genera la Interfaz Gráfica de Configuracion"""
        layout = [
            [  # Título
                sg.Text("ScrabbleAR",font=("arial", "80", "bold")),
            ],
            [sg.Text('_' * 88)],
            [
                sg.Column(columna_izquierda(lista_de_opciones)),
                sg.VSeperator(),
                sg.Column(cantidad_de_fichas(configuracion),key="columna_cant_fichas", visible=False),
                sg.Column(dificultad_y_valor_de_fichas(configuracion), key="columna_dificultad")
            ]
        ]

        return layout

    def guardar_configuracion(user_config):
        guardado = Configuracion.guardar_configuracion(user_config)

        if guardado:
            sg.PopupOK("Los cambios se han guardado con éxito.")
        else:
            sg.PopupOK("Un error ocurrió mientras intentábamos guardar la configuración."
                       " No se guardaron los cambios")

    lista_de_opciones = [
        "dificultad_y_valor_de_fichas",
        "cantidad_de_fichas",
    ]

    opcion_actual = lista_de_opciones[0]

    user_config = Configuracion.obtener_config()
    default_config = Configuracion.Configuracion()

    window = sg.Window("Configuracion").Layout(layout_principal(lista_de_opciones, user_config))
    while True:

        event, values = window.Read()

        # Salir de la configuración
        if event is None or event == "Salir":
            window.Close()
            break

        # Seleccionar opción
        elif event == "dificultad_y_valor_de_fichas":
            opcion_actual = event
            window.Element(event).Update(disabled=True)
            window.Element("cantidad_de_fichas").Update(disabled=False)
            window.Element("columna_cant_fichas").Update(visible=False)
            window.Element("columna_dificultad").Update(visible=True)

        elif event == "cantidad_de_fichas":
            opcion_actual = event
            window.Element(event).Update(disabled=True)
            window.Element("dificultad_y_valor_de_fichas").Update(disabled=False)
            window.Element("columna_cant_fichas").Update(visible=True)
            window.Element("columna_dificultad").Update(visible=False)

        elif event in ("boton_por_defecto1", "boton_por_defecto2"):
            if PopUp_confirmar("Valores por defecto",
                                                    "Continuar restablecerá todas las opciones de "
                                                    + opcion_actual.capitalize().replace("_", " ")
                                                    + " a sus valores por defecto. ¿Seguro que desea continuar?"):
                if opcion_actual == "dificultad_y_valor_de_fichas":
                    user_config.tiempo = default_config.tiempo
                    user_config.dificultad = default_config.dificultad
                    user_config.valor_fichas = default_config.valor_fichas

                if opcion_actual == "cantidad_de_fichas":
                    user_config.cantidad_fichas = default_config.cantidad_fichas

                sg.PopupOK("Valores por defecto reestablecidos.")
                guardar_configuracion(user_config)
                window.Close()
                gui_configuracion.abrir_configuracion()

        elif event in ("boton_confirmar1", "boton_confirmar2"):

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

            guardar_configuracion(user_config)

            window.Close()
            gui_configuracion.abrir_configuracion()
            break
    return


if __name__ == "__main__":
    abrir_configuracion()
