import PySimpleGUI as sg
import config as gui_configuracion
import tableroDeJuego as juego
import puntajes_GUI as puntajes

'''Menú principal e inicio del programa. Desde acá se llama a todos los demás módulos'''


def abrirMain():
    layout = [
        [
            sg.Text("ScrabblerAR", font=('arial', '95', 'bold'), justification="center", key="titulo")
        ],
        [
            sg.Button("JUGAR", font=('arial', '15', 'bold'), size=(15, 1), key="jugar"),

            sg.Button("CONFIGURACION", font=('arial', '15', 'bold'), size=(15, 1), key="config"),

            sg.Button("PUNTAJES", font=('arial', '15', 'bold'), size=(15, 1), key="puntaje"),

            sg.Button("SALIR", font=('arial', '15', 'bold'), size=(15, 1), key="salir")
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
            try:
                juego.ventana_juego()
            except:
                print("sale")
            window.Reappear()

        else:
            window.Disappear()
            try:
                puntajes.puntajes_GUI()
            except:
                print("sale")
            window.Reappear()


if __name__ == '__main__':
    abrirMain()