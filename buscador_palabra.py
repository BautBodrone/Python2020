import itertools as it
import random
import correccion_de_palabras as correccion

dic=dict()
dic['facil']=2
dic['medio']=3
dic['dificil']=4
def convertirTupla(tupla):  # sacado de geekforgeeks

    str = ''.join(tupla)
    return str

def buscar_palabra(atril, dificultad):

    for i in range(dic[dificultad],len(atril)):
        for each in it.permutations(atril,i):
            palabra=convertirTupla(each)
            if(correccion.palabraValida(palabra,dificultad)):
                return palabra
    return ""

