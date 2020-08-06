# AUTORES:
# Bautista Jose Bodrone
# Javier Franco Jose Camacho Encinas
#
# GPL-3.0-or-later
import itertools as it
import random
import correccion_de_palabras as correccion

def convertirTupla(tupla):  # sacado de geekforgeeks
    str = ''.join(tupla)
    return str

def buscar_palabra(atril, dificultad,categoria):
    """permuta las fichas hasta encontrar una palabra dependiendo el largo que se elige al azar"""
    largo_palabras = [*range(2, 8)]
    for i in range(2, 8):
        largo = random.choice(largo_palabras)  # se elige un largo
        for each in it.permutations(atril,largo):#se recorren un lista de permutacion que se obtiene con permutations
            palabra = convertirTupla(each)
            if (correccion.palabraValida(palabra, dificultad, categoria)):#se pregunta si alguna palabra corresponde con
                return palabra                                             #la dificultad
        largo_palabras.remove(largo)  # se elimina el largo para que no se vuelva a repetir ese tamaño de palabras
    return False

