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
    
    '''
    COSAS QUE FALTAN:
    -Construcción de casas ¬_¬
    -Sistema de bancarrota
    -Valor neto

    cuando esto se solucione se debe agregar la interfaz
    '''

    def siguiente_turno(self):
        if not self.jugadores:
            print("❌ No hay jugadores")
            return None
        
        jugador = self.jugadores[self.turno_actual]

        # genera muchos =
        print(f"\n{'='*50}")
        print(f"🎯 RONDA {self.ronda} - TURNO DE {jugador.nombre.upper()}")
        print(f"💰 Dinero: ${jugador.dinero}")
        #revisa si está en la carcel
        if jugador.en_carcel:
            print(f"🔒 {jugador.nombre} está en la cárcel")
            movimiento = self.procesar_turno_carcel(jugador)

            #revisa si ya terminó la condena 
            if movimiento and not jugador.en_carcel:
                nueva_pos = self.tablero.mover_jugador(jugador, movimiento)
                nueva_casilla = self.tablero.casillas[nueva_pos]
                print(f"🔄 Movió a: {nueva_casilla.nombre}")
                self.procesar_casilla(jugador, nueva_casilla, movimiento)    
        else:
            # mostrar posición actual
            casilla_actual = self.tablero.casillas[jugador.posicion]
            print(f"📍 Posición actual: {casilla_actual.nombre}")

            # tirar dados y mover
            dados = self.tirar_dados()
            nueva_pos = self.tablero.mover_jugador(jugador, dados)
            nueva_casilla = self.tablero.casillas[nueva_pos]
        
            print(f"🔄 Movió a: {nueva_casilla.nombre}")

            #### en esta parte se tiene que crear la jugabilidad ####
            self.procesar_casilla(jugador, nueva_casilla, dados)

        # prepara el siguiente turno
        self.turno_actual = (self.turno_actual + 1) % len(self.jugadores)
        if self.turno_actual == 0:  # nueva ronda
            self.ronda += 1
                
        return jugador
    
    def procesar_subasta(self, jugador_actual):
        """Maneja el sistema de subastas/intercambios cuando un jugador cae en Subasta"""
        print(f"🏛️  ¡SUBASTA! - Turno de {jugador_actual.nombre}")
        print("Se abre el mercado de propiedades...")
        
        # Verificar si tiene propiedades para ofrecer
        if not jugador_actual.propiedades_compradas:
            print(f"❌ {jugador_actual.nombre} no tiene propiedades para ofrecer")
            return
        
        # Jugador actual selecciona una propiedad para ofrecer
        print(f"\n📦 PROPIEDADES DE {jugador_actual.nombre}:")
        for i, prop in enumerate(jugador_actual.propiedades_compradas, 1):
            print(f"   {i}. {prop.nombre} - Valor: ${prop.valor_propiedad}")
        
        while True:
            try:
                eleccion = int(input("Selecciona una propiedad para ofrecer (número): "))
                if 1 <= eleccion <= len(jugador_actual.propiedades_compradas):
                    propiedad_ofrecida = jugador_actual.propiedades_compradas[eleccion - 1]
                    break
                else:
                    print("❌ Selección inválida")
            except ValueError:
                print("❌ Ingresa un número válido")
        
        print(f"✅ Ofreciendo: {propiedad_ofrecida.nombre}")

        # Otros jugadores ofrecen
        ofertas = []
        for jugador in self.jugadores:
            if jugador != jugador_actual and jugador.propiedades_compradas:
                print(f"\n🔄 Turno de {jugador.nombre} para ofrecer:")
                print("Propiedades disponibles:")
                for i, prop in enumerate(jugador.propiedades_compradas, 1):
                    print(f"   {i}. {prop.nombre} - Valor: ${prop.valor_propiedad}")
                
                # Preguntar si quiere ofertar
                respuesta = input("¿Quieres hacer una oferta? (s/n): ")
                if respuesta.lower() == 's':
                    while True:
                        try:
                            eleccion = int(input("Selecciona propiedad para ofertar: "))
                            if 1 <= eleccion <= len(jugador.propiedades_compradas):
                                propiedad_ofertada = jugador.propiedades_compradas[eleccion - 1]
                                ofertas.append({
                                    'jugador': jugador,
                                    'propiedad': propiedad_ofertada,
                                    'valor': propiedad_ofertada.valor_propiedad
                                })
                                print(f"✅ {jugador.nombre} ofrece: {propiedad_ofertada.nombre}")
                                break
                            else:
                                print("❌ Selección inválida")
                        except ValueError:
                            print("❌ Ingresa un número válido")
        
    # Mostrar ofertas
        if not ofertas:
            print("❌ Nadie hizo ofertas. Subasta cancelada.")
            return
        
        print(f"\n🎯 OFERTAS RECIBIDAS por {propiedad_ofrecida.nombre}:")
        for i, oferta in enumerate(ofertas, 1):
            print(f"   {i}. {oferta['jugador'].nombre} ofrece: {oferta['propiedad'].nombre} (${oferta['valor']})")


        #el jugador elije
        print(f"\n🤔 {jugador_actual.nombre}, elige la oferta que prefieres:")
        for i, oferta in enumerate(ofertas, 1):
            print(f"   {i}. Aceptar {oferta['propiedad'].nombre} de {oferta['jugador'].nombre}")
        print(f"   {len(ofertas) + 1}. Rechazar todas las ofertas")
        
        while True:
            try:
                eleccion = int(input("Tu elección: "))
                if 1 <= eleccion <= len(ofertas):
                    # Aceptar oferta seleccionada
                    oferta_aceptada = ofertas[eleccion - 1]
                    self.ejecutar_intercambio(jugador_actual, propiedad_ofrecida, 
                                            oferta_aceptada['jugador'], oferta_aceptada['propiedad'])
                    break
                elif eleccion == len(ofertas) + 1:
                    print("❌ Subasta cancelada - No se aceptó ninguna oferta")
                    break
                else:
                    print("❌ Opción inválida")
            except ValueError:
                print("❌ Ingresa un número válido")

    def procesar_casilla(self, jugador, casilla, dados):
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

            elif "Compañía" in casilla.nombre:
                self.procesar_servicio(jugador, casilla, dados)

            elif casilla.nombre == "Carcel":
                self.mandar_a_la_carcel(jugador)

            elif casilla.nombre == "Subasta":  # ✅ NUEVO: Sistema de subastas
                self.procesar_subasta(jugador)
            # Aquí después agregarás impuestos, suerte, etc. procesar_casilla_especial

    def verificar_monopolio(self, jugador, color):
        #Verifica si un jugador tiene monopolio de un color"""
        propiedades_del_color = [prop for prop in jugador.propiedades_compradas 
                            if prop.color == color]
        
        # Contar cuántas propiedades hay de ese color en el tablero
        total_propiedades_color = len([casilla for casilla in self.tablero.casillas 
                                    if hasattr(casilla, 'color') and casilla.color == color])
        
        if len(propiedades_del_color) == total_propiedades_color:
            print(f"🎉 ¡{jugador.nombre} consiguió el MONOPOLIO de propiedades {color}!")
            print(f"   El alquiler de estas propiedades se duplicará")
            return True
        return False

    def calcular_alquiler_monopolio(self, propiedad):
        """Calcula el alquiler considerando el monopolio"""
        alquiler_base = propiedad.valor_alquiler
        
        if propiedad.propietario:
            # Verificar si el dueño tiene monopolio de este color
            propiedades_mismo_color = [prop for prop in propiedad.propietario.propiedades_compradas 
                                    if prop.color == propiedad.color]
            
            # Contar total de propiedades de este color en el tablero
            total_propiedades_color = len([casilla for casilla in self.tablero.casillas 
                                        if hasattr(casilla, 'color') and casilla.color == propiedad.color])
            
            # Si tiene todas las propiedades del mismo color → MONOPOLIO
            if len(propiedades_mismo_color) == total_propiedades_color:
                alquiler_final = alquiler_base * 2  # Duplicar alquiler
                print(f"   ⚡ MONOPOLIO {propiedad.color} → Alquiler duplicado: ${alquiler_base} → ${alquiler_final}")
                return alquiler_final
        
        # Si no hay monopolio, alquiler normal
        return alquiler_base

    def contar_propiedades_por_color(self, jugador, color):
        """Cuenta cuántas propiedades tiene un jugador de un color específico"""
        return len([prop for prop in jugador.propiedades_compradas 
                if prop.color == color])
        
    def ejecutar_intercambio(self, jugador1, prop1, jugador2, prop2):
    #jecuta el intercambio de propiedades entre dos jugadores"""
        print(f"\n🔄 EJECUTANDO INTERCAMBIO:")
        print(f"   {jugador1.nombre} da: {prop1.nombre}")
        print(f"   {jugador2.nombre} da: {prop2.nombre}")
        
        # Remover propiedades de los jugadores
        jugador1.propiedades_compradas.remove(prop1)
        jugador2.propiedades_compradas.remove(prop2)
        
        # Cambiar propietarios
        prop1.propietario = jugador2
        prop2.propietario = jugador1
        
        # Agregar propiedades a los nuevos dueños
        jugador1.propiedades_compradas.append(prop2)
        jugador2.propiedades_compradas.append(prop1)

        bonificacion = 200
        jugador1.dinero += bonificacion
        jugador2.dinero += bonificacion
        
        print(f"✅ Intercambio exitoso!")
        print(f"   {jugador1.nombre} ahora tiene: {prop2.nombre}")
        print(f"   {jugador2.nombre} ahora tiene: {prop1.nombre}")
        print(f"😎😎😎¡Ambos reciben 200!😎😎😎")

    def mandar_a_la_carcel(self, jugador):
        posicion_carcel = None
        for i, casilla in enumerate(self.tablero.casillas):
            if casilla.nombre == "Carcel":
                posicion_carcel = i
                break

        if posicion_carcel is not None:
            jugador.posicion = posicion_carcel
            jugador.en_carcel = True
            jugador.turnos_en_carcel = 0
            print(f"🔒 {jugador.nombre} fue llevado a la cárcel")
        else:
            print("❌ Error: No se encontró la casilla de Cárcel")

    def procesar_turno_carcel(self, jugador):
    #Maneja el turno de un jugador que está en la cárcel"""
        print(f"🔒 {jugador.nombre} está en la cárcel (turno {jugador.turnos_en_carcel + 1}/3)")
        
        opciones = []
        
        # Opción 1: Pagar fianza ($50)
        opciones.append("Pagar fianza de $50")
        
        # Opción 2: Tirar dados para dobles
        opciones.append("Tirar dados para conseguir dobles")
        
        # Opción 3: Usar carta de libertad (si tiene)
        if jugador.cartas_libertad > 0:
            opciones.append(f"Usar carta de salir de la cárcel gratis ({jugador.cartas_libertad} disponibles)")
        
        # Mostrar opciones
        print("Opciones:")
        for i, opcion in enumerate(opciones, 1):
            print(f"   {i}. {opcion}")
        
        # Elegir opción
        while True:
            try:
                eleccion = int(input("Elige una opción: "))
                if 1 <= eleccion <= len(opciones):
                    break
                else:
                    print("❌ Opción inválida")
            except ValueError:
                print("❌ Ingresa un número válido")
        
        movimiento = False
        
        # Procesar elección
        if eleccion == 1:  # Pagar fianza
            if jugador.dinero >= 50:
                jugador.dinero -= 50
                jugador.en_carcel = False
                jugador.turnos_en_carcel = 0
                print(f"✅ {jugador.nombre} pagó $50 de fianza y sale de la cárcel")
            else:
                print(f"❌ {jugador.nombre} no tiene $50 para pagar la fianza")
        
        elif eleccion == 2:  # Tirar dados
            dado1 = random.randint(1, 6)
            dado2 = random.randint(1, 6)
            total = dado1 + dado2
            print(f"🎲 Dados: {dado1} + {dado2} = {total}")
            
            if dado1 == dado2:
                jugador.en_carcel = False
                jugador.turnos_en_carcel = 0
                print(f"🎯 ¡Dobles! {jugador.nombre} sale de la cárcel")
                movimiento = total  # Retorna el movimiento para que el jugador se mueva
            else:
                jugador.turnos_en_carcel += 1
                print(f"❌ No salieron dobles. Te quedan {3 - jugador.turnos_en_carcel} intentos")
        
        elif eleccion == 3 and jugador.cartas_libertad > 0:  # Usar carta
            jugador.cartas_libertad -= 1
            jugador.en_carcel = False
            jugador.turnos_en_carcel = 0
            print(f"🎫 {jugador.nombre} usa carta de salir de la cárcel gratis")
        
        # Verificar si lleva 3 turnos en cárcel (obligatorio salir)
        if jugador.en_carcel and jugador.turnos_en_carcel >= 3:
            print(f"⏰ {jugador.nombre} lleva 3 turnos en cárcel. Debe pagar $50 para salir")
            if jugador.dinero >= 50:
                jugador.dinero -= 50
                jugador.en_carcel = False
                jugador.turnos_en_carcel = 0
                print(f"✅ {jugador.nombre} paga $50 y sale de la cárcel")
            else:
                print(f"❌ {jugador.nombre} no tiene dinero. Permanece en cárcel")
        
        return movimiento

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
        #Calcula el alquiler basado en cuántas líneas tiene el dueño"""
        lineas_propietario = self.contar_lineas_transporte(propietario)
        
        # ✅ NUEVO SISTEMA: Alquiler base + $50 por cada línea adicional
        alquiler_base = 50  # $50 de base por la primera línea
        
        # Cada línea adicional suma $50 al alquiler
        alquiler_final = alquiler_base + (50 * (lineas_propietario - 1))
        
        print(f"   📊 Dueño tiene {lineas_propietario} líneas → Alquiler: ${alquiler_final}")
            
        return alquiler_final
    
    def procesar_servicio(self, jugador, servicio, dados):
        #Procesa las compañías de servicios (luz y agua)"""
        # Asignar valor por defecto si de alguna manera no existe
        if not hasattr(servicio, 'valor_propiedad') or servicio.valor_propiedad == 0:
            servicio.valor_propiedad = 150
            
        if servicio.propietario is None:
            # Ofrecer compra
            if jugador.dinero >= servicio.valor_propiedad:
                respuesta = input(f"¿Quieres comprar {servicio.nombre} por ${servicio.valor_propiedad}? (s/n): ")
                if respuesta.lower() == 's':
                    servicio.propietario = jugador
                    jugador.dinero -= servicio.valor_propiedad
                    jugador.propiedades_compradas.append(servicio)
                    print(f"✅ {jugador.nombre} compró {servicio.nombre}")
                    
                    servicios_actuales = self.contar_servicios(jugador)
                    print(f"   🎯 Ahora tienes {servicios_actuales} servicios")
                    if servicios_actuales == 2:
                        print(f"   ⚡ ¡Tienes el monopolio de servicios!")
                else:
                    print(f"❌ {jugador.nombre} decidió no comprar {servicio.nombre}")
            else:
                print(f"❌ {jugador.nombre} no tiene suficiente dinero para {servicio.nombre}")
        else:
            # Pagar por uso - depende de los dados y cuántos servicios tenga el dueño
            if servicio.propietario != jugador:
                pago = self.calcular_pago_servicio(servicio.propietario, dados)
                jugador.dinero -= pago
                servicio.propietario.dinero += pago
                
                servicios_propietario = self.contar_servicios(servicio.propietario)
                print(f"💡 {jugador.nombre} paga ${pago} por uso de {servicio.nombre}")
                print(f"   📊 {servicio.propietario.nombre} tiene {servicios_propietario} servicios")

    def contar_servicios(self, jugador):
        #Cuenta cuántas compañías de servicios tiene un jugador"""
        servicios = 0
        for propiedad in jugador.propiedades_compradas:
            if "Compañía" in propiedad.nombre:
                servicios += 1
        return servicios
    
    def calcular_pago_servicio(self, propietario, dados):
        #Calcula el pago por uso de servicios usando los dados originales"""
        servicios_propietario = self.contar_servicios(propietario)
        
        print(f"🎲 Usando dados del movimiento: {dados}")
        
        # Multiplicador según cuántos servicios tiene el dueño
        if servicios_propietario == 1:
            multiplicador = 4   # 1 servicio: 4x dados
        else:  # 2 servicios (monopolio)
            multiplicador = 10  # 2 servicios: 10x dados
        
        pago = dados * multiplicador
        
        print(f"   📊 Dueño tiene {servicios_propietario} servicios → Multiplicador: x{multiplicador}")
        
        return pago

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
                    # verifiva monopolio
                    self.verificar_monopolio(jugador, propiedad.color)
                else:
                    print(f"❌ {jugador.nombre} decidió no comprar {propiedad.nombre}")
            else:
                print(f"❌ {jugador.nombre} no tiene suficiente dinero para comprar {propiedad.nombre}")
        else:
            # Pagar alquiler
            if propiedad.propietario != jugador:
                alquiler = self.calcular_alquiler_monopolio(propiedad)
                jugador.dinero -= alquiler
                propiedad.propietario.dinero += alquiler
                print(f"💰 {jugador.nombre} paga ${alquiler} de alquiler a {propiedad.propietario.nombre}")

    def mostrar_estado(self):
        print(f"\n📊 ESTADO GENERAL - Ronda {self.ronda}")
        for jugador in self.jugadores:
            casilla = self.tablero.casillas[jugador.posicion]
            estado_carcel = " (ENCARCELADO)" if jugador.en_carcel else ""
            cartas = f" | Cartas libertad: {jugador.cartas_libertad}" if jugador.cartas_libertad > 0 else ""

            monopolios = self.obtener_monopolios(jugador)
            monopolios_str = f" | Monopolios: {', '.join(monopolios)}" if monopolios else ""
            print(f"   {jugador.nombre}: ${jugador.dinero} | Pos: {casilla.nombre}{estado_carcel}{cartas}{monopolios_str}")
        
    def obtener_monopolios(self, jugador):
        """Obtiene la lista de colores donde el jugador tiene monopolio"""
        monopolios = []
        colores_revisados = set()
        
        for propiedad in jugador.propiedades_compradas:
            if hasattr(propiedad, 'color') and propiedad.color not in colores_revisados:
                colores_revisados.add(propiedad.color)
                
                # Verificar si tiene monopolio de este color
                propiedades_color = [prop for prop in jugador.propiedades_compradas 
                                if prop.color == propiedad.color]
                
                total_en_tablero = len([casilla for casilla in self.tablero.casillas 
                                    if hasattr(casilla, 'color') and casilla.color == propiedad.color])
                
                if len(propiedades_color) == total_en_tablero:
                    monopolios.append(propiedad.color)
        
        return monopolios

    
# Función de prueba
def probar_sistema_turnos():
    juego = Juego()
    
    
    #elige la cantiadad de turnos
    turnos=int(input("Cantidad de turnos: "))

    for i in range(2):
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
