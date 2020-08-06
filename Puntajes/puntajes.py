# AUTORES:
# Bautista Jose Bodrone
# Javier Franco Jose Camacho Encinas
#
# GPL-3.0-or-later
import json
from os import sep  # Sirve para las /\ de los os

class ConfigEncoder(json.JSONEncoder):
    """Adapta los datos de la clase Configuracion para poder enviarlos a un archivo con formato .json"""
    def default(self, obj):
        return obj.__dict__

class Puntajes:

    def __init__(self,facil=[["","",""]], medio=[["","",""]], dificil=[["","",""]], total=[["","",""]]):
        self.facil = facil
        self.medio = medio
        self.dificil = dificil
        self.total = total

    def solo_top_diez(self,lista):
        try:
            return sorted(lista, key=lambda x: x[1], reverse=True)[:10]
        except TypeError:
            return sorted(lista, reverse=True)

    def por_nivel(self):
        self.facil = self.solo_top_diez(self.facil)
        self.medio = self.solo_top_diez(self.medio)
        self.dificil = self.solo_top_diez(self.dificil)

        return self.facil, self.medio, self.dificil

    def por_puntaje(self):
        self.total = self.solo_top_diez(self.total)

        return self.total

def obtener_puntajes():
    def abrir_puntajes():
        """crea puntajes nueva con datos predeterminados"""
        puntajes = Puntajes()
        archivo_puntajes = open("Puntajes" + sep + "puntajes.json", "w+")
        json.dump(puntajes, archivo_puntajes, cls=ConfigEncoder, indent=4)
        return puntajes

    """intenta abrir la puntajes sino crea un predeterminada"""
    try:
        archivo_puntajes = open("Puntajes" + sep + "puntajes.json", "r")
    except:
        puntajes = abrir_puntajes()

    else:
        """intenta obtener los datos de la config sino crea otra"""
        try:
            p = json.load(archivo_puntajes)
            puntajes = Puntajes(facil=p["facil"],
                                medio=p["medio"],
                                dificil=p["dificil"],
                                total=p["total"]
            )

        except:
            puntajes = abrir_puntajes()

    return puntajes


def guardar_puntajes(puntajes):
    """busca el archivo de puntajes y los sobreescribe si lo econcuetra sino crea otro
    devuelve true o false para avisar al user si hubo un error"""
    try:
        archivo_puntajes = open("Puntajes" + sep + "puntajes.json", "w+")
        json.dump(puntajes, archivo_puntajes, cls=ConfigEncoder, indent=4)
    except:
        exito = False
    else:
        exito = True

    return exito