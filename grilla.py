def ventana_juego():
    import PySimpleGUI as sg
    import random
    dic=dict()

    valores = {"A": 1, "B": 3, "C": 3, "D": 2, "E": 1, "F": 4, "G": 2, "H": 4, "I": 1, "J": 1, "K": 5, "L": 1, "M": 3,
               "N": 1, "O": 1, "P": 3, "Q": 10, "R": 1, "S": 1, "T": 1, "U": 1, "V": 4, "W": 4, "X": 8, "Y": 4, "Z": 10}

    bolsa = ["A", "A", "A", "B", "B", "C", "D", "D", "E", "E", "E", "F", "G", "H", "I", "I", "J", "K", "L", "M", "N",
             "O", "O", "P", "Q", "R", "S"]

    marrones = ((0, 0),(0, 7),(0, 14),(7, 0),(7, 7),(7, 14),(14, 0),(14, 7),(14,14))
    rojos = ((1,1),(2,2),(3,3),(4,4),(5,5),(1,13),(2,12),(3,11),(4, 10),(5,9),(9,5),(10,4),(11,3),(12,2),(13,1),(9,9),(10,10),(11,11),(12,12),(13,13))
    azules = ((1,5),(1,9),(13,9),(13,5),(6,6),(6,8),(8,6),(8,8),(5,1),(9,1),(9,13,),(5,13))
    verdes = ((0,4),(0,10),(10,0),(4,0),(4,14),(10,14),(14,4),(14,10),(2,6),(2,8),(8,2),(6,2),(12,6),(12,8),(8,12),(6,12),(3,7),(7,3),(11,7),(7,11))
    def asignarColor(clave,x,y):
        """"se asigna un color a cada clave"""
        if(x,y) in rojos:
            dic[clave] = "red"
            return ("black", "red")
        elif(x,y) in azules:
            dic[clave] = "blue"
            return ("black", "blue")
        elif(x,y) in marrones:
            dic[clave] = "brown"
            return ("black", "brown")
        elif(x,y) in verdes:
            dic[clave] = "green"
            return ("black", "green")
        else:
            dic[clave] ='white'
            return("black", "white")
    def valorDeBoton(clave,n):
        """"se asigna el valor de cada ficha dependiendo en que color es asigando en la matriz"""
        if dic[clave] == 'red':
            return (n-1)
        elif dic[clave] == 'blue':
            return (n-3)
        elif dic[clave] == 'green':
            return (n*2)
        elif dic[clave] == 'brown':
            return (n*3)
        return(n)
    def desbloquear_boton():
        """desbloquea todos los cuadrantes"""
        for lista in matriz:
            for boton in lista:
                boton.Update(disabled=False)

    def bloquar_boton():
        """bloquea todos los cuadrantes"""
        for lista in matriz:
            for boton in lista:
                boton.Update(disabled=True, disabled_button_color=("black", "gray"))

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

    def buscar_fichas(lista_fichas, remover_ficha=False):# se le asigna una nueva letra al usuario
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

    def generar_matriz(N=15):
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
                        button_color=asignarColor(clave,x,y),
                    ),
                )
            matriz.append(linea)
        linea = [
            sg.Submit("comenzar",key= 'comenzar' ,size=(9, 2)),
            sg.Submit("salir", key= 'salir' ,size=(9, 2)),
        ]
        matriz.append(linea)
        return matriz

    def crear_izquierda():
      return   ([ [sg.Submit(
            random.choice(bolsa),
            key="letra1",
            size=(4, 2),
            button_color=("black", "white")),
            sg.Submit(
                random.choice(bolsa),
                key="letra2",
                size=(4, 2),
                button_color=("black", "white")),
            sg.Submit(
                random.choice(bolsa),
                key="letra3",
                size=(4, 2),
                button_color=("black", "white")),
            sg.Submit(
                random.choice(bolsa),
                key="letra4",
                size=(4, 2),
                button_color=("black", "white")),
            sg.Submit(
                random.choice(bolsa),
                key="letra5",
                size=(4, 2),
                button_color=("black", "white")),
            sg.Submit(
                random.choice(bolsa),
                key="letra6",
                size=(4, 2),
                button_color=("black", "white")),
            sg.Submit(
                random.choice(bolsa),
                key="letra7",
                size=(4, 2),
                button_color=("black", "white")),
        ],
        [
            sg.Submit("Seleccionar Palabra", key="confirmar"),
            sg.Submit("Cambiar Letra", key="cambiar"),
            sg.Submit("CANCELAR SELECCIÓN", key="cancelar")
        ]
       ])

    matriz = generar_matriz()
    columna_derecha = matriz
    columna_izquierda = crear_izquierda()

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

        if event is None:#si no recibe un evento se termina el programa
            window.Close()
            break
        if event == 'salir':
            window.close()
            break
        elif event == "confirmar":#ingresa la palabra en el tablero
            # confirmar es solo de testing por ahora
            palabra = ""
            total = 0
            n=0
            for clave in presionadas:
                palabra += window.Element(clave).GetText()
            for letra in palabra:
                total += valorDeBoton(presionadas[n],valores[letra])
                n+=1
            print(total)
            if len(presionadas) > 0:
                buscar_fichas(letras, True)
            presionadas = cancelar_seleccion(letras)
            letras = [] #se elimina todas las letras

        elif event == "cambiar":#cambia las letras
                   print('falta')
        elif event == "cancelar":#debuelve las palabras que puse en el tablero
            presionadas = cancelar_seleccion(letras, presionadas)

        elif event in ("letra1","letra2", "letra3",'letra4','letra5','letra6','letra7'):#ingresa palabras
            print("Tipo: ", event)
            if len(presionadas) == 0:
                desbloquear_boton()
            elif len(presionadas) < 2:
                desbloquear_der_abajo(presionadas[len(presionadas) - 1])
            else:
                desbloquear_der_abajo(presionadas[len(presionadas) - 1], presionadas[len(presionadas) - 2])
            actual = window.Element(event).GetText()# hay un problema de si presiono 2 o mas fichas
            window.Element(event).Update(disabled=True, disabled_button_color=("silver", "silver"))
            letras.append(event)

        else:#se entra cada vez que toco una celda de la matriz
            print(presionadas)
            if event in presionadas:
                presionadas.remove(event)
                window.Element(event).Update(text="")
                window.Element(event).Update(button_color=("black", "white"))
            else:#entra si la celda del tablero esta en blaco
                presionadas.append(event)
                window.Element(event).Update(text=actual)
                window.Element(event).Update(button_color=("black", "red"))
                bloquar_boton()

        event, values = window.Read()


if __name__ == "__main__":
    ventana_juego()