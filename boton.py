import color_para_boton as color
class Boton:

    def __init__(self):
        self._valor=None
        self._color=None

    def asignarColor(self, i, j, dificultad):
        """asigna un color y un valor con multiplicacion y descuento a cada boton"""
        dic=color.nivel(dificultad)
        if (i, j) in dic['azul']:
            self._color = ("black", "blue")
            self._valor = lambda n: n-3
        elif (i, j) in dic['rojo']:
            self._color = ("black", "red")
            self._valor = lambda  n: n-1
        elif (i, j) in dic['marron']:
            self._color = ("black", "brown")
            self._valor = lambda n: n*3
        elif (i, j) in dic['verde']:
            self._color = ("black", "green")
            self._valor = lambda n: n*2
        elif (i, j) == (7,7):
            self._color = ("black", "orange")
            self._valor = lambda n: n+0
        else:
            self._color = ("black", "white")
            self._valor = lambda n: n+0


    def devolverValor(self, v):
        """resive un valor y devuelve el valor del boton dependiendo del valor que reciba como parametro"""
        return self._valor(v)
    def colorNuevo(self,color):
        """este color se asigna a las claves que ya fueron usados por el jugador o la maquina"""
        self._color=color

    @property

    def color(self):
        """es un getter que devuelve el color del boton"""
        return self._color