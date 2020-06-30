import pattern.text.es as pt


def correccion_de_palabra(palabra, dificultad):
    correcto = False
    for palabra in pt.lexicon.items():
        if palabra[0] == palabra:
            correcto = True
            break
    if correcto:
        if pt.parse(palabra, tokenize=False, tags=True, chunks=False).split("/")[1] in dificultad: #aca iria la dif del juego
            return True
    return False


if __name__ == "main":
    correccion_de_palabra()