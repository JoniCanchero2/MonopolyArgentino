import pygame
import sys

pygame.init()

ANCHO = 750 
ALTO = 700
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Monopoly Argentino")

reloj = pygame.time.Clock()
FPS = 60 

moriste = False
color_fondo = (0, 0, 0)
DISTANCIA_MOVIMIENTO = 10 

TAMANO_FICHA = 60 

try:
    imagen_tablero = pygame.image.load('argentina.png').convert() 
    imagen_tablero = pygame.transform.scale(imagen_tablero, (700, 700))
    rect_tablero = imagen_tablero.get_rect()
    rect_tablero.center = (ANCHO // 2, ALTO // 2)

    imagen_jugador_1 = pygame.image.load('pelota.png').convert_alpha() 
    imagen_jugador_1 = pygame.transform.scale(imagen_jugador_1, (TAMANO_FICHA, TAMANO_FICHA))
    rect_jugador_1 = imagen_jugador_1.get_rect()
    rect_jugador_1.center = (ANCHO - 50, ALTO - 50) 
    
    imagen_jugador_2 = pygame.image.load('mate.png').convert_alpha() 
    imagen_jugador_2 = pygame.transform.scale(imagen_jugador_2, (TAMANO_FICHA, TAMANO_FICHA))
    rect_jugador_2 = imagen_jugador_2.get_rect()
    rect_jugador_2.center = (50, ALTO - 50) 

except pygame.error as e:
    print(f"se cargo mal la imagen: {e}")
    pygame.quit()
    sys.exit()


while not moriste: 
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            moriste = True
            
        if event.type == pygame.KEYDOWN:
            rect_jugador_1.y -= DISTANCIA_MOVIMIENTO 
            rect_jugador_2.y -= DISTANCIA_MOVIMIENTO 
        
    
    pantalla.fill(color_fondo) 
    
    pantalla.blit(imagen_tablero, rect_tablero) 
    
    pantalla.blit(imagen_jugador_1, rect_jugador_1) 
    pantalla.blit(imagen_jugador_2, rect_jugador_2) 
    
    pygame.display.update()
    
    reloj.tick(FPS) 

pygame.quit()
sys.exit()