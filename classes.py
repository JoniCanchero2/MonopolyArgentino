import random
import pygame
from seteador import ANCHO, ALTURA, ESPACIO, BORDE, TAMANO_FICHA, BLACK, FONDO_TABLERO_IMG
from suerte_cards import get_shuffled_suerte_deck 

class Player:
    """Representa a un jugador en el juego."""
    def __init__(self, id, nombre, dinero, posicion, color, ficha_img):
        self.id = id
        self.nombre = nombre
        self.dinero = dinero
        self.posicion = posicion
        self.color = color
        self.activo = True
        self.ficha_img = ficha_img
        self.turns_in_jail = 0
        self.extra_turn_count = 0 
        
        
    def move(self, roll):
        """Mueve al jugador y retorna si pasó por SALIDA."""
        old_pos = self.posicion
        self.posicion = (old_pos + roll) % 40
        return old_pos + roll > 39 
    
    def pay(self, amount):
        """Paga una cantidad de dinero."""
        self.dinero -= amount
        return self.dinero <= 0 # Retorna True si el jugador queda en bancarrota

    def receive_money(self, amount):
        """Recibe una cantidad de dinero."""
        self.dinero += amount


class Game:
    """Clase principal que gestiona el estado y la lógica del juego Monopoly."""
    def __init__(self, board_data, players_data, pantalla, fonts):
        self.board = board_data
        self.pantalla = pantalla
        
        # Importar constantes de settings
        self.ANCHO = ANCHO
        self.ALTURA = ALTURA
        self.TAMANO_FICHA = TAMANO_FICHA
        self.ESPACIO = ESPACIO
        self.BORDE = BORDE
        
        self.FONT, self.SMALL_FONT, self.TINY_FONT, self.STATUS_FONT = fonts
        
        # Inicializar jugadores 
        self.players = self._initialize_players(players_data) 
        
        self.current_turn_index = 0
        self.current_player = self.players[0]
        self.current_message = f"Turno de {self.current_player.nombre}. Presiona 'S' para tirar los dados."
        self.purchase_state = False
        self.interaction_done = False
        self.game_over = False
        
        # --- LÓGICA DE TARJETAS DE SUERTE ---
        self.suerte_deck = get_shuffled_suerte_deck() 
        self.suerte_discard = []                     
        self.current_card_message = ""               
        # ------------------------------------
        
        try:
            self.fondo_img = pygame.image.load(FONDO_TABLERO_IMG).convert()
            centro_ancho = self.ANCHO - 2 * self.ESPACIO
            self.fondo_img = pygame.transform.scale(self.fondo_img, (centro_ancho, centro_ancho))
        except pygame.error:
            print(f"Advertencia: No se pudo cargar {FONDO_TABLERO_IMG}. Usando fondo de color.")
            self.fondo_img = None
            
        self.current_turn_index = 0

    def _initialize_players(self, players_data):
        """Crea instancias de Player a partir de los datos iniciales y carga imágenes."""
        players = []
        for p_data in players_data:
            ficha_img = self._load_player_token(p_data["nombre"], p_data["color"])

            players.append(Player(
                p_data["id"], 
                p_data["nombre"], 
                p_data["dinero"], 
                p_data["posicion"], 
                p_data["color"], 
                ficha_img
            ))
        return players

    def _load_player_token(self, name, color):
        """Carga la imagen de la ficha o crea un sustituto de color."""
        try:
            token_name = name.split("(")[1].split(")")[0].lower()
            file_name = f"{token_name}.png"
            
            img = pygame.image.load(file_name).convert_alpha()
            ficha = pygame.transform.scale(img, self.TAMANO_FICHA)
            return ficha
        except:
            print(f"WARNING: no se encontró la imagen. Usando un cuadrado de color de reserva.")
            ficha = pygame.Surface(self.TAMANO_FICHA)
            ficha.fill(color)
            return ficha

    def roll_dice(self):
        """Simula la tirada de dados y aplica la lógica de la cárcel."""
        if self.game_over:
            self.current_message = "El juego ha terminado."
            return 0
        
        player = self.current_player
        dado1 = random.randint(1, 6)
        dado2 = random.randint(1, 6)
        roll = dado1 + dado2
        is_doubles = (dado1 == dado2)
        
        # 1. Lógica para salir de la cárcel (sin cambios)
        if player.turns_in_jail > 0:
            
            if is_doubles:
                self.current_message = f"Turno de {player.nombre}. ¡Dados: {dado1} + {dado2} (DOBLES)! Sale de la cárcel y avanza {roll}."
                player.turns_in_jail = 0 
                self.purchase_state = False
                return roll 
            
            elif player.turns_in_jail == 3:
                player.turns_in_jail = 0 
                bail = 50 
                
                if player.pay(bail):
                    self.handle_bankruptcy(player)
                    return 0 
                
                self.current_message = f"Turno de {player.nombre}. Fianza pagada: ${bail}. Avanza {roll}."
                self.purchase_state = False
                return roll 
                
            else:
                self.current_message = f"Turno de {player.nombre} (Cárcel, Turno {player.turns_in_jail}). Dados: {dado1} + {dado2}. ¡No hay dobles! Pierde el turno."
                player.turns_in_jail += 1
                self.interaction_done = True 
                return 0 
        
        # 2. Movimiento normal
        else:
            self.current_message = f"Turno de {player.nombre}. ¡Dados: {dado1} + {dado2} = {roll}!"
            self.purchase_state = False
            return roll

    def next_turn(self):
        """Pasa el turno al siguiente jugador activo, aplicando lógica de turno extra."""
        player = self.current_player
        
        # 1. Lógica de Turno Extra
        if player.extra_turn_count > 0:
            player.extra_turn_count -= 1
            self.current_message = f"¡EXTRA TURNO! {player.nombre} tira de nuevo. Presiona 'S' para tirar los dados."
            self.purchase_state = False
            self.interaction_done = False
            return 
            
        # 2. Chequear si el juego terminó
        jugadores_activos = [p for p in self.players if p.activo]
        if len(jugadores_activos) <= 1:
            self.game_over = True
            if len(jugadores_activos) == 1:
                self.current_message = f"¡{jugadores_activos[0].nombre} ha ganado el juego!"
            else:
                self.current_message = "¡Todos han quedado en bancarrota! Fin del juego."
            return

        # 3. Pasar al siguiente índice activo
        while True:
            self.current_turn_index = (self.current_turn_index + 1) % len(self.players)
            self.current_player = self.players[self.current_turn_index]
            
            if self.current_player.activo:
                self.current_message = f"Turno de {self.current_player.nombre}. Presiona 'S' para tirar los dados."
                self.purchase_state = False
                self.interaction_done = False 
                break
    
    def handle_bankruptcy(self, player):
        """Maneja la lógica de la bancarrota."""
        player.activo = False
        self.current_message = f"¡🚨 {player.nombre} ha quebrado y es ELIMINADO del juego! 🚨"
        
        # Las propiedades vuelven a ser sin dueño
        for i, casilla in enumerate(self.board):
            if casilla["propietario"] == player.id:
                self.board[i]["propietario"] = None
        
        player.dinero = 0
        # No llamamos next_turn aquí, se espera que el código llamador lo haga.

    # --- MÉTODOS DE TARJETAS DE SUERTE ---
    
    def _draw_suerte_card(self):
        """Saca una carta de Suerte del mazo, baraja si es necesario."""
        if not self.suerte_deck:
            self.suerte_deck = self.suerte_discard
            self.suerte_discard = []
            random.shuffle(self.suerte_deck)
            self.current_message += " (¡Mazo de Suerte barajado!)"

        if self.suerte_deck:
            card = self.suerte_deck.pop(0)
            self.suerte_discard.append(card)
            return card
        return None

    def process_suerte_card(self):
        """Saca una carta y aplica su efecto. Implementa las 19 tarjetas personalizadas."""
        player = self.current_player
        card = self._draw_suerte_card()

        if card is None:
            self.current_message += " (No hay cartas en el mazo de Suerte.)"
            self.interaction_done = True
            return

        self.current_card_message = card["mensaje"]
        self.current_message += f" 🃏 ¡Tarjeta SUERTE! **{card['mensaje']}**."

        action = card["accion"]
        value = card["valor"]
        tipo_movimiento = card["tipo_movimiento"]
        
        # Lógica de la tarjeta
        
        # Caso 1: Acción de Dinero directa
        if action == "money":
            if value > 0:
                player.receive_money(value)
            elif value < 0:
                if player.pay(abs(value)):
                    self.handle_bankruptcy(player)
                    return 
            self.interaction_done = True
        
        # Caso 2: Cobrar de otros jugadores (Cumpleaños - Card 6)
        elif action == "money_per_player":
            amount = value
            total_received = 0
            
            for other_player in self.players:
                if other_player.activo and other_player.id != player.id:
                    if other_player.pay(amount):
                        self.handle_bankruptcy(other_player)
                    else:
                        total_received += amount
            
            player.receive_money(total_received)
            self.current_message += f" ¡Recibiste **${total_received}** de los otros jugadores!"
            self.interaction_done = True
            
        # Caso 3: Pagar a otros jugadores (Compañeros piden plata - Card 7)
        elif action == "pay_per_player":
            amount = value
            active_opponents = [p for p in self.players if p.activo and p.id != player.id]
            total_paid = amount * len(active_opponents)
            
            if player.pay(total_paid):
                self.handle_bankruptcy(player)
                return 
            
            for other_player in active_opponents:
                other_player.receive_money(amount)
                
            self.current_message += f" Pagaste **${total_paid}** en total."
            self.interaction_done = True
            
        # Caso 4: Interacción de dinero para todos (Error bancario/Mercado Pago - Card 14/15)
        elif action == "money_all_interact":
            amount = value
            for p in self.players:
                if p.activo:
                    if amount > 0:
                        p.receive_money(amount)
                    elif amount < 0:
                        if p.pay(abs(amount)):
                            # La bancarrota se maneja dentro del loop, si el jugador actual quiebra, no se continúa.
                            self.handle_bankruptcy(p) 
                            if p.id == player.id: return 
                            
            self.current_message += f" **Todos** los jugadores fueron afectados con **${abs(amount)}**."
            self.interaction_done = True
            
        # Caso 5: Turno Extra (Card 13/17)
        elif action == "extra_turn":
            player.extra_turn_count += value
            self.current_message += " ¡Ganas un turno extra! Podrás tirar de nuevo."
            self.interaction_done = True 
            
        # Caso 6: Mensaje de perder turno (Card 10)
        elif action == "skip_turn_message":
            self.current_message += " El turno de dados del jugador ha finalizado."
            self.interaction_done = True

        # Caso 7: Acciones de Movimiento
        elif action == "move":
            
            if tipo_movimiento == "absolute_jail":
                # Card 3: Ir a la Cárcel
                player.posicion = value # Pos 10
                player.turns_in_jail = 1
                self.current_message += " 🚓 ¡Enviado a la Cárcel!."
                self.interaction_done = True
                
            elif tipo_movimiento == "absolute_pass_go":
                # Card 8: Ir a Olivos (Posición 39) con cobro
                target_pos = value # Pos 39
                
                if target_pos < player.posicion:
                    player.receive_money(200)
                    self.current_message += " 💸 Pasaste por Salida y cobraste $200."
                    
                player.posicion = target_pos
                self.current_message += f" 👣 Moviendo a {self.board[target_pos]['nombre']}."
                self.interaction_done = True 
                
            elif tipo_movimiento == "relative":
                # Card 9: Retroceder 3 casilleros
                roll = value # -3
                old_pos = player.posicion
                
                player.posicion = (old_pos + roll) % 40 
                
                self.current_message += f" 🚶 Retrocedes a {self.board[player.posicion]['nombre']}."
                self.interaction_done = True


    # ----------------------------------------

    def handle_interaction(self):
        """Maneja lo que sucede al caer en una casilla."""
        player = self.current_player
        posicion = player.posicion
        casilla = self.board[posicion]
        
        self.current_message += f" Caíste en {casilla['nombre']}."
        
        if casilla["tipo"] in ["Propiedad", "Ferrocarril", "Servicio"]:
            
            # 1. No tiene dueño: Ofrecer compra
            if casilla["propietario"] is None:
                if player.dinero >= casilla["precio"]:
                    self.current_message += f" ¡{casilla['nombre']} no tiene dueño! Precio: ${casilla['precio']}. (B/N)"
                    self.purchase_state = True
                else:
                    self.current_message += f" ¡{casilla['nombre']} no tiene dueño! No tienes suficiente dinero ($ {casilla['precio']})."
                    self.interaction_done = True 
            
            # 2. Tiene dueño (otro jugador): Cobrar alquiler y transferir dinero
            elif casilla["propietario"] != player.id:
                alquiler = casilla["alquiler"]
                
                if player.pay(alquiler):
                    self.handle_bankruptcy(player)
                    return 
                
                propietario_obj = next((p for p in self.players if p.id == casilla["propietario"]), None)
                
                if propietario_obj and propietario_obj.activo:
                    propietario_obj.receive_money(alquiler)
                    self.current_message += f" 💰 ¡{casilla['nombre']} es de {propietario_obj.nombre}! Pagaste alquiler de **${alquiler}**."
                else:
                    self.current_message += f" Pagaste alquiler: ${alquiler}. (Dueño no encontrado o inactivo)."
                    
                self.interaction_done = True 
            
            # 3. Es tuya
            else:
                self.current_message += f" ¡Bienvenido a tu propiedad: {casilla['nombre']}!"
                self.interaction_done = True 

        elif casilla["tipo"] == "Impuesto":
            impuesto = casilla["precio"] 
            if player.pay(impuesto):
                self.handle_bankruptcy(player)
                return
            self.current_message += f" 💸 ¡IMPUESTO! Pagaste **${impuesto}**."
            self.interaction_done = True 

        elif casilla["tipo"] in ["Suerte", "Comunidad"]:
            # --- MANEJO DE SUERTE ---
            if casilla["nombre"] == "SUERTE":
                self.process_suerte_card()
            else:
                self.current_message += f" ❓ ¡Caíste en {casilla['nombre']}! (Presiona 'S' para continuar)"
                self.interaction_done = True
            
        elif casilla["tipo"] == "Descanso": 
            self.current_message += f" 😴 ¡Caíste en {casilla['nombre']}! Disfruta tu descanso."
            self.interaction_done = True
            
        elif casilla["tipo"] == "IrACárcel":
            player.posicion = 10 
            player.turns_in_jail = 1 
            self.current_message += f" 🚓 ¡IR A CÁRCEL! {player.nombre} ha sido enviado a la Cárcel."
            self.interaction_done = True 
    
    def process_purchase(self, wants_to_buy):
        """Maneja la decisión de compra de propiedad."""
        player = self.current_player
        casilla_actual = self.board[player.posicion]
        
        if wants_to_buy:
            if player.dinero >= casilla_actual["precio"]:
                player.pay(casilla_actual["precio"]) 
                self.board[player.posicion]["propietario"] = player.id
                self.current_message = f" ¡COMPRADO! {player.nombre} es dueño de {casilla_actual['nombre']} por ${casilla_actual['precio']}."
            else:
                self.current_message = " ¡No tienes suficiente dinero para comprar!"
        else:
            self.current_message = f" {player.nombre} decidió no comprar {casilla_actual['nombre']}."
        
        self.purchase_state = False
        self.next_turn()

    def get_token_coords(self, pos, player_id):
        """Mapea la posición del tablero a coordenadas de pantalla (x, y)."""
        offset_map = {1: (0, 0), 2: (15, 0), 3: (0, 15), 4: (15, 15)}
        offset_x, offset_y = offset_map.get(player_id, (0, 0))

        # Coordenadas base (sin cambios)
        if 0 <= pos <= 10: 
            x = self.ANCHO - (pos + 1) * self.ESPACIO
            y = self.ALTURA - self.ESPACIO
            if pos == 0: x = self.ANCHO - self.ESPACIO 
            if pos == 10: x = 0; y = self.ALTURA - self.ESPACIO 
            
        elif 11 <= pos <= 20: 
            x = 0
            y = self.ALTURA - (pos - 10) * self.ESPACIO
            if pos == 20: y = 0 
            
        elif 21 <= pos <= 30: 
            x = (pos - 20) * self.ESPACIO
            y = 0
            if pos == 30: x = self.ANCHO - self.ESPACIO 
            
        elif 31 <= pos <= 39: 
            x = self.ANCHO - self.ESPACIO
            y = (pos - 30) * self.ESPACIO
            
        else:
            x = self.BORDE
            y = self.BORDE
        
        # Ajuste simple de centrado + offset (sin cambios)
        x += (self.ESPACIO - self.TAMANO_FICHA[0]) // 2 + offset_x - 7
        y += (self.ESPACIO - self.TAMANO_FICHA[1]) // 2 + offset_y - 7
        
        return (x, y)


    def draw_board(self):
        """Dibuja el tablero, nombres de casillas y barras de color. (Sin cambios)"""
        from seteador import BLACK
        
        for i in range(11):
            pygame.draw.line(self.pantalla, BLACK, (i * self.ESPACIO, 0), (i * self.ESPACIO, self.ALTURA))
            pygame.draw.line(self.pantalla, BLACK, (0, i * self.ESPACIO), (self.ANCHO, i * self.ESPACIO))

        for i in range(40):
            casilla = self.board[i]
            
            if 0 <= i <= 10: 
                rect = pygame.Rect(self.ANCHO - (i + 1) * self.ESPACIO, self.ALTURA - self.ESPACIO, self.ESPACIO, self.ESPACIO)
                color_rect = pygame.Rect(rect.left, rect.top, self.ESPACIO, 10) 
            elif 11 <= i <= 20: 
                rect = pygame.Rect(0, self.ALTURA - (i - 9) * self.ESPACIO, self.ESPACIO, self.ESPACIO)
                color_rect = pygame.Rect(rect.right - 10, rect.top, 10, self.ESPACIO) 
            elif 21 <= i <= 30: 
                rect = pygame.Rect((i - 20) * self.ESPACIO, 0, self.ESPACIO, self.ESPACIO)
                color_rect = pygame.Rect(rect.left, rect.bottom - 10, self.ESPACIO, 10) 
            elif 31 <= i <= 39: 
                rect = pygame.Rect(self.ANCHO - self.ESPACIO, (i - 30) * self.ESPACIO, self.ESPACIO, self.ESPACIO)
                color_rect = pygame.Rect(rect.left, rect.top, 10, self.ESPACIO) 
            else:
                 continue 

            if casilla["tipo"] in ["Propiedad", "Ferrocarril", "Servicio"]:
                pygame.draw.rect(self.pantalla, casilla["color_grupo"], color_rect)
                
                if casilla["propietario"] is not None:
                    dueño = next((p for p in self.players if p.id == casilla["propietario"]), None)
                    if dueño:
                        propietario_color = dueño.color
                        owner_rect = pygame.Rect(rect.centerx - 5, rect.centery - 5, 10, 10)
                        pygame.draw.rect(self.pantalla, propietario_color, owner_rect)

            nombre_linea1 = self.SMALL_FONT.render(casilla["nombre"], True, BLACK)
            
            if nombre_linea1.get_width() > self.ESPACIO - 4:
                palabras = casilla["nombre"].split()
                if palabras:
                    nombre_linea1_rend = self.SMALL_FONT.render(palabras[0], True, BLACK)
                    nombre_linea2_rend = self.SMALL_FONT.render(" ".join(palabras[1:]), True, BLACK)
                    self.pantalla.blit(nombre_linea1_rend, (rect.centerx - nombre_linea1_rend.get_width() / 2, rect.top + 10))
                    self.pantalla.blit(nombre_linea2_rend, (rect.centerx - nombre_linea2_rend.get_width() / 2, rect.top + 25))
                
            else:
                self.pantalla.blit(nombre_linea1, (rect.centerx - nombre_linea1.get_width() / 2, rect.top + 20))

            if casilla["precio"] > 0 and casilla["tipo"] != "Impuesto":
                precio_texto = self.TINY_FONT.render(f"${casilla['precio']}", True, BLACK)
                self.pantalla.blit(precio_texto, (rect.centerx - precio_texto.get_width() / 2, rect.bottom - 15))


        centro_rect = pygame.Rect(self.ESPACIO, self.ESPACIO, self.ANCHO - 2*self.ESPACIO, self.ALTURA - 2*self.ESPACIO)
        
        if self.fondo_img:
            self.pantalla.blit(self.fondo_img, centro_rect.topleft)
        else:
            pygame.draw.rect(self.pantalla, (240, 240, 240), centro_rect)
            
        pygame.draw.rect(self.pantalla, BLACK, centro_rect, 2)

    def draw_ui(self):
        """Dibuja la información de estado de los jugadores y los mensajes del juego (Actualizado)."""
        from seteador import WHITE, BLUE, BLACK 
        
        # Título (sin cambios)
        text_title = self.FONT.render("Monopoly Argentino", True, BLACK)
        self.pantalla.blit(text_title, (self.ANCHO/2 - text_title.get_width()/2, self.ALTURA/2 - 140))
        
        # Estado de todos los jugadores (sin cambios)
        y_offset = self.ALTURA/2 - 90
        for jugador in self.players:
            if jugador.activo:
                prefix = "->" if jugador.id == self.current_player.id and not self.game_over else ""
                status_text = f"{prefix} {jugador.nombre} (${jugador.dinero})"
                if jugador.turns_in_jail > 0:
                    status_text += f" (Cárcel T{jugador.turns_in_jail})"
                if jugador.extra_turn_count > 0:
                    status_text += f" (+{jugador.extra_turn_count} Turno)"
                    
                color = jugador.color
            else:
                status_text = f"X {jugador.nombre} (ELIMINADO)"
                color = (100, 100, 100)
                
            text_status = self.STATUS_FONT.render(status_text, True, color)
            self.pantalla.blit(text_status, (self.ANCHO/2 - text_status.get_width()/2, y_offset))
            y_offset += 25

        # ---------------------------------------------------
        # FONDO PARA EL MENSAJE DEL JUEGO - NUEVO
        # ---------------------------------------------------
        
        message = self.current_message
        line1_text = message
        line2_text = None
        
        # Lógica para dividir el mensaje si es muy largo (más de 50 caracteres)
        if len(message) > 50 and ' ' in message:
            split_point = len(message) // 2
            # Buscar el espacio más cercano antes o después de la mitad
            idx = message.rfind(' ', 0, split_point + 5) 
            
            if idx != -1:
                line1_text = message[:idx].strip()
                line2_text = message[idx:].strip()

        # Crear superficie semitransparente para el fondo del mensaje
        if line2_text:
            # Calcular dimensiones para 2 líneas
            text_line1 = self.SMALL_FONT.render(line1_text, True, BLACK)
            text_line2 = self.SMALL_FONT.render(line2_text, True, BLACK)
            
            ancho_fondo = max(text_line1.get_width(), text_line2.get_width()) + 40
            alto_fondo = 60  # Espacio para 2 líneas
            
            # Crear superficie semitransparente
            fondo_mensaje = pygame.Surface((ancho_fondo, alto_fondo), pygame.SRCALPHA)
            fondo_mensaje.fill((255, 255, 255, 200))  # Blanco semitransparente (alpha = 200)
            
            # Dibujar fondo centrado
            x_fondo = self.ANCHO/2 - ancho_fondo/2
            y_fondo = self.ALTURA/2 + 20
            self.pantalla.blit(fondo_mensaje, (x_fondo, y_fondo))
            
            # Dibujar borde opcional
            pygame.draw.rect(self.pantalla, BLACK, (x_fondo, y_fondo, ancho_fondo, alto_fondo), 1)
            
            # Dibujar texto sobre el fondo
            self.pantalla.blit(text_line1, (self.ANCHO/2 - text_line1.get_width()/2, self.ALTURA/2 + 30))
            self.pantalla.blit(text_line2, (self.ANCHO/2 - text_line2.get_width()/2, self.ALTURA/2 + 55))
        else:
            # Calcular dimensiones para 1 línea
            text_msg = self.SMALL_FONT.render(line1_text, True, BLACK)
            
            ancho_fondo = text_msg.get_width() + 40
            alto_fondo = 40
            
            # Crear superficie semitransparente
            fondo_mensaje = pygame.Surface((ancho_fondo, alto_fondo), pygame.SRCALPHA)
            fondo_mensaje.fill((255, 255, 255, 200))  # Blanco semitransparente
            
            # Dibujar fondo centrado
            x_fondo = self.ANCHO/2 - ancho_fondo/2
            y_fondo = self.ALTURA/2 + 20
            self.pantalla.blit(fondo_mensaje, (x_fondo, y_fondo))
            
            # Dibujar borde
            pygame.draw.rect(self.pantalla, BLACK, (x_fondo, y_fondo, ancho_fondo, alto_fondo), 1)
            
            # Dibujar texto sobre el fondo
            self.pantalla.blit(text_msg, (self.ANCHO/2 - text_msg.get_width()/2, self.ALTURA/2 + 40))
        
        # ---------------------------------------------------

        # Instrucciones (sin cambios de posición)
        if not self.game_over and not self.purchase_state and not self.interaction_done:
            text_instr_roll = self.SMALL_FONT.render("Presiona 'S' para tirar los dados", True, BLACK)
            self.pantalla.blit(text_instr_roll, (self.ANCHO/2 - text_instr_roll.get_width()/2, self.ALTURA/2 + 90))

        elif self.purchase_state:
            casilla_actual = self.board[self.current_player.posicion]
            text_instr_buy = self.FONT.render(f"¿Comprar ({casilla_actual['precio']})? (B/N)", True, BLUE)
            self.pantalla.blit(text_instr_buy, (self.ANCHO/2 - text_instr_buy.get_width()/2, self.ALTURA/2 + 90))

        elif self.interaction_done:
            text_instr_pause = self.FONT.render("Presiona 'S' para continuar", True, (0, 100, 0))
            self.pantalla.blit(text_instr_pause, (self.ANCHO/2 - text_instr_pause.get_width()/2, self.ALTURA/2 + 90))
            
    def draw_players(self):
        """Dibuja las fichas de los jugadores en el tablero. (Sin cambios)"""
        for player in self.players:
            if player.activo:
                player_coords = self.get_token_coords(player.posicion, player.id)
                self.pantalla.blit(player.ficha_img, player_coords)

    def draw(self):
        """Método principal de dibujo. (Sin cambios)"""
        from seteador import WHITE 
        self.pantalla.fill(WHITE)
        self.draw_board()
        self.draw_ui()
        self.draw_players()
        pygame.display.flip()