def ventana_juego():
    import PySimpleGUI as sg
    import random
    import boton
    import time
    from correccion_de_palabras import palabraValida

    presionadas = []  # los cuadrantes que se seleccionaron del tablero
    botones_usados=[] #lista todos lod botones usados desde que se presiona la celda 7,7
    puntajeTotal = 0
    turno = ( True, False )#verdadero yo, falso la maquina
    dic = dict()  # diccionario de botones(objetos)
    fichas = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U",
              "V", "W", "X", "Y", "Z"]

    valores = {"A": 1, "B": 3, "C": 3, "D": 2, "E": 1, "F": 4, "G": 2, "H": 4, "I": 1, "J": 1, "K": 5, "L": 1, "M": 3,
               "N": 1, "O": 1, "P": 3, "Q": 10, "R": 1, "S": 1, "T": 1, "U": 1, "V": 4, "W": 4, "X": 8, "Y": 4, "Z": 10}

    bolsa = ["A", "A", "A", "B", "B", "C", "D", "D", "E", "E", "E", "F", "G", "H", "I", "I", "J", "K", "L", "M", "N",
             "O", "O", "P", "Q", "R", "S"]
    boton_inicial=""
    def desbloquear_boton():
        """desbloquea todos los cuadrantes"""
        for lista in matriz:
            for boton in lista:
                boton.Update(disabled=False)

    def bloquear_boton():
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
        """desbloquea los cuadrantes de abajo o de la derecha dependiendo de la forma que se esta escribiendo
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

    def cambiar_fichas(lista_fichas,remover_ficha=False):  # se le asigna una nueva letra al usuario
        if len(bolsa) >= len(lista_fichas):
            for ficha in lista_fichas:
                cambio = window.Element(ficha).GetText()
                window.Element(ficha).Update(text=random.choice(bolsa))
                if not remover_ficha:
                    bolsa.append(cambio)

    def buscar_ficha():
        text = random.choice(bolsa)
        bolsa.remove(text)
        return text

    def salir(e):
        return e is None

    def cancelar_seleccion(letras, seleccion=[]):
        if len(seleccion) > 0:
            for clave in seleccion:
                window.Element(clave).Update(text="", disabled=True, button_color=dic[clave].color)
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
                bot = boton.Boton()
                bot.asignarColor(y, x, "facil")
                linea.append(
                    sg.Button(
                        "",
                        key=clave,
                        disabled=True,
                        font='Courier 10',
                        size=(4, 2) if N <= 12 else (2, 1),
                        button_color=bot.color,
                    ),
                )
                dic[clave] = bot
            matriz.append(linea)
        linea = [
            sg.Submit("comenzar", key='comenzar', size=(9, 2)),
            sg.Submit("salir", key='salir', size=(9, 2)),
        ]
        matriz.append(linea)
        return matriz

    def crear_atril(nombre):
        atril_l=[]
        for x in range(1,8):
            boton=(sg.Button("", key=nombre+str(x), size=(4, 2), button_color=("black", "white"),
                             disabled=True))
            atril_l.append(boton)
        return atril_l

    def crear_izquierda():#tambien se puede atomatizar con "letra"+(1+n)
        return ([crear_atril("letra"),
                 [sg.Text("el puntaje es 0", key="puntaje", size=(20, 1))],
                 [sg.Text('', size=(8, 2), font=('Helvetica', 20), justification='center', key='-DISPLAY-')],
                 [
                     sg.Submit("Seleccionar Palabra", key="confirmar", disabled=True),
                     sg.Submit("Cambiar Letra", key="cambiar", disabled=True),
                     sg.Submit("CANCELAR SELECCIÓN", key="cancelar", disabled=True)
                ]
            ])
    def generarAtrilIA():#se puede atomatizar
        """se muesta el puntaje y el atril del jugador IA"""
        return ([crear_atril("bot")
        ,[sg.Text("el puntaje es 0", key="puntajeIA",size=(20, 1))],])


    def devolverString(x, y):
        return (str(x) + "," + str(y))

    def letrasPegadas(cla, usados):  # falta verificar por si esta fuera de rango
        """verifica que si la letras esta pegada a otra"""
        x, y = int(cla[0]), int(cla[1])
        if devolverString(x - 1, y) in usados:
            return True
        elif devolverString(x + 1, y) in usados:
            return True
        elif devolverString(x, y + 1) in usados:
            return True
        elif devolverString(x, y - 1) in usados:
            return True
        else:
            return False

    def palabrasPegadas(claves, usados):
        """verifica si la palabras esta pegada a otra, letra por letra"""
        for each in claves:
            if (letrasPegadas(each.split(","), usados)):
                return True
        return False

    def HorozontalesVerticales(presionados, usados):
        """verifica si la palabras esta en vertical o Horizontal en caso de ser verdadero devuelve True sino false"""
        if (("7,7") in presionados):
            return True
        else:
            return palabrasPegadas(presionados, usados)


    def letrasPegadas(cla,usados):# falta verificar por si esta fuera de rango
        """verifica que si la letras esta pegada a otra"""
        x, y = int(cla[0]), int(cla[1])
        if devolverString(x-1,y) in usados:
            return True
        elif devolverString(x+1,y) in usados:
            return True
        elif devolverString(x,y+1) in usados:
            return True
        elif devolverString(x,y-1) in usados:
            return True
        else:
            return False

    def palabrasPegadas(claves,usados):
        """verifica si la palabras esta pegada a otra, letra por letra"""
        for each in claves:
            if (letrasPegadas(each.split(","),usados)):
                return True
        return False

    def HorozontalesVerticales(presionados,usados):
        """verifica si la palabras esta en vertical o Horosoltal en caso de ser verdadero devuelve True sino false"""
        if (("7,7") in presionados):
            return True
        else:
            return palabrasPegadas(presionados,usados)

    def verificarConfirmar(list,totalCeldas,l):
        """se pregunta si todo esta bien para insertar la palabras"""
        if (HorozontalesVerticales(list,totalCeldas)) and (len(list) > 1) and (palabraValida(l, 'facil')):
            print('verificarConfirmar devuelve True')
            return True
        else:
            print('verificarConfirmar devuelve False')
            return False

    def time_as_int():
        return int(round(time.time() * 100))


    inteligenciaArt = generarAtrilIA()
    matriz = generar_matriz()
    columna_derecha = matriz
    columna_izquierda = crear_izquierda()

    layout = [
            [
            sg.Column(inteligenciaArt),
            sg.Column(columna_derecha),
            sg.Column(columna_izquierda)]
    ]

    window = sg.Window("ScrabbleAR").Layout(layout)

    letras = []  # las letras seleccionadas para colocarlas en el tablero
    actual = ''
    event_anterior = ""
    tablero_jugador = ("letra1", "letra2", "letra3", 'letra4', 'letra5', 'letra6', 'letra7')
    cambiar=False
    comenzar=False

    deshabiliatar = True#utilizado para habilitar atril
    iniciado=False#utilizado una sola vez para buscar las 7 letras del atril

    current_time, paused_time, paused = 0, 0, False #variables del timer
    start_time = time_as_int()

    turnoEligido = random.choice(turno)
    while True:
        if (turnoEligido):

            if not comenzar:
                event, values = window.Read()
            else:
                event, values = window.Read(timeout=10)

            if event in (None, 'salir'):  # si no recibe un evento se termina el programa
                window.Close()
                break

            elif event is "comenzar":
                comenzar = not comenzar
                if comenzar:
                    window.Element("comenzar").Update(text="pausar")
                    start_time = start_time + time_as_int() - paused_time
                else:
                    paused_time = time_as_int()
                    window.Element("comenzar").Update(text="comenzar")
                deshabiliatar=not deshabiliatar
                for x in range (1,8):
                    window.Element("letra"+str(x)).Update(disabled=deshabiliatar)
                    if not iniciado:
                        window.Element("letra"+str(x)).Update(text=buscar_ficha())
                iniciado=True
                window.Element("confirmar").Update(disabled=deshabiliatar)
                window.Element("cambiar").Update(disabled=deshabiliatar)
                window.Element("cancelar").Update(disabled=deshabiliatar)

                #inicio timer
                #cambiar boton a pausar

            elif event == "confirmar":  # ingresa la palabra en el tablero
                total = 0
                letra=""
                for i in presionadas:
                    letra += window.Element(i).GetText()
                print(letra)

                if verificarConfirmar(presionadas, botones_usados, letra):
                    for clave in presionadas:  # suma el puntaje
                        palabra = window.Element(clave).GetText()
                        total += dic[clave].devolverValor(valores[palabra])  # el diccionario de claves devuelve el boton con esa blave y el boton devuelve su valor
                    print(total)
                    puntajeTotal += total #el puntaje real del jugador real
                    text = str(puntajeTotal)
                    window.FindElement('puntaje').Update("el puntaje es {}".format(text)) #muestra el puntaje
                    if len(presionadas) > 0:
                        cambiar_fichas(letras, True)
                    botones_usados.extend(presionadas)
                    presionadas = cancelar_seleccion(letras)
                    letras = []  # se elimina todas las letras
                    turnoEligido = not turnoEligido
                # elif ('7,7' in presionadas):
                #     for each in tablero_jugador:  # cambia las letras del atril
                #         window.Element(each).Update(disabled=False)
                #     for clave in presionadas[1:]:  # vuelve al valor anterior a los botones selecionados de la matriz
                #         window.Element(clave).Update(button_color=dic[clave].color)
                #         window.Element(clave).Update(text="")
                #     presionadas = cancelar_seleccion(letras)
                #     letras = []
                else:
                    for each in tablero_jugador:  # cambia las letras del atril
                        window.Element(each).Update(disabled=False)
                    for clave in presionadas:  # vuelve al valor anterior a los botones selecionados de la matriz
                        window.Element(clave).Update(button_color=dic[clave].color)
                        window.Element(clave).Update(text="")
                    presionadas = cancelar_seleccion(letras)
                    letras = []

            elif event == "cambiar":  # cambia las letras
                # presionadas = cancelar_seleccion(letras, presionadas)
                # cambiar = not cambiar
                # window.Element("cancelar").Update(disabled=True)
                # window.Element("confirmar").Update(disabled=True)
                # letras_para_cambiar=[]
                # while cambiar and event is not None:
                #     if event == "cambiar":
                #         cambiar= not cambiar
                #         for i in letras_para_cambiar:
                #             window.Element(i).Update(disabled=False)
                #             window.Element(i).Update(random.choice(fichas))
                #     elif event in tablero_jugador:
                #         letras_para_cambiar.append(event)
                #         window.Element(event).Update(disabled=True)
                if (event is None):
                    break
                else:
                    window.Element("cancelar").Update(disabled=False)
                    window.Element("confirmar").Update(disabled=False)
                    turnoEligido= not turnoEligido

            elif event == "cancelar":  # debuelve las palabras que puse en el tablero
                presionadas = cancelar_seleccion(letras, presionadas)

            elif event in tablero_jugador:  # entra si se preciona una letra del atril
                print("Tipo: ", event)
                if event_anterior in tablero_jugador:  # se fija si la letra anterior fue una del tablero para desbloquaer
                    window.Element(event_anterior).Update(disabled=False)
                # if (len(presionadas) == 0 and (not '7,7' in botones_usados) ):  # desbloquea botones de la matriz
                #     presionadas.append('7,7')
                #     window.Element('7,7').Update(disabled=True,disabled_button_color=('black','red'))
                #     desbloquear_boton()
                elif len(presionadas) == 0 :
                    if window.Element("7,7").get_text() != "":
                        desbloquear_boton()
                    else:
                        print("habilitado")
                        window.Element("7,7").Update(disabled=False)
                        print(event)
                elif len(presionadas) < 2:  # desbloquea botones dependiendo de la pos
                    desbloquear_der_abajo(presionadas[len(presionadas) - 1])
                else:
                    desbloquear_der_abajo(presionadas[len(presionadas) - 1], presionadas[len(presionadas) - 2])
                actual = window.Element(event).GetText()
                window.Element(event).Update(disabled=True, disabled_button_color=("silver", "silver"))
                letras.append(event)

            else:  
                if event in presionadas:
                    presionadas.remove(event)
                    window.Element(event).Update(text="")
                    window.Element(event).Update(button_color=("black", "white"))
                else:  # entra si la celda del tablero esta en blanco
                    if event != "__TIMEOUT__":
                        presionadas.append(event)
                        window.Element(event).Update(text=actual)
                        window.Element(event).Update(button_color=("black", "red"))
                        bloquear_boton()
                    #print(presionadas)
            if event != "__TIMEOUT__":
                event_anterior = event
        if not turnoEligido:
            print("turno de la maquina")
            turnoEligido = not turnoEligido

        window['-DISPLAY-'].Update('{:02d}:{:02d}.{:02d}'.format((current_time // 100) // 60,
                                                                 (current_time // 100) % 60,
                                                                 current_time % 100))
    window.close()


if __name__ == "__main__":
    ventana_juego()