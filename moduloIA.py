import random

from buscador_palabra import buscar_palabra



def devolverString(x, y):
    """devuelve un string con los parametro recividos """
    return (str(x) + "," + str(y))


def primera_jugada(fichas, window, dificultad, letrasT, valores, valor_boton, jugada, claves,categoria):
    """como es la primera jugada se inserta tranquilamente en la posicion inicial del juego se elige si se inserta
     abajo o a la derecha dependiendo del valor que reciba la variable "lugar" del la operacion random.choice()"""
    palabra = buscar_palabra(fichas, dificultad,categoria)
    if palabra is not False:
        puntos = 0
        x, y = 7, 7
        lugar = random.choice([True, False])  # true=derecha y false=abajo
        if lugar:
            for i in palabra:
                clave = devolverString(x, y)
                puntos += valor_boton[clave].devolverValor(valores[i])
                window.Element(clave).Update(text=i)
                window.Element(clave).Update(disabled=True, button_color=("black", "purple"))
                fichas.remove(i)
                claves[clave] = i
                y += 1
                letrasT.append(clave)
        else:
            for i in palabra:
                clave = devolverString(x, y)
                puntos += valor_boton[clave].devolverValor(valores[i])
                window.Element(clave).Update(text=i)
                window.Element(clave).Update(disabled=True, button_color=("black", "purple"))
                fichas.remove(i)
                claves[clave] = i
                x += 1
                letrasT.append(clave)
        jugada.append("la letra formada es: {0} y su valor de la jugada es: {1}".format(palabra, puntos))
        window.Element("jugada2").update(jugada)

        return puntos
    else:
        return False

def se_sigue(fichas, letrast, dificultad, window, valores, valor_boton, jugada, claves,categoria):
    """como a la maquina no le toca insertar letras en la primera posicion entonces busca un lugar donde insertar
    sin que se choque con ninguna palabra ya formada """
    n = 0
    ok = False
    puntos = 0
    palabra = buscar_palabra(fichas, dificultad,categoria)
    if palabra is not False:
        while not ok:
            x = random.randrange(15)
            y = random.randrange(15)
            clave = devolverString(x, y)
            if not clave in letrast:
                lugar = random.choice([True, False])  # true=derecha y false=abajo
                abajo = True
                derecha = True
                while (
                        abajo or derecha) and not ok:  # entra en el while para ver si se puede colocar en posicon ya sea abajo o arriba sin chocar con otras palabras
                    print(palabra)
                    if lugar:
                        letras_dic = dict()
                        tamanioPalabra = len(palabra)
                        if (tamanioPalabra + x) < 15:  # se fija que no este fuera del rango
                            auxX = x
                            for i in palabra:  # pregunta por si el tamaño no choca con otra palabra
                                if devolverString(auxX, y) in letrast:
                                    abajo = not abajo
                                    break
                                else:
                                    clave = devolverString(auxX, y)
                                    letras_dic[clave] = i
                                    auxX += 1
                        else:
                            abajo = not abajo
                            lugar = not lugar
                        print("el tamanio es: " + str(len(letras_dic)))
                        if len(letras_dic) == len(palabra) and len(palabra)>= 2:  # si el tamaño es acorde a la dificultad pone la letra
                            print(palabra)
                            for i in letras_dic.keys():
                                letrast.append(i)
                                claves[i] = letras_dic[i]
                                puntos += valor_boton[i].devolverValor(valores[letras_dic[i]])
                                window.Element(i).Update(text=letras_dic[i], button_color=("black", "purple"))
                                fichas.remove(letras_dic[i])
                            jugada.append(
                                "la letra formada es: {0} y su valor de la jugada es: {1}".format(palabra, puntos))
                            window.Element("jugada2").Update(jugada)
                            print(palabra)
                            ok = True  # con esto sale
                    else:
                        letras_dic = dict()
                        tamanioPalabra = len(palabra)
                        if (tamanioPalabra + y) < 15:
                            auxY = y
                            for i in palabra:
                                if devolverString(x, auxY) in letrast:
                                    derecha = not derecha
                                    break
                                else:
                                    clave = devolverString(x, auxY)
                                    letras_dic[clave] = i
                                    auxY += 1
                        else:
                            derecha = not derecha
                            lugar = not lugar
                        print("el tamanio es: " + str(len(letras_dic)))
                        if len(letras_dic) == len(palabra) and len(palabra)>= 2 :
                            print(palabra)
                            for i in letras_dic.keys():
                                letrast.append(i)
                                puntos += valor_boton[i].devolverValor(valores[letras_dic[i]])
                                window.Element(i).Update(text=letras_dic[i], button_color=("black", "purple"))
                                claves[i] = letras_dic[i]
                            jugada.append(
                                "la letra formada es: {0} y su valor de la jugada es: {1}".format(palabra, puntos))
                            window.Element("jugada2").Update(jugada)
                            ok = True
                    if (n < 50):
                        n += 1
                    else:
                        break
            if (n < 50):  # para que no quede en un bucle infinico en caso de que no hay lugar
                n += 1
            else:
                break

        return puntos
    else:
        return False


def turno_pc(fichas, letrasT, window, dificultad, valores, valor_boton, jugada, claves,categoria):
    """en este modulo se determina si la pc empieza primero y inserta la palabra en la posicion inicial o si
    inserta en una posicion aleatoria del tablero """
    if len(letrasT) == 0:  # en el caso de no sea 0 es porque no hay ninguna palabra puesta y la palabra se pone el 77
        puntaje = primera_jugada(fichas, window, dificultad, letrasT, valores, valor_boton, jugada, claves,categoria)
        return puntaje
    else:
        puntaje = se_sigue(fichas, letrasT, dificultad, window, valores, valor_boton, jugada, claves,categoria)
        return puntaje
