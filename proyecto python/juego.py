import random
#traer los archivos anteriores
from seteador import cargar_tablero_completo
from objetos import Jugador
porcentaje_para_ganar = 2
#cuando unjugador duplica el valor neto de los demas gana

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
    -Sistema de bancarrota
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

        #pregunta si quiere construir casa
        if  not jugador.en_carcel:
            monopolios = self.obtener_monopolios(jugador)
            if monopolios:
                print(f"🎯 Tienes monopolios: {', '.join(monopolios)}")
                respuesta = input("¿Quieres construir casas antes de mover? (s/n): ")
                if respuesta.lower() == 's':
                    self.construir_casas(jugador)

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

        #  VERIFICAR SI HAY GANADOR DESPUÉS DEL TURNO
        ganador = self.verificar_ganador()
        if ganador:
            print(f"\n{'='*60}")
            print(f"🎉 ¡¡¡{ganador.nombre} ES EL GANADOR!!!")
            print(f"💰 Valor neto final: ${self.calcular_valor_neto(ganador)}")
            self.mostrar_detalle_completo(ganador)
            print(f"{'='*60}")
            return ganador  # Retorna al ganador para que el juego sepa que terminó


        # prepara el siguiente turno
        self.turno_actual = (self.turno_actual + 1) % len(self.jugadores)
        if self.turno_actual == 0:  # nueva ronda
            self.ronda += 1
                
        return jugador
    
    def calcular_valor_neto(self, jugador):
        """Calcula el valor neto simple: dinero + propiedades + casas"""
        valor_total = jugador.dinero  # Dinero en efectivo
        
        # Sumar valor de todas las propiedades y casas
        for propiedad in jugador.propiedades_compradas:
            # Valor base de la propiedad
            valor_total += propiedad.valor_propiedad
            
            # Valor de las casas construidas
            if hasattr(propiedad, 'cantidad_casas') and propiedad.cantidad_casas > 0:
                valor_total += propiedad.valor_casa * propiedad.cantidad_casas
        
        return valor_total

    def mostrar_valor_neto(self, jugador=None):
        """Muestra el valor neto de un jugador específico o de todos"""
        if jugador:
            # Mostrar valor neto de un jugador específico
            valor_neto = self.calcular_valor_neto(jugador)
            print(f"\n💰 VALOR NETO DE {jugador.nombre.upper()}: ${valor_neto}")
            
            # Desglose simple
            print(f"   💵 Dinero: ${jugador.dinero}")
            
            valor_propiedades = sum(prop.valor_propiedad for prop in jugador.propiedades_compradas)
            print(f"   🏠 Propiedades: ${valor_propiedades}")
            
            valor_casas = sum(prop.valor_casa * prop.cantidad_casas for prop in jugador.propiedades_compradas)
            if valor_casas > 0:
                print(f"   🏗️  Casas: ${valor_casas}")
            
        else:
            # Mostrar ranking de todos los jugadores
            print(f"\n🏆 RANKING - Ronda {self.ronda}")
            
            jugadores_ordenados = sorted(self.jugadores, 
                                    key=lambda j: self.calcular_valor_neto(j), 
                                    reverse=True)
            
            for i, jugador in enumerate(jugadores_ordenados, 1):
                valor_neto = self.calcular_valor_neto(jugador)
                emoji = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "  "
                print(f"   {emoji} {i}. {jugador.nombre}: ${valor_neto}")

    def mostrar_detalle_completo(self, jugador):
        """Muestra un desglose completo pero simple"""
        valor_neto = self.calcular_valor_neto(jugador)
        
        print(f"\n📈 {jugador.nombre.upper()} - Valor Neto: ${valor_neto}")
        print(f"   💵 Dinero actual: ${jugador.dinero}")
        
        if jugador.propiedades_compradas:
            print(f"   🏠 Propiedades:")
            for propiedad in jugador.propiedades_compradas:
                valor_prop = propiedad.valor_propiedad
                valor_casas = propiedad.valor_casa * propiedad.cantidad_casas
                total_prop = valor_prop + valor_casas
                
                casas_info = f" + {propiedad.cantidad_casas} casas (${valor_casas})" if propiedad.cantidad_casas > 0 else ""
                print(f"      • {propiedad.nombre}: ${valor_prop}{casas_info} = ${total_prop}")

    def construir_casas(self, jugador):
        """Permite a un jugador construir casas en sus propiedades SOLO con monopolio"""
        print(f"🏗️  CONSTRUCCIÓN DE CASAS - Turno de {jugador.nombre}")
        
        # ✅ FILTRAR SOLO propiedades donde TIENE MONOPOLIO
        propiedades_construibles = []
        for propiedad in jugador.propiedades_compradas:
            if (hasattr(propiedad, 'color') and 
                self.tiene_monopolio(jugador, propiedad.color) and
                hasattr(propiedad, 'valor_casa') and 
                propiedad.valor_casa > 0):  # ✅ Verificar que tenga costo de casa
                propiedades_construibles.append(propiedad)
        
        if not propiedades_construibles:
            print("❌ No tienes monopolios completos para construir casas")
            print("   Necesitas todas las propiedades de un mismo color")
            return
        
        print("📋 Propiedades donde puedes construir (con monopolio):")
        for i, prop in enumerate(propiedades_construibles, 1):
            estado = f"{prop.cantidad_casas} casas" if prop.cantidad_casas > 0 else "Sin casas"
            print(f"   {i}. {prop.nombre} ({prop.color}) - {estado} - Costo casa: ${prop.valor_casa}")
        
        while True:
            try:
                eleccion = int(input("Selecciona propiedad para construir (0 para cancelar): "))
                if eleccion == 0:
                    print("❌ Construcción cancelada")
                    return
                elif 1 <= eleccion <= len(propiedades_construibles):
                    propiedad_seleccionada = propiedades_construibles[eleccion - 1]
                    self.construir_en_propiedad(jugador, propiedad_seleccionada)
                    break
                else:
                    print("❌ Selección inválida")
            except ValueError:
                print("❌ Ingresa un número válido")
                
    def construir_en_propiedad(self, jugador, propiedad):
        """Construye una casa en una propiedad específica"""
        if not hasattr(propiedad, 'valor_casa') or propiedad.valor_casa <= 0:
                print("❌ Esta propiedad no permite construcción de casas")
                return

        if propiedad.cantidad_casas >= 4:
            print("❌ Ya tienes el máximo de 4 casas en esta propiedad")
            return
        
        costo_casa = propiedad.valor_casa
        if jugador.dinero < costo_casa:
            print(f"❌ No tienes suficiente dinero. Necesitas ${costo_casa}, tienes ${jugador.dinero}")
            return
        
        # Verificar construcción equilibrada (no más de 1 casa de diferencia entre propiedades del mismo color)
        if not self.verificar_construccion_equilibrada(jugador, propiedad):
            print("❌ Primero debes construir casas en las otras propiedades del mismo color")
            return
        
        # Construir la casa
        jugador.dinero -= costo_casa
        propiedad.cantidad_casas += 1
        
        print(f"✅ ¡{jugador.nombre} construyó una casa en {propiedad.nombre}!")
        print(f"   💰 Costo: ${costo_casa}")
        print(f"   🏠 Casas en {propiedad.nombre}: {propiedad.cantidad_casas}/4")
        print(f"   💰 Dinero restante: ${jugador.dinero}")
        
        # Mostrar nuevo alquiler
        nuevo_alquiler = self.calcular_alquiler_actualizado(propiedad)
        print(f"   📈 Nuevo alquiler: ${nuevo_alquiler}")

    def verificar_construccion_equilibrada(self, jugador, propiedad):
        """Verifica que la construcción sea equilibrada entre propiedades del mismo color"""
        propiedades_mismo_color = [prop for prop in jugador.propiedades_compradas 
                                if prop.color == propiedad.color]
        
        # Encontrar la propiedad con menos casas del mismo color
        min_casas = min(prop.cantidad_casas for prop in propiedades_mismo_color)
        
        # No permitir más de 1 casa de diferencia
        if propiedad.cantidad_casas > min_casas:
            return False
        
        return True

    def tiene_monopolio(self, jugador, color):
            #Verifica si un jugador tiene monopolio de un color"""
        if not color:  # Si la propiedad no tiene color
            return False
        
        propiedades_del_color = [prop for prop in jugador.propiedades_compradas 
                            if hasattr(prop, 'color') and prop.color == color]
        
        total_propiedades_color = len([casilla for casilla in self.tablero.casillas 
                                    if hasattr(casilla, 'color') and casilla.color == color])
        
        return len(propiedades_del_color) == total_propiedades_color and total_propiedades_color > 0   
 
    def calcular_alquiler_actualizado(self, propiedad):
        """Calcula el alquiler actualizado basado en casas construidas"""
        alquiler_base = propiedad.valor_alquiler
        
        # Tabla de multiplicadores según cantidad de casas
        multiplicadores = {
            0: 1,   # Sin casas (pero con monopolio)
            1: 5,   # 1 casa
            2: 15,  # 2 casas  
            3: 40,  # 3 casas
            4: 80   # 4 casas (hotel)
        }
        
        return alquiler_base * multiplicadores.get(propiedad.cantidad_casas, 1)

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

            if casilla.nombre == "Impuesto Medio" or casilla.nombre == "Impuesto rompeojete somos comunistas oligarca sorete":
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
        """Calcula el alquiler considerando monopolio y casas construidas"""
        if propiedad.cantidad_casas > 0:
            # Si tiene casas, usar el sistema de casas
            return self.calcular_alquiler_actualizado(propiedad)
        
        # Si no tiene casas pero tiene monopolio, duplicar alquiler base
        if propiedad.propietario and self.tiene_monopolio(propiedad.propietario, propiedad.color):
            alquiler_base = propiedad.valor_alquiler
            alquiler_final = alquiler_base * 2
            print(f"   ⚡ MONOPOLIO {propiedad.color} → Alquiler duplicado: ${alquiler_base} → ${alquiler_final}")
            return alquiler_final
        
        # Alquiler normal (sin monopolio ni casas)
        return propiedad.valor_alquiler

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
        #Cartas de suerte mejoradas con ideas temáticas"""
        cartas = [
            # Cartas MALAS (M)
            {"texto": "Subieron los impuestos", "monto": -100, "tipo": "dinero", "clase": "M"},
            {"texto": "Se te acusó de fraude - Vas a la cárcel", "monto": 0, "tipo": "ir_carcel", "clase": "M"},
            {"texto": "Pediste un préstamo y no lo pagaste a tiempo - Intereses", "monto": -150, "tipo": "dinero", "clase": "M"},
            {"texto": "Tus compañeros te pidieron dinero", "monto": 0, "tipo": "dar_jugadores", "clase": "M"},
            {"texto": "Tomaste el bondi equivocado - Retrocedes 3 casilleros", "monto": 0, "tipo": "retroceder", "clase": "M"},
            {"texto": "Te paró tránsito - Perdés un turno", "monto": 0, "tipo": "perder_turno", "clase": "M"},
            {"texto": "Perdiste la billetera", "monto": -40, "tipo": "dinero", "clase": "M"},
            {"texto": "Cayó mercado pago - Todos pierden $100", "monto": 0, "tipo": "todos_pierden", "clase": "M"},
            {"texto": "Pagás impuesto a la ganancia", "monto": -100, "tipo": "dinero", "clase": "M"},
            {"texto": "Te multan por exceso de velocidad", "monto": -200, "tipo": "multa_carcel", "clase": "M"},
            
            # Cartas BUENAS (B)
            {"texto": "Ganaste la lotería", "monto": 150, "tipo": "dinero", "clase": "B"},
            {"texto": "Se comprobó tu inocencia - Salir de la cárcel gratis", "monto": 0, "tipo": "carcel", "clase": "B"},
            {"texto": "Ganaste un sorteo del banco", "monto": 100, "tipo": "dinero", "clase": "B"},
            {"texto": "Es tu cumpleaños - Cada jugador te da $50", "monto": 0, "tipo": "cobrar_jugadores", "clase": "B"},
            {"texto": "Visita al presidente - Vas hasta Olivos", "monto": 0, "tipo": "mover_olivos", "clase": "B"},
            {"texto": "Ganaste la rifa del día del padre", "monto": 50, "tipo": "dinero", "clase": "B"},
            {"texto": "Día del empleado municipal - Ganás 1 turno", "monto": 0, "tipo": "ganar_turno", "clase": "B"},
            {"texto": "Error bancario - Todos ganan $100", "monto": 0, "tipo": "todos_ganan", "clase": "B"},
            {"texto": "Argentina gana el mundial - Feriado nacional - Ganás un turno", "monto": 0, "tipo": "ganar_turno", "clase": "B"},
            {"texto": "Recibiste una transferencia equivocada", "monto": 200, "tipo": "dinero", "clase": "B"}
        ]
        
        carta = random.choice(cartas)
        emoji = "😊" if carta['clase'] == "B" else "😞"
        print(f"🎁 CARTA DE SUERTE: {carta['texto']} {emoji}")
        
        # Procesar según el tipo de carta
        if carta['tipo'] == "dinero":
            jugador.dinero += carta["monto"]
            if carta["monto"] > 0:
                print(f"   💰 +${carta['monto']} | Dinero actual: ${jugador.dinero}")
            else:
                print(f"   💸 ${carta['monto']} | Dinero actual: ${jugador.dinero}")
        
        elif carta['tipo'] == "carcel":
            jugador.cartas_libertad += 1
            print(f"   🎫 Obtienes una carta de 'Salir de la cárcel gratis'")
            print(f"   📬 Cartas de libertad: {jugador.cartas_libertad}")
        
        elif carta['tipo'] == "ir_carcel":
            self.mandar_a_la_carcel(jugador)
            print(f"   🔒 Fuiste enviado a la cárcel por fraude")
        
        elif carta['tipo'] == "dar_jugadores":
            pago_por_jugador = 20
            total_pagado = 0
            
            for otro_jugador in self.jugadores:
                if otro_jugador != jugador:
                    if jugador.dinero >= pago_por_jugador:
                        jugador.dinero -= pago_por_jugador
                        otro_jugador.dinero += pago_por_jugador
                        total_pagado += pago_por_jugador
                        print(f"   💸 Das ${pago_por_jugador} a {otro_jugador.nombre}")
                    else:
                        print(f"   ❌ No tienes para darle a {otro_jugador.nombre}")
            
            if total_pagado > 0:
                print(f"   📤 Total dado: ${total_pagado}")
                print(f"   💰 Dinero actual: ${jugador.dinero}")
        
        elif carta['tipo'] == "retroceder":
            nueva_posicion = (jugador.posicion - 3) % len(self.tablero.casillas)
            jugador.posicion = nueva_posicion
            print(f"   🔙 Retrocedes 3 casillas a: {self.tablero.casillas[nueva_posicion].nombre}")
            # Procesar la casilla donde cayó
            self.procesar_casilla(jugador, self.tablero.casillas[nueva_posicion], 0)
        
        elif carta['tipo'] == "perder_turno":
            jugador.en_carcel = True
            jugador.turnos_en_carcel = 0
            print(f"   🚓 Te paró tránsito - Pierdes un turno")
        
        elif carta['tipo'] == "cobrar_jugadores":
            pago_por_jugador = 50
            total_cobrado = 0
            
            for otro_jugador in self.jugadores:
                if otro_jugador != jugador and otro_jugador.dinero >= pago_por_jugador:
                    otro_jugador.dinero -= pago_por_jugador
                    total_cobrado += pago_por_jugador
                    print(f"   💵 {otro_jugador.nombre} te da ${pago_por_jugador}")
            
            if total_cobrado > 0:
                jugador.dinero += total_cobrado
                print(f"   🎊 Total recibido: +${total_cobrado}")
                print(f"   💰 Dinero actual: ${jugador.dinero}")
            else:
                print(f"   😞 Nadie tenía dinero para darte")
        
        elif carta['tipo'] == "mover_olivos":
            # Buscar la casilla "Olivos" o "Vicente Lopez" como alternativa
            posicion_olivos = None
            for i, casilla in enumerate(self.tablero.casillas):
                if "Olivos" in casilla.nombre or "Vicente Lopez" in casilla.nombre:
                    posicion_olivos = i
                    break
            
            if posicion_olivos is not None:
                # Verificar si pasa por el inicio
                pos_actual = jugador.posicion
                if posicion_olivos < pos_actual:
                    jugador.dinero += 200
                    print(f"   💰 +$200 por pasar por el inicio")
                
                jugador.posicion = posicion_olivos
                print(f"   🏛️  Visitas al presidente en: {self.tablero.casillas[posicion_olivos].nombre}")
                self.procesar_casilla(jugador, self.tablero.casillas[posicion_olivos], 0)
            else:
                print(f"   ❌ No se encontró la casilla Olivos")
        
        elif carta['tipo'] == "ganar_turno":
            # El jugador juega otra vez - simplemente no avanzamos el turno
            self.turno_actual = (self.turno_actual - 1) % len(self.jugadores)
            print(f"   ⭐ Ganas un turno extra - ¡Juegas otra vez!")
        
        elif carta['tipo'] == "todos_ganan":
            for j in self.jugadores:
                j.dinero += 100
                print(f"   💰 {j.nombre} recibe +$100")
            print(f"   🎉 Error bancario - ¡Todos ganan $100!")
        
        elif carta['tipo'] == "todos_pierden":
            for j in self.jugadores:
                if j.dinero >= 100:
                    j.dinero -= 100
                    print(f"   💸 {j.nombre} pierde $100")
                else:
                    print(f"   ❌ {j.nombre} no tiene $100 para perder")
            print(f"   📉 Cayó mercado pago - ¡Todos pierden $100!")
        
        elif carta['tipo'] == "multa_carcel":
            jugador.dinero -= 200
            print(f"   💸 Multa de -$200 por exceso de velocidad")
            print(f"   💰 Dinero actual: ${jugador.dinero}")
            self.mandar_a_la_carcel(jugador)
            print(f"   🔒 Además, vas a la cárcel")

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
            valor_neto = self.calcular_valor_neto(jugador)
            cartas = f" | Cartas libertad: {jugador.cartas_libertad}" if jugador.cartas_libertad > 0 else ""

             # Contar casas totales
            total_casas = sum(prop.cantidad_casas for prop in jugador.propiedades_compradas)
            casas_str = f" | Casas: {total_casas}" if total_casas > 0 else ""
            
            print(f"   {jugador.nombre}: ${jugador.dinero} | Neto: ${valor_neto} | Pos: {casilla.nombre}{estado_carcel}{casas_str}")
            
            # Mostrar propiedades con casas
            for prop in jugador.propiedades_compradas:
                if prop.cantidad_casas > 0:
                    print(f"      🏠 {prop.nombre}: {prop.cantidad_casas} casas - Alquiler: ${self.calcular_alquiler_actualizado(prop)}")
    
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
    
    def verificar_ganador(self):
        """Verifica si hay un ganador basado en valor neto"""
        if len(self.jugadores) < 2:
            return None
        
        # Ordenar jugadores por valor neto
        jugadores_ordenados = sorted(self.jugadores, 
                                key=lambda j: self.calcular_valor_neto(j), 
                                reverse=True)
        
        primer_lugar = jugadores_ordenados[0]
        segundo_lugar = jugadores_ordenados[1]
        
        valor_primer = self.calcular_valor_neto(primer_lugar)
        valor_segundo = self.calcular_valor_neto(segundo_lugar)
        
        # Ganador si tiene significativamente más valor neto
        if valor_primer >= valor_segundo * porcentaje_para_ganar:  # 50% más que el segundo
            return primer_lugar
        
        return None

    
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
        ganador = juego.verificar_ganador()
        if ganador:
            print(f"\n🎉 ¡¡¡{ganador.nombre} ES EL GANADOR!!!")
            print(f"💰 Valor neto final: ${juego.calcular_valor_neto(ganador)}")
            juego.mostrar_detalle_completo(ganador)
            break  # Terminar el juego si hay ganador
        
        # Mostrar ranking cada 2 rondas
        if juego.ronda % 2 == 0:
            juego.mostrar_valor_neto()
    
    # Si llegamos aquí sin break (sin ganador), mostrar resultado final
    if not juego.verificar_ganador():
        print(f"\nJUEGO COMPLETAD0 - {turnos} turnos por jugador")
        juego.mostrar_valor_neto()
        print("🤝 Nadie llegó al Límite - Juego terminado por límite de turnos")

if __name__ == "__main__":
    probar_sistema_turnos()
