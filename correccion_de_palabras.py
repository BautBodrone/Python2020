from pattern.es import verbs, spelling, lexicon, parse, split

def verbosOAdjetivos(palabra,soloVerbosOadjetivos):
    """verifico que sea adjetivo o verbo"""
    #print(palabra)
    dato=parse(palabra)
    VD=parse(palabra).split()[0][0][1]

    #print(VD)
    #print(dato)
    if VD in soloVerbosOadjetivos:
        print(palabra)
        return True
    else:
        return False

def palabraValida(palabra,dificultad):
    """devuelve si la palabra es valida segun su dificultad """
    dificultadMedia=['JJ','JJR','JJS','VB','VDB','VBG','VBN','VBP','VBZ'] # es una lista con como representa pattern los verbos o adjetivos
    if (not palabra.lower() in verbs):#pregunta si no es un verbo en caso de que no sea verdadero es porque es un verbo
        if (not palabra.lower() in spelling):# pregunta si es una palabra que esta dentro de spelling
            if (not(palabra.lower() in lexicon) and not(palabra.upper() in lexicon) and not(palabra.capitalize() in lexicon)):#pregunta si esta dentro de lexicon
                ok=False
            else:
                ok=True
        else:
            ok=True
    else:
        ok=True
    if (ok):
        if (dificultad == 'facil'):
            return True
        else:
            return verbosOAdjetivos(palabra,dificultadMedia)