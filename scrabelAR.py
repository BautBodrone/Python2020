# AUTORES:
# Bautista Jose Bodrone
# Javier Franco Jose Camacho Encinas
#
# GPL-3.0-or-later
import PySimpleGUI as sg
import config as gui_configuracion
import puntajes_GUI as puntajes
import tableroDeJuego as juego

'''Menú principal e inicio del programa. Desde acá se llama a todos los demás módulos'''

sg.theme("DarkTeal")
layout = [
    [
        sg.Text("ScrabblerAR", font=("arial", "95", "bold"), justification="center", key="titulo")
    ],
    [
        sg.Image(filename="caratula.png", size=(800, 350))
    ],
    [
        sg.Button("JUGAR", font=("arial", "15", "bold"), size=(15, 1), key="jugar"),

        sg.Button("CONFIGURACION", font=("arial", "15", "bold"), size=(15, 1), key="config"),

        sg.Button("PUNTAJES", font=("arial", "15", "bold"), size=(15, 1), key="puntaje"),

        sg.Button("SALIR", font=("arial", "15", "bold"), size=(15, 1), key="salir")
    ]
]

window = sg.Window(
    "ScrabblerAR",
    resizable=False,
    size=(800, 600)
).Layout(layout)

while True:
    event, values = window.Read()

    if event is None or event == 'salir':
        break

    elif event == "config":
        window.Disappear()
        gui_configuracion.abrir_configuracion()
        window.Reappear()

    elif event == "jugar":
        window.Disappear()
        juego.ventana_juego()
        window.Reappear()

    else:
        window.Disappear()
        puntajes.puntajes_GUI()
        window.Reappear()
