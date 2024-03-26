'''
en esta version aparte de contar los obstaculos y 
contar las veces que choca o no choca,
tambien le agregue que recolecte "si salto" o "no salto"

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
obstaculos = 0
colisiones = 0
listaobst = []
listacol = []
listasalto=[]

def main():
    global obstaculos, colisiones
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
                    if dino_jump:
                        listasalto.append("si salto")
                        print(listasalto)
                    #else:
                    #    listasalto.append("no salto")
                    #    print(listasalto)

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
        obstacle_rect.x -= OBSTACLE_SPEED  # Desplaza el obstáculo hacia la izquierda según la velocidad del juego

        # Verifica si el obstáculo ha pasado completamente fuera de la pantalla por la izquierda
        if obstacle_rect.right < 0:
            obstacle_rect.left = WIDTH  # Si es así, reposiciona el obstáculo completamente a la derecha de la pantalla
            # Restablece la posición vertical del obstáculo para que esté alineado con el suelo
            obstacle_rect.top = HEIGHT - OBSTACLE_SIZE
            obstaculos += 1  # Incrementa el contador de obstáculos pasados
            listaobst.append(1)
            print(listaobst)
            # Incrementa el contador de colisiones
            colisiones += 0
            listacol.append("no choco")
            print(listacol)

        # Dibuja el dinosaurio y el obstáculo
        pygame.draw.rect(screen, BLACK, dino_rect)
        pygame.draw.rect(screen, RED, obstacle_rect)

        # Dibuja las vidas
        font = pygame.font.Font(None, 36)
        text = font.render(f"Obstaculo numero: {obstaculos}, Colisiones: {colisiones}", True, BLACK)
        screen.blit(text, (10, 10))

        # Verifica si hay colisión entre el rectángulo del dinosaurio y el rectángulo del obstáculo
        if dino_rect.colliderect(obstacle_rect):
            # Comprueba si el dinosaurio está en el suelo (altura máxima) para considerar una colisión válida
            if dino_rect.bottom == HEIGHT:
                # Si el dinosaurio colisiona con el obstáculo, mueve el obstáculo fuera de la pantalla
                # y restablece su posición vertical alineada con el suelo
                obstacle_rect.left = WIDTH
                obstacle_rect.top = HEIGHT - OBSTACLE_SIZE
                # Incrementa el contador de obstáculos pasados
                obstaculos += 1
                listaobst.append(1)
                print(listaobst)
                # Incrementa el contador de colisiones
                colisiones += 1
                listacol.append("choco")
                print(listacol)
                if len(listasalto)<len(listacol):
                    listasalto.append("no salto")
                    print(listasalto)

                

        pygame.display.flip()
        clock.tick(GAME_SPEED)

if __name__ == "__main__":
    main()
