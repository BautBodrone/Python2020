def puntajes_GUI():
    import PySimpleGUI as sg
    from Puntajes import puntajes as Puntajes

    puntaje = Puntajes.obtener_puntajes()
    facil, medio, dificil = puntaje.por_nivel()
    total = puntaje.por_puntaje()
    print(puntaje.total)

    Puntajes.guardar_puntajes(puntaje)

    columna_total = sg.Column([[sg.Table(total, headings=["nivel", "puntaje", "fecha"], hide_vertical_scroll=True)]],
                              key="col_tot")

    columna_nivel = sg.Column(
        [[sg.Table(facil, headings=["nivel", "puntaje", "fecha"], hide_vertical_scroll=True, key="t1"),
          sg.Table(medio, headings=["nivel", "puntaje", "fecha"], visible=True, hide_vertical_scroll=True, key="t2"),
          sg.Table(dificil, headings=["nivel", "puntaje", "fecha"], visible=True, hide_vertical_scroll=True,
                   key="t3")]],
        key="col_niv", visible=False)

    columna_izq = sg.Column(
        [[sg.Frame("Mostrar puntaje TOP 10 por ", [[sg.Button("Puntaje", key="puntaje", disabled=True),
                                                    sg.Button("Nivel", key="nivel")]])],
         [sg.Button("volver")]])

    columna_der = sg.Column([[columna_nivel, columna_total]])
    layout = [[columna_izq, columna_der]]
    window = sg.Window("Puntajes").Layout(layout)
    while True:
        event, values = window.Read()

        if event == "nivel":
            window.Element("col_niv").Update(visible=True)
            window.Element("col_tot").Update(visible=False)
            window.Element("nivel").Update(disabled=True)
            window.Element("puntaje").Update(disabled=False)

        elif event == "puntaje":
            window.Element("col_niv").Update(visible=False)
            window.Element("col_tot").Update(visible=True)
            window.Element("nivel").Update(disabled=False)
            window.Element("puntaje").Update(disabled=True)

        else:
            window.Close()
            break


if __name__ == "__main__":
    puntajes_GUI()
