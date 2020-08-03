def ventana_juego():
    import PySimpleGUI as sg
    import random
    import boton
    import time
    from correccion_de_palabras import palabraValida
    from moduloIA import turno_pc
    from Configuracion import config_dictionary as configuracion
    from Puntajes import puntajes as Puntajes
    from datetime import datetime as fecha_y_hora

    user_config = configuracion.obtener_config()
    presionadas = []  # los cuadrantes que se seleccionaron del tablero
    botones_usados = []  # lista todos lod botones usados desde que se presiona la celda 7,7
    puntajeTotal = 0
    puntajeMaquina = 0
    turno = (True, False)  # verdadero yo, falso la maquina

    dic = dict()  # diccionario de botones(objetos)

    valores = user_config.convertir_a_valores()  # busca los valores de la letras en la configuracion
    bolsa = user_config.convertir_en_bolsa()  # busca todas las letras q se van a jugar en la configuracion
    tiempo_total = user_config.tiempo * 6000
    dificultad = user_config.dificultad
    print("Letras")
    print(bolsa)
    exception_bloqueo=["comenzar", "salir", "pausar"]

    def desbloquear_boton():
        """desbloquea todos los cuadrantes"""
        for lista in matriz:
            for boton in lista:
                if boton.get_text() == "":
                    boton.Update(disabled=False)

    def bloquear_boton():
        """bloquea todos los cuadrantes"""
        for lista in matriz:
            for boton in lista:
                if boton.get_text() not in exception_bloqueo:
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

    def cambiar_fichas(lista_fichas, bolsa):
        if len(bolsa) >= len(lista_fichas):
            for ficha in lista_fichas:
                cambio = window.Element(ficha).GetText()
                window.Element(ficha).Update(text=random.choice(bolsa))
                bolsa.append(cambio)
        else:
            sg.popup_error("No se puede cambiar por falta de fichas en la bolsa")

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
                bot.asignarColor(y, x, dificultad)
                linea.append(
                    sg.Button(
                        "",
                        key=clave,
                        disabled=True,
                        font='Courier 10',
                        size=(4, 2) if N <= 12 else (4, 2),
                        button_color=bot.color,
                        pad=(0, 0)
                    ),
                )
                dic[clave] = bot
            matriz.append(linea)
        linea = [
            sg.Submit("comenzar", key="comenzar", size=(9, 2)),
            sg.Submit("salir", key="salir", size=(9, 2)),
        ]
        matriz.append(linea)
        return matriz

    def crear_atril(nombre):
        atril_l = []
        for x in range(1, 8):
            boton = (sg.Button("", key=nombre + str(x), size=(4, 2), button_color=("black", "white"), disabled=True))
            atril_l.append(boton)
        return atril_l

    def crear_izquierda():
        return ([crear_atril("letra"),
                 [sg.Listbox(values=[], key='jugada1', size=(50, 10))],
                 [sg.Text("el puntaje es 0", key="puntaje", size=(20, 1))],
                 [sg.Text('', size=(8, 2), font=("Helvetica", 20), justification="center", key="-DISPLAY-")],
                 [
                     sg.Submit("Seleccionar Palabra", key="confirmar", disabled=True),
                     sg.Submit("Cambiar Letra", key="cambiar", disabled=True),
                     sg.Submit("Cancelar seleccion", key="cancelar", disabled=True)
                 ]
                 ])

    def generarAtrilIA():  # se puede atomatizar
        """se muesta el puntaje y el atril del jugador IA"""
        return ([crear_atril("bot"), [sg.Listbox(values=[], key="jugada2", size=(50, 10))]
            , [sg.Text("el puntaje es 0", key="puntajeIA", size=(20, 1))], ])

    def verificarConfirmar(list, l):
        """se pregunta si todo esta bien para insertar la palabras"""
        if (len(list) > 1) and (palabraValida(l, dificultad)):
            print('verificarConfirmar devuelve True')
            return True
        else:
            print('verificarConfirmar devuelve False')
            return False

    def time_as_int():
        return int(round(time.time() * 100))

    def fichaAtrilAI():
        l = []
        for i in range(7):
            l.append(buscar_ficha())
        return l

    def reponerFichas(atrilMaquina):
        while (len(atrilMaquina) != 7):
            atrilMaquina.append(buscar_ficha())

    def preguntar():
        """abre una ventana para preguntar si se elige una partida nueva o continua con una guardada"""

        layout2 = [[sg.Submit("Continuar con la partida ", key="continuar"),
                    sg.Submit("Iniciar una nueva partida ", key="no continuar")]]
        window2 = sg.Window("ScrabbleAR").Layout(layout2)
        event1, values1 = window2.Read()
        window2.Close()
        return event1

    def toma_valores_atril(atril, valores):
        suma = 0
        for x in atril:
            suma += valores[x]  # enviar valores como parametro
        return suma

    def popUp_cambio(atril_valores, bolsa, cambios_restantes):
        """Permite cambiar las letras seleccionadas"""

        botones_letras = []
        for x in range(0, 7):
            botones_letras.append(sg.Button(atril_valores[x], key=x+1, size=(4, 2)))

        layout = [
            [
                sg.Text("Seleccione la letras a cambiar")
            ],
            botones_letras,
            [
                sg.Text("cambios restantes: "+str(cambios_restantes))
            ],
            [
                sg.Button("Confirmar", key="cambio_confirmar"),
                sg.Button("Cancelar", key="cambio_cancelar"),
                sg.Button("Salir", key="cambio_salir")
            ]
        ]
        if cambios_restantes==0:
            sg.popup_error("No te quedan mas cambios")
        else:
            window_cambio = sg.Window("Cambiador de letras").Layout(layout)
            letras_a_cambiar = []
            letras_seleccion = []
            while True:
                event_cambio, values_cambio = window_cambio.Read()
                try:
                    if event_cambio == "cambio_confirmar":
                        if len(letras_a_cambiar) > 0:
                            cambiar_fichas(letras_a_cambiar, bolsa)
                            window_cambio.close()
                            cambios_restantes -= 1
                            return cambios_restantes

                    elif event_cambio in (None, "cambio_salir"):
                        window_cambio.close()
                        return cambios_restantes

                    elif event_cambio == "cambio_cancelar":
                        letras_a_cambiar = []
                        for x in letras_seleccion:
                            window_cambio.Element(x).Update(disabled=False)
                        letras_seleccion = []

                    elif event_cambio in range(0,8):
                        letras_seleccion.append(event_cambio)
                        letras_a_cambiar.append("letra"+str(event_cambio))
                        window_cambio.Element(event_cambio).Update(disabled=True)

                except Exception as e:
                    print(e)


    def fin_juego(puntaje_total,puntaje_maquina, atril_jugador, atril_maquina, valores):
        atril_player=[]
        for x in atril_jugador:
            atril_player.append(str(window.Element(x).get_text()))
        puntaje_total -= toma_valores_atril(atril_player, valores)
        puntaje_maquina -= toma_valores_atril(atril_maquina, valores)

        if puntaje_total > puntaje_maquina:
            sg.Popup("GANASTE!!! con: " + str(puntaje_total) + " puntos contra: " + str(puntaje_maquina) + " de la maquina")


        elif puntaje_maquina == puntaje_total:
            sg.Popup("Hubo empate")

        else:
            sg.Popup("Gano la maquina con: " + str(puntaje_maquina) + " puntos contra: " + str(puntaje_total) + " tuyos")

        puntaje = Puntajes.obtener_puntajes()

        if dificultad == "facil":
            puntaje.facil.append([dificultad, puntaje_total, fecha_y_hora.now().strftime("%Y-%m-%d %H:%M:%S")])
        elif dificultad == "medio":
            puntaje.medio.append([dificultad, puntaje_total, fecha_y_hora.now().strftime("%Y-%m-%d %H:%M:%S")])
        else:
            puntaje.dificil.append([dificultad, puntaje_total, fecha_y_hora.now().strftime("%Y-%m-%d %H:%M:%S")])
        puntaje.total.append([dificultad, puntaje_total, fecha_y_hora.now().strftime("%Y-%m-%d %H:%M:%S")])
        Puntajes.guardar_configuracion(puntaje)
        window.close()
        return

    evento = preguntar()
    if evento == "continuar":
        try:
            raise
        except:
            sg.popup("no hay partida guardada")
    elif (evento == "no continuar"):
        if len(bolsa) < 20:
            sg.PopupError("Minimo de letras permitodo es 20. Agregue mas y vuelva a intentar")
            exit()
        else:
            turno_elegido = random.choice(turno)
            inteligenciaArt = generarAtrilIA()
            matriz = generar_matriz()
            columna_derecha = matriz
            columna_izquierda = crear_izquierda()
    else:
        exit()

    layout = [
        [
            sg.Column(inteligenciaArt),
            sg.Column(columna_derecha),
            sg.Column(columna_izquierda)]
    ]

    window = sg.Window("ScrabbleAR").Layout(layout)
    jugada = []

    letras = []  # las letras seleccionadas para colocarlas en el tablero
    actual = ''
    event_anterior = ""
    atril_jugador = ("letra1", "letra2", "letra3", "letra4", "letra5", "letra6", "letra7")
    cambio = False
    comenzar = False
    cambios_restantes=3

    deshabiliatar = True  # utilizado para habilitar atril
    iniciado = False  # utilizado una sola vez para buscar las 7 letras del atril

    current_time, paused_time, paused = 0, time_as_int(), False  # variables del timer
    start_time = time_as_int()
    atrilMaquina = fichaAtrilAI()  # se crea el atril de la maquina
    puntajeMaquina=0
    puntajeTotal=0
    cambios_cantidad = 3
    # turnoEligido = random.choice(turno)

    while True:
        try:
            if not paused:
                if current_time < tiempo_total:
                    current_time = int(round(time.time() * 100)) - start_time
                else:  # se termina el juego y se define al ganador
                    raise Exception("TIMEOUT")

            if not comenzar:
                event, values = window.Read()
            else:
                event, values = window.Read(timeout=10)

            if event in (None, "salir"):  # si no recibe un evento se termina el programa
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
                deshabiliatar = not deshabiliatar
                for x in range(1, 8):
                    window.Element("letra" + str(x)).Update(disabled=deshabiliatar)
                    if not iniciado:
                        window.Element("letra" + str(x)).Update(text=buscar_ficha())
                iniciado = True
                window.Element("confirmar").Update(disabled=deshabiliatar)
                window.Element("cambiar").Update(disabled=deshabiliatar)
                window.Element("cancelar").Update(disabled=deshabiliatar)

                # inicio timer
                # cambiar boton a pausar

            elif event == "confirmar":  # ingresa la palabra en el tablero
                total = 0
                letra = ""
                for i in presionadas:
                    letra += window.Element(i).GetText()
                print(letra)

                if verificarConfirmar(presionadas, letra):
                    for clave in presionadas:  # suma el puntaje
                        palabra = window.Element(clave).GetText()
                        total += dic[clave].devolverValor(valores[
                                                              palabra])  # el diccionario de claves devuelve el boton con esa blave y el boton devuelve su valor
                    print(total)
                    puntajeTotal += total  # el puntaje real del jugador real
                    text = str(puntajeTotal)
                    window.FindElement('puntaje').Update("el puntaje es {}".format(text))  # muestra el puntaje
                    if len(presionadas) > 0:
                        for i in letras:
                            window.Element(i).Update(text=buscar_ficha())
                        #cambiar_fichas(letras, True)
                    jugada.append("la letra formada es: {0} y su valor de la jugada es: {1}".format(letra, total))
                    window.Element('jugada1').Update(jugada)
                    botones_usados.extend(presionadas)
                    presionadas = cancelar_seleccion(letras)
                    letras = []  # se elimina todas las letras
                    turno_elegido = not turno_elegido
                    # elif ('7,7' in presionadas):
                    #     for each in atril_jugador:  # cambia las letras del atril
                    #         window.Element(each).Update(disabled=False)
                    #     for clave in presionadas[1:]:  # vuelve al valor anterior a los botones selecionados de la matriz
                    #         window.Element(clave).Update(button_color=dic[clave].color)
                    #         window.Element(clave).Update(text="")
                    #     presionadas = cancelar_seleccion(letras)
                    #     letras = []
                else:
                    for each in atril_jugador:  # cambia las letras del atril
                        window.Element(each).Update(disabled=False)
                    for clave in presionadas:  # vuelve al valor anterior a los botones selecionados de la matriz
                        window.Element(clave).Update(button_color=dic[clave].color)
                        window.Element(clave).Update(text="")
                    presionadas = cancelar_seleccion(letras)
                    letras = []

            elif event == "cambiar":  # cambia las letras
                atril_cambio_valor=[]
                for x in atril_jugador:
                    atril_cambio_valor.append(window.Element(x).get_text())
                cambios_restantes = popUp_cambio(atril_cambio_valor, bolsa, cambios_restantes)


            elif event == "cancelar":  # debuelve las palabras que puse en el tablero
                presionadas = cancelar_seleccion(letras, presionadas)

            elif event in atril_jugador and not cambio:  # entra si se preciona una letra del atril
                print("Tipo: ", event)
                if event_anterior in atril_jugador:  # se fija si la letra anterior fue una del tablero para desbloquaer
                    window.Element(event_anterior).Update(disabled=False)
                    # if (len(presionadas) == 0 and (not '7,7' in botones_usados) ):  # desbloquea botones de la matriz
                    #     presionadas.append('7,7')
                    #     window.Element('7,7').Update(disabled=True,disabled_button_color=('black','red'))
                    #     desbloquear_boton()
                elif len(presionadas) == 0:
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
                    if event != "__TIMEOUT__" and not event in botones_usados:
                        presionadas.append(event)
                        window.Element(event).Update(text=actual)
                        window.Element(event).Update(button_color=("black", "violet"))
                        bloquear_boton()
                        # print(presionadas)

            if event != "__TIMEOUT__":
                event_anterior = event
            if not turno_elegido:
                print("turno de la maquina")
                print(atrilMaquina)
                # desbloquear_boton()
                puntajeMaquina += float(turno_pc(atrilMaquina, botones_usados, window, dificultad, valores, dic))
                window.Element("puntajeIA").Update("el puntaje total es: {}".format(str(puntajeMaquina)))
                print(atrilMaquina)
                reponerFichas(atrilMaquina)
                # bloquear_boton()

                turno_elegido = not turno_elegido
                print(botones_usados)

            window['-DISPLAY-'].Update('{:02d}:{:02d}.{:02d}'.format((current_time // 100) // 60,
                                                                     (current_time // 100) % 60,
                                                                     current_time % 100))
        except IndexError:
            fin_juego(puntajeTotal,puntajeMaquina, atril_jugador, atrilMaquina,valores)

        except Exception:
            fin_juego(puntajeTotal,puntajeMaquina, atril_jugador, atrilMaquina,valores)

    window.close()

if __name__ == "__main__":
    # try:
    ventana_juego()
    # except:
    print("sale")
