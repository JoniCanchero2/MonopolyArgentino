class Casilla:
    def __init__(self, id_propiedad, nombre, color=None, propietario=None, valor_propiedad=0, valor_alquiler=0, cantidad_casas=0, casilla_especial=False, monto=0, valor_casa=0):
        self.id_propiedad = id_propiedad
        self.nombre = nombre
        self.color = color
        self.propietario = propietario
        self.valor_propiedad = valor_propiedad
        self.valor_alquiler = valor_alquiler
        self.cantidad_casas = cantidad_casas
        self.casilla_especial = casilla_especial
        self.monto = monto
        self.valor_casa = valor_casa


class Jugador:
    def __init__(self, id_jugador, nombre, dinero, posicion=0, propiedades_compradas=None):
        self.id_jugador = id_jugador
        self.nombre = nombre 
        self.dinero = dinero
        self.posicion = posicion
        self.propiedades_compradas = propiedades_compradas if propiedades_compradas else []
        #para la carcel
        self.en_carcel = False
        self.turnos_en_carcel = 0
        self.turnos_sin_tirar = 0  
        self.cartas_libertad = 0

class Tablero:
    def __init__(self):
        self.casillas = []
    
    def agregar_casilla(self, casilla):
        self.casillas.append(casilla)
    
    def mover_jugador(self, jugador, valor_dados):
        nueva_posicion = (jugador.posicion + valor_dados) % len(self.casillas)
        jugador.posicion = nueva_posicion
        return nueva_posicion
    
    def obtener_casilla(self, posicion):
        if 0 <= posicion < len(self.casillas):
            return self.casillas[posicion]
        return None