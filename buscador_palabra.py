import itertools as it
import random
import correccion_de_palabras as correccion

#dic=dict()
#dic['facil']=2
#dic['medio']=3
#dic['dificil']=4
def convertirTupla(tupla):  # sacado de geekforgeeks

    str = ''.join(tupla)
    return str

def buscar_palabra(atril, dificultad,categoria):
    largo_palabras = [*range(2, 8)]
    for i in range(2, 8):
        largo = random.choice(largo_palabras)
        for each in it.permutations(atril,largo):
            palabra=convertirTupla(each)
            if(correccion.palabraValida(palabra,dificultad,categoria)):
                return palabra
        largo_palabras.remove(largo)
    return ""

