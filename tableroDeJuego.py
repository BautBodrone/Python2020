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
    import json

    jugada=[]

    user_config = configuracion.obtener_config()
    presionadas = []  # los cuadrantes que se seleccionaron del tablero
    botones_usados = []  # lista todos lod botones usados desde que se presiona la celda 7,7
    puntajeTotal = 0
    puntajeMaquina = 0
    turno = (True, False)  # verdadero yo, falso la maquina

    dic = dict()  # diccionario de botones(objetos)

    valores = user_config.convertir_a_valores()  # busca los valores de la letras en la configuracion
    print(valores)
    bolsa = user_config.convertir_en_bolsa()  # busca todas las letras q se van a jugar en la configuracion
    tiempo_total = user_config.tiempo * 6000
    dificultad = user_config.dificultad
    atril_jugador = ("letra1", "letra2", "letra3", "letra4", "letra5", "letra6", "letra7")

    exception_bloqueo = ["Comenzar", "Salir", "Pausar", "Posponer", "Terminar"]
    letras_del_jugador = []
    clavesMaquina = dict()
    clavesJugador = dict()
    jugadasMaquina=[]
    tamanio_matriz=15

    def desbloquear_boton():
        """desbloquea todos los cuadrantes"""
        for lista in matriz:
            for boton in lista:
                if boton.GetText() == "":
                    boton.Update(disabled=False)

    def bloquear_boton():
        """bloquea todos los cuadrantes"""
        for lista in matriz:
            for boton in lista:
                if boton.GetText() not in exception_bloqueo:
                    boton.Update(disabled=True, disabled_button_color=("black", "gray"))

    def checkear_disponibilidad(posicion):
        """se fija si el cuadrantes que se le pasa tiene o no una letra"""
        if window.Element(posicion).GetText() == "":
            return True
        else:
            return False

    def desbloquear_der_abajo(posicion, anterior="", tamanio=tamanio_matriz):
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
        if x < tamanio-1 and checkear_disponibilidad(pos):
            if anterior == "" or y_ant != y - 1:
                window.Element(pos).Update(disabled=False)
        pos = str(x) + "," + str(y + 1)
        if y < tamanio-1 and checkear_disponibilidad(pos):
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

    def cancelar_seleccion(letras, seleccion=[]):
        if len(seleccion) > 0:
            for clave in seleccion:
                window.Element(clave).Update(text="", disabled=True, button_color=dic[clave].color)
        for clave in letras:
            window.Element(clave).Update(disabled=False)
        return []

    def generar_matriz(dificultad,clavesMaquina="", clavesJugador="", tamanio=tamanio_matriz):
        """Genera una matriz de N filas y N columnas y muestra los botones de comenzar, terminar,pausar y salir"""
        if(clavesMaquina == ""):
            matriz = []
            for y in range(tamanio):
                linea = []
                for x in range(tamanio):
                    clave = str(x) + "," + str(y)
                    bot = boton.Boton()
                    bot.asignarColor(y, x, dificultad)
                    linea.append(
                        sg.Button(
                            "",
                            key=clave,
                            disabled=True,
                            font='Courier 10',
                            size=(4, 2),
                            button_color=bot.color,
                            pad=(0, 0)
                        ),
                    )
                    dic[clave] = bot
                matriz.append(linea)
            linea = [
                sg.Submit("Comenzar", key="comenzar", size=(9, 2)),
                sg.Submit("Posponer", key="posponer", size=(9, 2), disabled=True),
                sg.Submit("Terminar", key="terminar", size=(9, 2), disabled=True),
                sg.Submit("Salir", key="salir", size=(9, 2))
            ]
            matriz.append(linea)
        else:
            matriz = []
            for y in range(tamanio):
                linea = []
                for x in range(tamanio):
                    clave = str(x) + "," + str(y)
                    if (clave in clavesMaquina.keys()):
                        bot = boton.Boton()
                        bot.colorNuevo(("black","purple"))
                        le=clavesMaquina[clave]
                    elif (clave in clavesJugador.keys()):
                        bot = boton.Boton()
                        bot.colorNuevo(("black", "violet"))
                        le=clavesJugador[clave]
                    else:
                        bot = boton.Boton()
                        bot.asignarColor(y, x, dificultad)
                        le=""
                    linea.append(
                        sg.Button(
                            le,
                            key=clave,
                            disabled=True,
                            font='Courier 10',
                            size=(4, 2),
                            button_color=bot.color,
                            pad=(0, 0)
                        ),
                    )
                    dic[clave] = bot
                matriz.append(linea)
            linea = [
                sg.Submit("Comenzar", key="comenzar", size=(9, 2)),
                sg.Submit("Posponer", key="posponer", size=(9, 2), disabled=True),
                sg.Submit("Terminar", key="terminar", size=(9, 2), disabled=True),
                sg.Submit("Salir", key="salir", size=(9, 2))
            ]
            matriz.append(linea)
        return matriz

    def crear_atril(nombre):
        atril_l = []
        for x in range(1, 8):
            boton = (sg.Button("", key=nombre + str(x), size=(4, 2), button_color=("black", "white"), disabled=True))
            atril_l.append(boton)
        return atril_l

    def crear_derecha(jugada="",puntaje=""):
        """muestra el atril del jugador , los puntos , las jugadas con sus respectivos puntos y los botones de
        confirmar, cancelar o cambiar ficha"""
        if jugada == "":
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
        else:
            return ([crear_atril("letra"),
                     [sg.Listbox(values=jugada, key='jugada1', size=(50, 10))],
                     [sg.Text("el puntaje es "+str(puntaje), key="puntaje", size=(20, 1))],
                     [sg.Text('', size=(8, 2), font=("Helvetica", 20), justification="center", key="-DISPLAY-")],
                     [
                         sg.Submit("Seleccionar Palabra", key="confirmar", disabled=True),
                         sg.Submit("Cambiar Letra", key="cambiar", disabled=True),
                         sg.Submit("Cancelar seleccion", key="cancelar", disabled=True)
                     ]
                     ])

    def generarAtrilIA(categoria="",jugadas="",puntaje="", dificultad=""):  # se puede atomatizar
        """se muesta el puntaje , el atril del jugador IA y del ayuda memoria que muestra el valor de los colores de la
        tabla, el turno de jugador al que le toque poner la ficha y la dificultad"""
        if(puntaje == ""):
            ext=[[sg.Listbox(values=[], key="jugada2", size=(50, 10))],[sg.Text("el puntaje es 0", key="puntajeIA", size=(20, 1))]]
        else:
            print(jugadas)
            ext = [[sg.Listbox(values=jugadas, key="jugada2", size=(50, 10))],[sg.Text("el puntaje es "+str(puntaje), key="puntajeIA", size=(20, 1))]]
        list =[crear_atril("bot")]
        list.extend(ext)
        list.append(ayuda_memoria(categoria,dificultad))
        return list

    def verificarConfirmar(list, l,categoria):
        """se pregunta si todo esta bien para insertar la palabras"""
        if (len(list) > 1) and (palabraValida(l, dificultad,categoria)):
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
        while len(atrilMaquina) != 7:
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

    def guardar(**kwargs):
        """recibe un diccionario y lo almacena en formato json"""
        print(kwargs)
        archivo = open("guardar\jugadaGuardada", "w")
        json.dump(kwargs, archivo)
        archivo.close()

    def retomarPartida(datos):
        """esta funcion es usada para devolver las variables que no son una estructura de datos o variables de tipo
        string"""
        list=[]
        for each in range(10,27):
            list.append(datos["guardar"+str(each)])
        return list

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

        window_cambio = sg.Window("Cambiador de letras").Layout(layout)
        letras_a_cambiar = []
        letras_seleccion = []
        while True:
            event_cambio, values_cambio = window_cambio.Read()
            try:
                if event_cambio == "cambio_confirmar":
                    if len(letras_a_cambiar) > 0:
                        cambiar_fichas(letras_a_cambiar, bolsa)
                        window_cambio.Close()
                        cambios_restantes -= 1
                        return cambios_restantes, True

                elif event_cambio in (None, "cambio_salir"):
                    window_cambio.Close()
                    return cambios_restantes, False

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

    def ayuda_memoria(cate,dificultad):
        texto_deficultad = str(dificultad.capitalize()) + ": "
        if dificultad == "facil":
            texto_deficultad += "todo tipo"
        elif dificultad == "medio":
            texto_deficultad += "adjetivos y verbos"
        else:
            texto_deficultad += cate

        return [sg.Frame("Ayuda Memoria",[[sg.Text(texto_deficultad)],
                                          [sg.Text(" "*31,key="turno_actual_display")],
                                          [sg.Button("",size=(2,1),button_color=("black", "red"),disabled=True),
                                            sg.Text("-1 letra")],
                                           [sg.Button("",size=(2,1),button_color=("black", "blue"),disabled=True),
                                            sg.Text("-3 letra")],
                                           [sg.Button("",size=(2,1),button_color=("black", "green"),disabled=True),
                                            sg.Text("*2 letra")],
                                           [sg.Button("",size=(2,1),button_color=("black", "brown"),disabled=True),
                                            sg.Text("*3 letra")]])]

    def fin_juego(puntaje_total,puntaje_maquina, atril_jugador, atril_maquina, valores):
        atril_player=[]
        for x in atril_jugador:
            atril_player.append(str(window.Element(x).GetText()))
        resta_puntaje_jugadoer = toma_valores_atril(atril_player, valores)
        puntaje_final = puntaje_total - resta_puntaje_jugadoer
        puntaje_maquina -= toma_valores_atril(atril_maquina, valores)

        if puntaje_final > puntaje_maquina:
            sg.Popup("GANASTE!!! con: " + str(puntaje_final) + " puntos contra: " + str(puntaje_maquina) +
                     " de la maquina", "Puntos por palabra: " + str(puntaje_total) + " - Puntos letras no usadas: " +
                     str(resta_puntaje_jugadoer))

        elif puntaje_maquina == puntaje_final:
            sg.Popup("Hubo empate de: " + str(puntaje_final))

        else:
            sg.Popup("Gano la maquina con: " + str(puntaje_maquina) + " puntos contra: " + str(puntaje_final) + " tuyos"
                     , "Puntos por palabra: " + str(puntaje_total) + " - Puntos letras no usadas: " +
                     str(resta_puntaje_jugadoer))

        puntaje = Puntajes.obtener_puntajes()

        if dificultad == "facil":
            puntaje.facil.append([dificultad, puntaje_total, fecha_y_hora.now().strftime("%Y-%m-%d %H:%M:%S")])
        elif dificultad == "medio":
            puntaje.medio.append([dificultad, puntaje_total, fecha_y_hora.now().strftime("%Y-%m-%d %H:%M:%S")])
        else:
            puntaje.dificil.append([dificultad, puntaje_total, fecha_y_hora.now().strftime("%Y-%m-%d %H:%M:%S")])
        puntaje.total.append([dificultad, puntaje_total, fecha_y_hora.now().strftime("%Y-%m-%d %H:%M:%S")])
        Puntajes.guardar_puntajes(puntaje)
        window.Close()
        return

    evento = preguntar()
    if evento == "continuar":
        try:
            """si se selecciona continuar se crea un layout a partir de los datos guardados"""
            archivo = open("guardar\jugadaGuardada", "r")
            datos = json.load(archivo)
            jugada = datos["guardar0"]
            letras = datos["guardar1"]
            atrilMaquina = datos["guardar2"]
            clavesJugador = datos["guardar3"]
            clavesMaquina = datos["guardar4"]
            jugadasMaquina = datos["guardar5"]
            bolsa = datos["guardar6"]
            valores = datos["guardar7"]
            botones_usados = datos["guardar8"]
            letras_del_jugador = datos["guardar9"]
            turno_elegido, deficultad, event_anterior, puntajeMaquina, puntajeTotal, cambios_cantidad, current_time\
                , tiempo_total, paused_time, paused, start_time, comenzar, iniciado, deshabiliatar\
                , cambio, cambios_restantes,cate = retomarPartida(datos)
            inteligenciaArt = generarAtrilIA(cate,jugadasMaquina, puntajeMaquina,dificultad=dificultad)
            matriz = generar_matriz(dificultad, clavesMaquina, clavesJugador)
            columna_izquierda = matriz
            columna_derecha = crear_derecha(jugada, puntajeTotal)
        except FileNotFoundError:
            sg.popup("no hay partida guardada")
    elif evento == "no continuar":
        """si se selecciona continuar se crea un layout desde cero"""
        if len(bolsa) < 20:
            sg.PopupError("Minimo de letras permitodo es 20. Agregue mas y vuelva a intentar")
            exit()
        else:
            turno_elegido = random.choice(turno)
            cate = ""
            if dificultad == "dificil" :
                categoria =["adjetivos","verbos"]
                cate = random.choice(categoria)
                inteligenciaArt = generarAtrilIA(categoria=cate,dificultad=dificultad)
            else:
                inteligenciaArt = generarAtrilIA(dificultad=dificultad)

            matriz = generar_matriz(dificultad)
            columna_izquierda = matriz
            columna_derecha = crear_derecha()

            cambios_restantes = 3
            cambios_cantidad = 3

            current_time, paused_time, paused = 0, time_as_int(), False  # variables del timer
            start_time = time_as_int()
            atrilMaquina = fichaAtrilAI()  # se crea el atril de la maquina

            puntajeMaquina = 0
            puntajeTotal = 0
            actual = ''
            event_anterior = ""
    else:
        exit()

    layout = [
        [
            sg.Column(inteligenciaArt),
            sg.Column(columna_izquierda),
            sg.Column(columna_derecha)]
    ]

    window = sg.Window("ScrabbleAR").Layout(layout)

    letras = []  # las letras seleccionadas para colocarlas en el tablero

    cambio = False
    comenzar = False

    deshabiliatar = True  # utilizado para habilitar atril
    iniciado = False  # utilizado una sola vez para buscar las 7 letras del atril

    while True:
        """main loop del programa el cual tiene en cuenta las opviones a seleccionar"""
        try:
            if not paused:
                """si no esta pausado el tiempo del timer corre normalmente"""
                if current_time < tiempo_total:
                    current_time = int(round(time.time() * 100)) - start_time
                else:  # se termina el juego y se define al ganador
                    raise TimeoutError

            if not comenzar:
                event, values = window.Read()  # espera leer un click en pantalla
            else:
                event, values = window.Read(
                    timeout=10)  # utilizado para el que avance el timer y para leer click de botones

            window.Element("turno_actual_display").Update(value="Turno actual: Jugador")

            if event in (None, "salir"):  # si no recibe un evento se termina el programa
                window.Close()
                break

            elif event is "comenzar":
                comenzar = not comenzar
                if comenzar:
                    window.Element("comenzar").Update(text="Pausar")
                    start_time = start_time + time_as_int() - paused_time
                else:
                    paused_time = time_as_int()
                    window.Element("comenzar").Update(text="Comenzar")
                deshabiliatar = not deshabiliatar
                if evento != "continuar":
                    for x in range(1, 8):
                        window.Element("letra" + str(x)).Update(disabled=deshabiliatar)
                        if not iniciado:
                            window.Element("letra" + str(x)).Update(text=buscar_ficha())
                else:
                    paused = not paused
                    x = 1

                    for i in letras_del_jugador:
                        window.Element("letra" + str(x)).Update(disabled=deshabiliatar)
                        if not iniciado:
                            window.Element("letra" + str(x)).Update(text=i)
                        x += 1
                    letras_del_jugador = []
                iniciado = True
                window.Element("confirmar").Update(disabled=deshabiliatar)
                window.Element("cambiar").Update(disabled=deshabiliatar)
                window.Element("cancelar").Update(disabled=deshabiliatar)
                window.Element("posponer").Update(disabled=deshabiliatar)
                window.Element("terminar").Update(disabled=deshabiliatar)

            elif event == "posponer":
                paused = not paused
                iniciado
                paused_time = time_as_int()
                for i in atril_jugador:
                    letras_del_jugador.append(window.Element(i).GetText())

                print(letras_del_jugador)
                guardar(guardar0=jugada, guardar1=letras, guardar2=atrilMaquina, guardar3=clavesJugador,
                        guardar4=clavesMaquina,
                        guardar5=jugadasMaquina, guardar6=bolsa, guardar7=valores,
                        guardar8=botones_usados, guardar9=letras_del_jugador, guardar10=turno_elegido,
                        guardar11=dificultad,
                        guardar12=event_anterior, guardar13=puntajeMaquina, guardar14=puntajeTotal,
                        guardar15=cambios_cantidad, guardar16=current_time, guardar17=tiempo_total,
                        guardar18=paused_time, guardar19=paused, guardar20=start_time, guardar21=comenzar,
                        guardar22=iniciado, guardar23=deshabiliatar, guardar24=cambio, guardar25=cambios_restantes,
                        guardar26=cate)
                break

            elif event == "terminar":
                """termina el juego levantando un excepcion para que lo agarre le except"""
                raise TimeoutError

            elif event == "confirmar":  # ingresa la palabra en el tablero
                total = 0
                letra = ""
                for i in presionadas:
                    letra += window.Element(i).GetText()
                print(letra)

                if verificarConfirmar(presionadas, letra, cate):
                    for clave in presionadas:  # suma el puntaje
                        palabra = window.Element(clave).GetText()
                        total += dic[clave].devolverValor(valores[
                                                              palabra])  # el diccionario de claves devuelve el boton con esa blave y el boton devuelve su valor
                        clavesJugador[clave] = window.Element(clave).GetText()
                    print(total)
                    puntajeTotal += total  # el puntaje real del jugador real
                    text = str(puntajeTotal)
                    window.FindElement("puntaje").Update("el puntaje es {}".format(text))  # muestra el puntaje
                    if len(presionadas) > 0:
                        for i in letras:
                            window.Element(i).Update(text=buscar_ficha())
                        # cambiar_fichas(letras, True)
                    jugada.append("la letra formada es: {0} y su valor de la jugada es: {1}".format(letra, total))
                    window.Element('jugada1').Update(jugada)
                    botones_usados.extend(presionadas)
                    presionadas = cancelar_seleccion(letras)
                    letras = []  # se elimina todas las letras
                    turno_elegido = not turno_elegido
                else:
                    for each in atril_jugador:  # cambia las letras del atril
                        window.Element(each).Update(disabled=False)
                    for clave in presionadas:  # vuelve al valor anterior a los botones selecionados de la matriz
                        window.Element(clave).Update(button_color=dic[clave].color)
                        window.Element(clave).Update(text="")
                    presionadas = cancelar_seleccion(letras)
                    letras = []

            elif event == "cambiar":  # cambia las letras
                if cambios_restantes == 0:
                    sg.popup_error("No te quedan mas cambios")
                else:
                    presionadas = cancelar_seleccion(letras, presionadas)
                    atril_cambio_valor = []
                    for x in atril_jugador:
                        atril_cambio_valor.append(window.Element(x).GetText())
                    cambios_restantes, cambio_realizado = popUp_cambio(atril_cambio_valor, bolsa, cambios_restantes)
                    if cambio_realizado:
                        turno_elegido = not turno_elegido

            elif event == "cancelar":  # debuelve las palabras que puse en el tablero
                presionadas = cancelar_seleccion(letras, presionadas)

            elif event in atril_jugador and not cambio:  # entra si se preciona una letra del atril
                print("Tipo: ", event)
                if event_anterior in atril_jugador:  # se fija si la letra anterior fue una del tablero para desbloquaer
                    window.Element(event_anterior).Update(disabled=False)
                elif len(presionadas) == 0:
                    if window.Element("7,7").GetText() != "":
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

            if event != "__TIMEOUT__":
                event_anterior = event
            if not turno_elegido:
                print("turno de la maquina")
                print(atrilMaquina)
                puntajeMaquina += float(
                    turno_pc(atrilMaquina, botones_usados, window, dificultad, valores, dic, jugadasMaquina,
                             clavesMaquina, cate))
                if puntajeMaquina is not False:
                    window.Element("puntajeIA").Update("el puntaje total es: {}".format(str(puntajeMaquina)))
                    print(atrilMaquina)
                    reponerFichas(atrilMaquina)

                turno_elegido = not turno_elegido
                print(botones_usados)

            window.Element("-DISPLAY-").Update("{:02d}:{:02d}.{:02d}".format((current_time // 100) // 60,
                                                                             (current_time // 100) % 60,
                                                                             current_time % 100))

        except (IndexError, TimeoutError):
             fin_juego(puntajeTotal, puntajeMaquina, atril_jugador, atrilMaquina, valores)
             break

        except Exception as e:
            print("!!!!!"+str(e)+"¡¡¡¡¡")

    window.Close()


if __name__ == "__main__":
    # try:
    ventana_juego()
    # except:
    print("sale")
