class casilla():
  def __init__(self, id_propuedad, nombre, color, propietario,valor_propiedad, valor_alquiler, cantidad_casas):
    self.id_propuedad = id_propuedad
    self.nombre = nombre
    self.color = color
    self.propietario = propietario
    self.valor_propiedad = valor_propiedad
    self.valor_alquiler = valor_alquiler
    self.cantidad_casas = cantidad_casas


class jugador():
  def __init__(self, id_jugador, dinero, posicion, propiedades_compradas):
    self.id_jugador = id_jugador
    self.dinero = dinero
    self.posicion = posicion
    self.propiedades_compradas = propiedades_compradas

class tablero(): 
  def __init__(self, id_propiedad, nombre):
    self.id_propiedad = id_propiedad
    self.nombre = nombre

  def mover_jugador(self, posicion, valor_dados):
    nueva_posicion = (posicion + valor_dados)
    return nueva_posicion
