'''

nueva version de ino de google con chatgpt sin imagenes 
(usando cuadrados de colores en lugar de dino y cactus)

funciona mal !!

en vez de descontar vidas cuando choca, descuenta siempre

me sirve para en el futuro contar los obstaculos

'''

import pygame
import sys
import random

# Dimensiones de la pantalla
WIDTH, HEIGHT = 600, 200

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Tamaño del dinosaurio y del obstáculo
DINO_SIZE = 30
OBSTACLE_SIZE = 30

# Posición inicial del dinosaurio y del obstáculo
DINO_INITIAL_POS = (50, HEIGHT - DINO_SIZE)
OBSTACLE_INITIAL_POS = (WIDTH, HEIGHT - OBSTACLE_SIZE)

# Velocidad del juego y del obstáculo
GAME_SPEED = 10
OBSTACLE_SPEED = 20

# Cantidad de obstaculos
obstaculos = 2000

def main():
    global obstaculos
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Dino Game")

    dino_rect = pygame.Rect(DINO_INITIAL_POS, (DINO_SIZE, DINO_SIZE))
    obstacle_rect = pygame.Rect(OBSTACLE_INITIAL_POS, (OBSTACLE_SIZE, OBSTACLE_SIZE))

    clock = pygame.time.Clock()

    dino_jump = False  # Variable para controlar el salto del dinosaurio

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and dino_rect.bottom == HEIGHT:
                    dino_jump = True

        screen.fill(WHITE)

        # Movimiento del dinosaurio
        if dino_jump:
            if dino_rect.bottom >= HEIGHT - 100:
                dino_rect.y -= 20
            else:
                dino_jump = False
        elif dino_rect.bottom < HEIGHT:
            dino_rect.y += 10

        # Movimiento del obstáculo
        obstacle_rect.x -= OBSTACLE_SPEED
        if obstacle_rect.right < 0:
            obstacle_rect.left = WIDTH
            # Restablecer la posición vertical del obstáculo para que esté alineado con el dinosaurio
            obstacle_rect.top = HEIGHT - OBSTACLE_SIZE
            obstaculos -= 1

        # Dibuja el dinosaurio y el obstáculo
        pygame.draw.rect(screen, BLACK, dino_rect)
        pygame.draw.rect(screen, RED, obstacle_rect)

        # Dibuja las vidas
        font = pygame.font.Font(None, 36)
        text = font.render(f"Obstaculo numero: {obstaculos}", True, BLACK)
        screen.blit(text, (10, 10))

        # cuenta cuando pasa un obstáculo
        if dino_rect.colliderect(obstacle_rect):
            # Restablecer la posición del obstáculo
            if dino_rect.bottom == HEIGHT:
                obstacle_rect.left = WIDTH
                obstacle_rect.top = HEIGHT - OBSTACLE_SIZE 
                obstaculos -= 1

        pygame.display.flip()
        clock.tick(GAME_SPEED)

if __name__ == "__main__":
    main()
