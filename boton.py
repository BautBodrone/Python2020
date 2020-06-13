class Boton:

    def __init__(self):
        self._valor=None
        self._color=None

    def asignarColor(self, i, j):
        """asigna un color a cada boton"""
        if (i,j) in ((1,5),(1,9),(13,9),(13,5),(6,6),(6,8),(8,6),(8,8),(5,1),(9,1),(9,13,),(5,13)):
            self._color = ("black", "blue")
            self._valor = lambda n: n-3
        elif (i,j) in ((1,1),(2,2),(3,3),(4,4),(5,5),(1,13),(2,12),(3,11),(4, 10),(5,9),(9,5),(10,4),(11,3),(12,2),(13,1),(9,9),(10,10),(11,11),(12,12),(13,13)):
            self._color = ("black", "red")
            self._valor = lambda  n: n-1
        elif (i,j) in ((0, 0),(0, 7),(0, 14),(7, 0),(7, 7),(7, 14),(14, 0),(14, 7),(14,14)):
            self._color = ("black", "brown")
            self._valor = lambda n: n*2
        elif (i,j) in ((0,4),(0,10),(10,0),(4,0),(4,14),(10,14),(14,4),(14,10),(2,6),(2,8),(8,2),(6,2),(12,6),(12,8),(8,12),(6,12),(3,7),(7,3),(11,7),(7,11)):
            self._color = ("black", "green")
            self._valor = lambda n: n*3
        else:
            self._color = ("black", "white")
            self._valor = lambda n: n+0


    def devolverValor(self, v):
        """devuelve el valor del boton"""
        return self._valor(v)

    @property
    def color(self):
        """es un getter"""
        return self._color







