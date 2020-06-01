def ventana_juego():
    import PySimpleGUI as sg
    import random

    valores = {"A": 1, "B": 3, "C": 3, "D": 2, "E": 1, "F": 4, "G": 2, "H": 4, "I": 1, "J": 1, "K": 5, "L": 1, "M": 3,
               "N": 1, "O": 1, "P": 3, "Q": 10, "R": 1, "S": 1, "T": 1, "U": 1, "V": 4, "W": 4, "X": 8, "Y": 4, "Z": 10}

    bolsa = ["A", "A", "A", "B", "B", "C", "D", "D", "E", "E", "E", "F", "G", "H", "I", "I", "J", "K", "L", "M", "N",
             "O", "O", "P", "Q", "R", "S"]

    def desbloquear_boton():
        """desbloquea todos los cuadrantes"""
        for lista in matriz:
            for boton in lista:
                boton.Update(disabled=False)

    def bloquar_boton():
        """bloquea todos los cuadrantes"""
        for lista in matriz:
            for boton in lista:
                boton.Update(disabled=True, disabled_button_color=("black", "grey"))

    def checkear_disponibilidad(posicion):
        """se fija si el cuadrantes que se le pasa tiene o no una letra"""
        if window.Element(posicion).GetText() == "":
            return True
        else:
            return False

    def desbloquear_der_abajo(posicion, anterior=""):
        """desbloquea los cuadrantes de abajo o de la derecha dependiendo de la forma que se esta escrinbiendo
            la palabra"""
        # hay que cambiar el 15 por el numero maximo de casilla de la matriz
        posicion = posicion.split(",")
        x, y = int(posicion[0]), int(posicion[1])
        pos = str(x + 1) + "," + str(y)
        if anterior != "":
            anterior = anterior.split(",")
            x_ant, y_ant = int(anterior[0]), int(anterior[1])
            print(x, y)
            print(x_ant, y_ant)
        if x < 14 and checkear_disponibilidad(pos):
            if anterior == "" or y_ant != y - 1:
                window.Element(pos).Update(disabled=False)
        pos = str(x) + "," + str(y + 1)
        if y < 14 and checkear_disponibilidad(pos):
            if anterior == "" or x_ant != x - 1:
                window.Element(pos).Update(disabled=False)

    def buscar_fichas(lista_fichas, remover_ficha=False):
        if len(bolsa) >= len(lista_fichas):
            for ficha in lista_fichas:
                cambio = window.Element(ficha).GetText()
                window.Element(ficha).Update(text=random.choice(bolsa))
                if not remover_ficha:
                    bolsa.append(cambio)

    def salir(e):
        return e is None

    def cancelar_seleccion(letras, seleccion=[]):
        if len(seleccion) > 0:
            for clave in seleccion:
                window.Element(clave).Update(text="", disabled=True, button_color=("black", "white"))
        for clave in letras:
            window.Element(clave).Update(disabled=False)
        return []

    def generar_matriz(N):
        """Genera una matriz de N filas y N columnas"""
        matriz = []
        for y in range(N):
            linea = []
            for x in range(N):
                clave = str(x) + "," + str(y)
                linea.append(
                    sg.Button(
                        "",
                        key=clave,
                        disabled=True,
                        font='Courier 10',
                        size=(4, 2) if N <= 12 else (2, 1),
                        button_color=("black", "white"),
                    ),
                )
            matriz.append(linea)

        return matriz

    matriz = generar_matriz(15)
    columna_derecha = matriz
    columna_izquierda = [
        [sg.Submit(
            "A",
            key="letra1",
            size=(4, 2),
            button_color=("black", "white")),
            sg.Submit(
                "B",
                key="letra2",
                size=(4, 2),
                button_color=("black", "white")),
            sg.Submit(
                "C",
                key="letra3",
                size=(4, 2),
                button_color=("black", "white"))
        ],
        [
            sg.Submit("Seleccionar Palabra", key="confirmar"),
            sg.Submit("Cambiar Letra", key="cambiar"),
            sg.Submit("CANCELAR SELECCIÓN", key="cancelar")
        ]
    ]

    layout = [
        [
            sg.Column(columna_derecha),
            sg.Column(columna_izquierda)
        ]
    ]

    window = sg.Window("ScrabbleAR").Layout(layout)
    event, values = window.Read()

    presionadas = []  # los cuadrantes que se seleccionaron del tablero
    letras = []  # las letras seleccionadas para colocarlas en el tablero
    actual = ''

    while not salir(event):

        if event is None:
            window.Close()
            break

        elif event == "confirmar":
            # confirmar es solo de testing por ahora
            palabra = ""
            total = 0
            for clave in presionadas:
                palabra += window.Element(clave).GetText()
            for letra in palabra:
                total += valores[letra]
            if len(presionadas) > 0:
                buscar_fichas(letras, True)
            presionadas = cancelar_seleccion(letras)
            letras = []

        elif event == "cambiar":
            print("solotesting")
        elif event == "cancelar":
            presionadas = cancelar_seleccion(letras, presionadas)

        elif event in ("letra1", "letra2", "letra3"):
            print("Tipo: ", event)
            if len(presionadas) == 0:
                desbloquear_boton()
            elif len(presionadas) < 2:
                desbloquear_der_abajo(presionadas[len(presionadas) - 1])
            else:
                desbloquear_der_abajo(presionadas[len(presionadas) - 1], presionadas[len(presionadas) - 2])
            actual = window.Element(event).GetText()
            window.Element(event).Update(disabled=True, disabled_button_color=("silver", "silver"))
            letras.append(event)

        else:
            print(presionadas)
            if event in presionadas:
                presionadas.remove(event)
                window.Element(event).Update(text="")
                window.Element(event).Update(button_color=("black", "white"))
            else:
                presionadas.append(event)
                window.Element(event).Update(text=actual)
                window.Element(event).Update(button_color=("black", "red"))
                bloquar_boton()

        event, values = window.Read()


if __name__ == "__main__":
    ventana_juego()
