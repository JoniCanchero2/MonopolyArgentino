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

            if casilla.nombre == "Impuesto Medio":
                jugador.dinero -= casilla.monto
                print(f"💸 {jugador.nombre} paga impuesto de ${casilla.monto}")

            elif casilla.nombre == "Visita a la Cárcel":
                print(f"🚓 {jugador.nombre} visita la cárcel (solo de paso)")

            elif casilla.nombre == "Suerte":
                self.procesar_carta_suerte(jugador)

            elif "Lineas" in casilla.nombre:
                self.procesar_transporte(jugador, casilla)
            # Aquí después agregarás impuestos, suerte, etc.

    def procesar_carta_suerte(self, jugador):
    #Cartas de suerte aleatorias"""
        cartas = [
            {"texto": "Corralito de dolares perdes", "monto": -150},
            {"texto": "Ganaste la rifa del dia del padre ganaste", "monto": 50},
            {"texto": "Encuentras dinero en la calle", "monto": 50},
            {"texto": "Miraste la hora en el lugar equivacado te robaron el celular", "monto": -150},
            {"texto": "Multa por exceso de velocidad", "monto": -50}
        ]
        carta = random.choice(cartas)
        jugador.dinero += carta["monto"]
        
        if carta["monto"] > 0:
            print(f"🎁 SUERTE: {carta['texto']} +${carta['monto']}")
        else:
            print(f"🎁 SUERTE: {carta['texto']} -${abs(carta['monto'])}")


    def procesar_transporte(self, jugador, transporte):
    #Procesa cualquier línea de transporte (todas funcionan igual)"""
        if transporte.propietario is None:
            # Ofrecer compra
            if jugador.dinero >= transporte.valor_propiedad:
                respuesta = input(f"¿Quieres comprar {transporte.nombre} por ${transporte.valor_propiedad}? (s/n): ")
                if respuesta.lower() == 's':
                    transporte.propietario = jugador
                    jugador.dinero -= transporte.valor_propiedad
                    jugador.propiedades_compradas.append(transporte)
                    print(f"✅ {jugador.nombre} compró {transporte.nombre}")
                    
                    # Mostrar estrategia
                    lineas_actuales = self.contar_lineas_transporte(jugador)
                    print(f"   🎯 Ahora tienes {lineas_actuales} líneas de transporte")
                    if lineas_actuales >= 2:
                        print(f"   ⚡ ¡El alquiler de tus líneas ahora se multiplica!")
            else:
                print(f"❌ {jugador.nombre} no tiene suficiente dinero para {transporte.nombre}")
        else:
            # Pagar alquiler - depende de cuántas líneas tenga el dueño
            if transporte.propietario != jugador:
                alquiler = self.calcular_alquiler_transporte(transporte.propietario, transporte)
                jugador.dinero -= alquiler
                transporte.propietario.dinero += alquiler
                
                lineas_propietario = self.contar_lineas_transporte(transporte.propietario)
                print(f"🚌 {jugador.nombre} paga ${alquiler} por usar {transporte.nombre}")
                print(f"   📊 {transporte.propietario.nombre} tiene {lineas_propietario} líneas de transporte")

    def contar_lineas_transporte(self, jugador):
        ####Cuenta cuántas líneas de transporte tiene un jugador"""
        # Busca cualquier propiedad que tenga "Linea de" en el nombre
        lineas = 0
        for propiedad in jugador.propiedades_compradas:
            if "Lineas" in propiedad.nombre:
                lineas += 1
        return lineas

    def calcular_alquiler_transporte(self, propietario, transporte):
        """Calcula el alquiler basado en cuántas líneas tiene el dueño"""
        lineas_propietario = self.contar_lineas_transporte(propietario)
        
        # Sistema de multiplicadores (como Monopoly real)
        multiplicadores = {
            1: 1,   # 1 línea: 25% del valor
            2: 2,   # 2 líneas: 50% del valor  
            3: 4,   # 3 líneas: 100% del valor
            4: 8    # 4 líneas: 200% del valor
        }
        
        multiplicador = multiplicadores.get(lineas_propietario, 1)
        alquiler_base = transporte.valor_propiedad // 4  # 25% del valor como base
        alquiler_final = alquiler_base * multiplicador
        
        return alquiler_final
    


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
