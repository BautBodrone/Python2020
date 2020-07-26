from buscador_palabra import buscar_palabra

dic=dict()
dic['facil']=2
dic['medio']=3
dic['dificil']=4
fichas = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U",
              "V", "W", "X", "Y", "Z"]

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


def no_choca(pos, palabra, x, y, letrast):
    for i in palabra:
        if not devolverString(x,y) in letrast:
            pos[i]=(x,y)
            y+=1
        else:
            return False
    return True


def primera_jugada(window, dificultad,letrasT):
    palabra = buscar_palabra(fichas, dificultad)
    x,y=7,7
    for letra in palabra:
        clave = str(x)+','+str(y)
        #window.Element(clave).Update(disabled = False)
        window.Element(clave).Update(text = letra)
        window.Element(clave).Update(disabled = True, disabled_button_color=("black", "red"))
        y+=1
        letrasT.append(clave)
    return  window
def se_sigue(letraT, dificultad, window, n=15):
    palabra = buscar_palabra(fichas, dificultad)
    pos = dict()
    for x in range(n):
        for y in range(n):
            if (letrasPegadas(devolverString(x,y).split(","),letraT)):
                if(no_choca(pos,palabra,x,y,letraT)):
                    break
    if(len(pos) == dic[dificultad]):
        for i in pos.keys():
            window.Element(devolverString(pos[i][0],pos[i][1])).Update(disabled=False)
            window.Element(devolverString(pos[i][0],pos[i][1])).Update(i)
            window.Element(devolverString(pos[i][0], pos[i][1])).Update(disabled=False)
            letraT.append(devolverString(pos[i][0], pos[i][1]))


def turno_pc(letrasT, window, dificultad ):
    if len(letrasT) == 0:
        return primera_jugada( window, dificultad, letrasT)
    else:
        return se_sigue(letrasT, dificultad, window)