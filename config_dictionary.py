import json
from os import sep  # Sirve para las /\ de los os


class Configuracion:

    def __init__(self,
                 tiempo: 2,
                 dificultad: "facil",
                 valor_fichas: {"A, E, O, S, I, U, N, L, R, T": 1,
                                "C, D, G": 2,
                                "M, B, P": 3,
                                "F, H, V, Y": 4,
                                "J": 6,
                                "K, LL, Ñ, Q, RR, W, X": 8,
                                "Z": 10},
                 cantidad_fichas: {"A": 11, "B": 3, "C": 4, "D": 4, "E": 11, "F": 2, "G": 2, "H": 2, "I": 6, "J": 2,
                                   "K": 1, "L": 4, "M": 3,
                                   "N": 5, "O": 8, "P": 2, "Q": 1, "R": 4, "S": 7, "T": 4, "U": 6, "V": 2, "W": 1,
                                   "X": 1, "Y": 1, "Z": 1},
                 tablero: "clasico"
                 ):
        self.tiempo: tiempo
        self.dificultad: dificultad
        self.valor_fichas: valor_fichas
        self.cantidad_fichas: cantidad_fichas
        self.tablero: tablero

    @property
    def to_dict(self):
        return self.__dict__

    def get_dificultad(self):
        return self.dificultad

    def get_tablero(self):
        return self.tablero

    def get_cantidad_fichas(self):
        return self.cantidad_fichas

    def get_tiempo(self):
        return self.tiempo

    def get_valor_fichas(self):
        return self.valor_fichas

def obtener_config():
    def abrir_configuracion():
        """crea config nueva con datos predeterminados"""
        configuracion = Configuracion()
        archivo_configuracion = open('Configuracion' + sep + 'config.json', 'w+')
        json.dump(configuracion, archivo_configuracion)
        return configuracion

    """intenta abrir la configuracion sino crea un predeterminada"""
    try:
        archivo_configuracion = open('Configuracion' + sep + 'config.json', 'r')
    except:
        configuracion = abrir_configuracion()

    else:
        """intenta obtener los datos de la config sino crea otra"""
        try:
            c = json.load(archivo_configuracion)
            configuracion = Configuracion(
                tiempo=c["tiempo"],
                dificultad=c["dificultad"],
                valor_fichas=c["valor_fichas"],
                cantidad_fichas=c["cantidad_fichas"],
                tablero=c["tablero"]
            )

        except:
            configuracion = abrir_configuracion()

    return configuracion


def guardar_configuracion(configuracion):
    """busca el archivo de configuracion y los sobreescribe si lo econcuetra sino crea otro
    devuelve true o false para avisar al user si hubo un error"""
    exito = False
    try:
        archivo_configuracion = open('Configuracion' + sep + 'config.json', 'w+')
        json.dump(configuracion, archivo_configuracion)
    except:
        exito = False
    else:
        exito = True

    return exito
