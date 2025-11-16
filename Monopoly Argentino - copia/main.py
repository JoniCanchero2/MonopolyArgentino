import pygame
from seteador import ANCHO, ALTURA, WHITE, BLUE
from data import TABLERO_DATA, JUGADORES_INICIAL
from classes import Game

# --- CONFIGURACIÓN E INICIALIZACIÓN DE PYGAME ---
pygame.init()
pygame.display.set_caption("Monopoly Argentino")

PANTALLA = pygame.display.set_mode((ANCHO, ALTURA))
CLOCK = pygame.time.Clock()
FPS = 60

# --- CONFIGURACIÓN DE FUENTES ---
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

# Inicializar la instancia del juego
monopoly_game = Game(
    board_data=TABLERO_DATA,
    players_data=JUGADORES_INICIAL,
    pantalla=PANTALLA,
    fonts=(FONT, SMALL_FONT, TINY_FONT, STATUS_FONT)
)

# --- BUCLE PRINCIPAL DE JUEGO (GAME LOOP) ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Manejo de entrada
        if event.type == pygame.KEYDOWN and not monopoly_game.game_over:
            
            player = monopoly_game.current_player
            
            # 1. TIRADA DE DADOS
            # Solo permite tirar si NO estamos comprando y NO estamos en pausa post-interacción
            if event.key == pygame.K_s and not monopoly_game.purchase_state and not monopoly_game.interaction_done:
                # Tirar dados y mover
                roll = monopoly_game.roll_dice()
                if roll > 0:
                    if player.move(roll):
                        player.receive_money(200) # Usar receive_money para cobrar
                        monopoly_game.current_message += " 💸 ¡Cobraste $200 por pasar SALIDA!"
                    
                    monopoly_game.handle_interaction()

            # 2. FIN DE INTERACCIÓN (PAUSA)
            # Permite pasar al siguiente turno si estamos en pausa post-interacción
            elif event.key == pygame.K_s and monopoly_game.interaction_done:
                monopoly_game.interaction_done = False # Desactiva la pausa
                monopoly_game.next_turn()              # Pasa al siguiente turno

            # 3. DECISIÓN DE COMPRA
            elif monopoly_game.purchase_state:
                # Decisión de compra (El turno pasa en process_purchase)
                if event.key == pygame.K_b: # Comprar (Buy)
                    monopoly_game.process_purchase(wants_to_buy=True)
                
                elif event.key == pygame.K_n: # No comprar
                    monopoly_game.process_purchase(wants_to_buy=False)

    # Lógica de dibujo
    PANTALLA.fill(WHITE)
    monopoly_game.draw()

    pygame.display.flip()
    CLOCK.tick(FPS)

pygame.quit()