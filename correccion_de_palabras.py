from pattern.es import verbs, spelling, lexicon, parse, split

def verbosOAdjetivos(palabra,soloVerbosOadjetivos,dificultad,categoria):
<<<<<<< HEAD
    """verifico si en caso de que la dificultad sea medio devuelva los verbos o adjetivos, o si en el caso de que sea
    la dificultad dificil devuelva la palabra segun la categoria elegida aleatoriamente """
=======
    """verifico que sea adjetivo o verbo"""
    #print(palabra)
>>>>>>> 78eb081f5d9b592eea79f20f45c9dc22bfcb1a1e
    dato=parse(palabra)
    VD=parse(palabra).split()[0][0][1]

    #print(VD)
    #print(dato)
    if dificultad == "medio":
        if VD in soloVerbosOadjetivos[dificultad]:
            print("medio")
            print(VD)
            print(palabra)
            return True
    elif VD in soloVerbosOadjetivos[categoria]:
        print(categoria)
        print(palabra)
        return True
    else:
        return False

def palabraValida(palabra,dificultad,categoria):
    """devuelve si la palabra es valida segun su dificultad """
<<<<<<< HEAD

=======
>>>>>>> 78eb081f5d9b592eea79f20f45c9dc22bfcb1a1e
    dificultadMedia={"medio":('JJ','JJR','JJS','VB','VDB','VBG','VBN','VBP','VBZ'),"verbos":('VB','VDB','VBG','VBN','VBP','VBZ'),"adjetivos":('JJ','JJR','JJS')}
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
            return verbosOAdjetivos(palabra, dificultadMedia,dificultad,categoria)