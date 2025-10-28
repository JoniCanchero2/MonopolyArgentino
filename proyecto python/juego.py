import random
#traer los archivos anteriores
from seteador import cargar_tablero_completo
from objetos import Jugador

class Juego:
    def __init__(self):
        self.tablero = cargar_tablero_completo()  # reutiliza la función existente
        self.jugadores = []
        self.turno_actual = 0
        self.ronda = 1

    def agregar_jugador(self, nombre):
            jugador = Jugador(len(self.jugadores) + 1, nombre, dinero=1500)
            self.jugadores.append(jugador)
            print(f"✅ Jugador {nombre} agregado")
            return jugador
    
    def tirar_dados(self):
        dado1 = random.randint(1, 6)
        dado2 = random.randint(1, 6)
        total = dado1 + dado2
        print(f"🎲 Dados: {dado1} + {dado2} = {total}")
        return total
    

    ############

    def siguiente_turno(self):
        if not self.jugadores:
            print("❌ No hay jugadores")
            return None
        
        jugador = self.jugadores[self.turno_actual]

        # genera muchos =
        print(f"\n{'='*50}")
        print(f"🎯 RONDA {self.ronda} - TURNO DE {jugador.nombre.upper()}")
        print(f"💰 Dinero: ${jugador.dinero}")

        # mostrar posición actual
        casilla_actual = self.tablero.casillas[jugador.posicion]
        print(f"📍 Posición actual: {casilla_actual.nombre}")

        # tirar dados y mover
        dados = self.tirar_dados()
        nueva_pos = self.tablero.mover_jugador(jugador, dados)
        nueva_casilla = self.tablero.casillas[nueva_pos]
    
        print(f"🔄 Movió a: {nueva_casilla.nombre}")

        #### en esta parte se tiene que crear la jugabilidad ####
        self.procesar_casilla(jugador, nueva_casilla)

        # prepara el siguiente turno
        self.turno_actual = (self.turno_actual + 1) % len(self.jugadores)
        if self.turno_actual == 0:  # nueva ronda
            self.ronda += 1
            
        return jugador
    
    def procesar_casilla(self, jugador, casilla):
    #Procesa lo que sucede cuando un jugador cae en una casilla"""
        if not casilla.casilla_especial:
            self.procesar_propiedad(jugador, casilla)
        else:
            # Para casillas especiales (por ahora solo mensaje)
            print(f"⚡ Casilla especial: {casilla.nombre}")
            # Aquí después agregarás impuestos, suerte, etc.

    def procesar_propiedad(self, jugador, propiedad):
        #Maneja la compra y alquiler de propiedades"""
        if propiedad.propietario is None:
            # Ofrecer compra
            if jugador.dinero >= propiedad.valor_propiedad:
                respuesta = input(f"¿Quieres comprar {propiedad.nombre} por ${propiedad.valor_propiedad}? (s/n): ")
                if respuesta.lower() == 's':
                    propiedad.propietario = jugador
                    jugador.dinero -= propiedad.valor_propiedad
                    jugador.propiedades_compradas.append(propiedad)
                    print(f"✅ {jugador.nombre} compró {propiedad.nombre}")
                else:
                    print(f"❌ {jugador.nombre} decidió no comprar {propiedad.nombre}")
            else:
                print(f"❌ {jugador.nombre} no tiene suficiente dinero para comprar {propiedad.nombre}")
        else:
            # Pagar alquiler
            if propiedad.propietario != jugador:
                alquiler = propiedad.valor_alquiler
                jugador.dinero -= alquiler
                propiedad.propietario.dinero += alquiler
                print(f"💰 {jugador.nombre} paga ${alquiler} de alquiler a {propiedad.propietario.nombre}")

    def mostrar_estado(self):
        print(f"\n📊 ESTADO GENERAL - Ronda {self.ronda}")
        for jugador in self.jugadores:
            casilla = self.tablero.casillas[jugador.posicion]
            print(f"   {jugador.nombre}: ${jugador.dinero} | Pos: {casilla.nombre}")

    
# Función de prueba
def probar_sistema_turnos():
    juego = Juego()
    
    # Agregar jugadores
    '''
    juego.agregar_jugador("Ana")
    juego.agregar_jugador("Luis")
    juego.agregar_jugador("Carlos")
    '''
    #elige la cantiadad de turnos
    turnos=int(input("Cantidad de turnos: "))

    for i in range(3):
        nombre = input("Ingresa nombre del jugador: ")
        juego.agregar_jugador(nombre)
        
    print("\n🎮 INICIANDO SIMULACIÓN DE TURNOS")
    
    
    # Simular 5 turnos por jugador
    for _ in range(turnos * len(juego.jugadores)):
        input("\n⏎ Presiona Enter para siguiente turno...")
        juego.siguiente_turno()
        juego.mostrar_estado()

if __name__ == "__main__":
    probar_sistema_turnos()
