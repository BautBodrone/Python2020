# AUTORES:
# Bautista Jose Bodrone
# Javier Franco Jose Camacho Encinas
#
# GPL-3.0-or-later
def nivel(dificultad):
    """es una funcion que se usa para armar el tablero dependiendo la dificultad el diccionario contiene el color
    para cada celda del tablero"""
    dic = dict()
    dic['azul'] = [(1, 5), (1, 9), (13, 9), (13, 5), (6, 6), (6, 8), (8, 6), (8, 8), (5, 1), (9, 1), (9, 13,), (5, 13)]
    dic['rojo'] = [(1, 1), (3, 3), (5, 5), (1, 13), (3, 11), (5, 9), (9, 5), (11, 3), (13, 1), (9, 9), (11, 11),
                   (13, 13)]
    dic['marron'] = [(0, 0), (0, 7), (0, 14), (7, 0), (7, 14), (14, 0), (14, 7), (14, 14)]
    dic['verde'] = [(0, 3), (0, 11), (11, 0), (3, 0), (3, 14), (11, 14), (14, 3), (14, 11), (2, 6), (2, 8), (8, 2),
                    (6, 2), (12, 6), (12, 8), (8, 12), (6, 12), (3, 7), (7, 3), (11, 7), (7, 11)]
    aux1 = [(2, 2), (4, 4), (10, 10), (12, 12), (2, 12), (4, 10), (10, 4), (12, 2)]
    aux2 = [(5, 7), (7, 5), (9, 7), (7, 9)]
    aux3 = [(1, 4), (2, 5), (3, 6), (4, 7), (3, 8), (2, 9), (1, 10), (4, 1), (5, 2), (6, 3), (7, 4), (8, 3), (9, 2),
            (10, 1), (4, 13), (5, 12), (6, 11), (7, 10), (8, 11), (9, 12), (10, 13), (10, 7), (11, 6), (12, 5), (13, 4),
            (11, 8), (12, 9), (13, 10)]

    if (dificultad == "facil"):
        dic['verde'].extend(aux1)

    elif (dificultad == "medio"):
        dic['rojo'].extend(aux1)
        dic['rojo'].extend(aux2)

    elif (dificultad == "dificil"):
        dic['rojo'].extend(aux1)
        dic['rojo'].extend(aux3)

    return dic
