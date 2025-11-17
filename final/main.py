import pygame
from seteador import ANCHO, ALTURA, WHITE, BLUE
from data import TABLERO_DATA, JUGADORES_INICIAL
from classes import Game

# INICIALIZACIÓN DE PYGAME 
pygame.init()
pygame.display.set_caption("Monopoly Argentino")

PANTALLA = pygame.display.set_mode((ANCHO, ALTURA))
CLOCK = pygame.time.Clock()
FPS = 60

#  CONFIGURAMOS LAS FUENTES 
try:
    FONT = pygame.font.SysFont('Arial', 24)
    SMALL_FONT = pygame.font.SysFont('Arial', 14)
    TINY_FONT = pygame.font.SysFont('Arial', 10)
    STATUS_FONT = pygame.font.SysFont('Arial', 16)
except:
    FONT = pygame.font.Font(None, 30)
    SMALL_FONT = pygame.font.Font(None, 18)
    TINY_FONT = pygame.font.Font(None, 12)
    STATUS_FONT = pygame.font.Font(None, 20)

# Inicializar el juego
monopoly_game = Game(
    board_data=TABLERO_DATA,
    players_data=JUGADORES_INICIAL,
    pantalla=PANTALLA,
    fonts=(FONT, SMALL_FONT, TINY_FONT, STATUS_FONT)
)

#  BUCLE PRINCIPAL DE JUEGO -
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Manejo de entrada
        if event.type == pygame.KEYDOWN and not monopoly_game.game_over:
            
            player = monopoly_game.current_player
            
            # 1)INTERCAMBIO 
            if monopoly_game.trade_state:
                if event.key == pygame.K_ESCAPE:
                    monopoly_game.cancel_trade()
                    
                elif monopoly_game.selected_my_property is None:
                    # Elegir una propiedad propia
                    if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, 
                                   pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]:
                        property_index = event.key - pygame.K_1  # 0-9
                        monopoly_game.select_my_property_for_trade(property_index)
                        
                elif monopoly_game.selected_target_player is None:
                    # Selección de jugador
                    if event.key == pygame.K_F1:
                        monopoly_game.select_trade_partner(0)
                    elif event.key == pygame.K_F2:
                        monopoly_game.select_trade_partner(1)
                    elif event.key == pygame.K_F3:
                        monopoly_game.select_trade_partner(2)
                    elif event.key == pygame.K_F4:
                        monopoly_game.select_trade_partner(3)
                        
                elif monopoly_game.selected_their_property is None:
                    #Elige una propiedad de otro jugador
                    if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, 
                                   pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]:
                        property_index = event.key - pygame.K_1  # 0-8
                        monopoly_game.select_their_property_for_trade(property_index)
                        
                else:
                    # Confirmación final
                    if event.key == pygame.K_RETURN:
                        monopoly_game.complete_trade()
            
            #2)INICIA INTERCAMBIO desde Descanso
            elif event.key == pygame.K_n:
                current_pos = player.posicion
                current_cell = monopoly_game.board[current_pos]
                # Verificar si está en descanso 
                if (current_cell["tipo"] == "Descanso" and 
                    not monopoly_game.purchase_state and 
                    not monopoly_game.trade_state):
                    print("Iniciando intercambio desde Descanso") 
                    monopoly_game.trade_state = True
                    monopoly_game.start_trade()
            
            # 3) TIRADA DE DADOS
            elif event.key == pygame.K_s and not monopoly_game.purchase_state and not monopoly_game.interaction_done:
                # Tira dados y mueve
                roll = monopoly_game.roll_dice()
                if roll > 0:
                    if player.move(roll):
                        player.receive_money(200)
                        monopoly_game.current_message += " 💸 ¡Cobraste $200 por pasar SALIDA!"
                    
                    monopoly_game.handle_interaction()

            # 4) TEMINA LA INTERACCIÓN 
            elif event.key == pygame.K_s and monopoly_game.interaction_done:
                monopoly_game.interaction_done = False
                monopoly_game.next_turn()

            # 5) COMPRA O NO
            elif monopoly_game.purchase_state:
                if event.key == pygame.K_b:
                    monopoly_game.process_purchase(wants_to_buy=True)
                elif event.key == pygame.K_n:
                    monopoly_game.process_purchase(wants_to_buy=False)
    # Lógica de dibujo
    PANTALLA.fill(WHITE)
    monopoly_game.draw()

    pygame.display.flip()
    CLOCK.tick(FPS)

pygame.quit()