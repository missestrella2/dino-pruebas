'''
para que lo pueda leer vsc:
- cambie la version de python de 312 a 311
- cambie la version en el path variables de entorno
-reinstale las librerias

'''

import pygame
import random
import numpy as np
import tensorflow as tf

# Dimensiones de la ventana
WIDTH = 800
HEIGHT = 600

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

class Player:
    def __init__(self):
        self.width = 20
        self.height = 20
        self.rect = pygame.Rect(WIDTH // 2 - self.width // 2, HEIGHT - self.height, self.width, self.height)
        self.velocity = [0, 0]  # Velocidad inicial del jugador

    def move(self, velocity):
        # Mueve al jugador según la velocidad proporcionada por el modelo
        self.rect.move_ip(velocity[0], velocity[1])

        # Limita el movimiento para que el jugador permanezca dentro de la pantalla
        self.rect.x = max(0, min(self.rect.x, WIDTH - self.width))
        self.rect.y = max(0, min(self.rect.y, HEIGHT - self.height))

    def draw(self, surface):
        pygame.draw.rect(surface, RED, self.rect)

class Obstacle:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = 0
        self.width = random.randint(20, 50)
        self.height = random.randint(20, 50)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def fall(self, speed):
        self.y += speed
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, surface):
        pygame.draw.rect(surface, BLACK, self.rect)

def load_model(model_path):
    return tf.keras.models.load_model(model_path)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Esquivar Obstáculos")

    clock = pygame.time.Clock()
    player = Player()
    obstacles = []

    # Cargar el modelo entrenado
    model = load_model("C:\\Users\\amand\\Desktop\\programas\\juego-obstaculos\\obstacle_model.h5")


    running = True
    iterations = 0

    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        

        if obstacles:
            player_input = np.array([[player.rect.x, obstacles[0].rect.x]])  # Características de entrada para el modelo
            velocity = model.predict(player_input).flatten()  # Predicción del modelo
            print("Shape of velocity:", velocity.shape)  # Imprime la forma de velocity
            player.move(velocity)


        player.draw(screen)

        # Genera nuevos obstáculos
        if random.random() < 0.05:
            obstacles.append(Obstacle())

        # Mueve y dibuja los obstáculos
        for obstacle in obstacles:
            obstacle.fall(3)
            obstacle.draw(screen)

            # Verifica colisión con el jugador
            if obstacle.rect.colliderect(player.rect):
                print("¡Has perdido!")
                running = False

            # Elimina obstáculos que hayan salido de la pantalla
            if obstacle.rect.y > HEIGHT:
                obstacles.remove(obstacle)

        pygame.display.flip()
        clock.tick(60)
        iterations += 1

    pygame.quit()

if __name__ == "__main__":
    main()
