import itertools as it
import random
import pattern.text.es as pt
import correccion_de_palabras as correccion


# CODIGO BOT
def buscador_palabra(tablero, difcultad):
    def convertirTupla(tupla):  # sacado de geekforgeeks
        str = ''.join(tupla)
        return str

    largo_palabra = random.randint(2, 7)
    posible = list(it.permutations(tablero, largo_palabra))
    for pos in posible:
        posible_pal = pt.spelling.suggest(convertirTupla(pos))[0]
        if posible_pal[1] == 1:
            if correccion.correccion_de_palabra(posible_pal[0], difcultad):
                return posible_pal
    return False
