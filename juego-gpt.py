import numpy as np
import pygame
import random

# Dimensiones del tablero
WIDTH = 800
HEIGHT = 600

# Colores
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

class Player:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.rect = pygame.Rect(self.x, self.y, 20, 20)

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        self.rect = pygame.Rect(self.x, self.y, 20, 20)

    def draw(self, surface):
        pygame.draw.rect(surface, RED, self.rect)

class Food:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.rect = pygame.Rect(self.x, self.y, 10, 10)

    def draw(self, surface):
        pygame.draw.rect(surface, GREEN, self.rect)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Recolecta de Datos para Red Neuronal")

    clock = pygame.time.Clock()
    player = Player()
    foods = [Food() for _ in range(5)]  # Genera 5 objetos de comida al inicio

    data = []

    running = True
    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.move(-1, 0)
        if keys[pygame.K_RIGHT]:
            player.move(1, 0)
        if keys[pygame.K_UP]:
            player.move(0, -1)
        if keys[pygame.K_DOWN]:
            player.move(0, 1)

        player.draw(screen)
        for food in foods:
            food.draw(screen)

        for food in foods:
            if player.rect.colliderect(food.rect):
                # Recolecta datos
                data.append([player.x, player.y, food.x, food.y])
                # Genera nueva comida
                foods.remove(food)
                foods.append(Food())

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

    # Guarda los datos recolectados
    np.save('training_data.npy', np.array(data))

if __name__ == "__main__":
    main()
