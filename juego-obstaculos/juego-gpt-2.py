import pygame
import random

# Dimensiones de la ventana
WIDTH = 800
HEIGHT = 600

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

class Player:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT - 50
        self.width = 20
        self.height = 20
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self, dx):
        self.x += dx
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, surface):
        pygame.draw.rect(surface, RED, self.rect)  # Cambiar el color a RED


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

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Esquivar Obstáculos")

    clock = pygame.time.Clock()
    player = Player()
    obstacles = []

    data = []

    running = True
    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x > 0:
            player.move(-5)
        if keys[pygame.K_RIGHT] and player.x < WIDTH - player.width:
            player.move(5)

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
                # Si hay colisión, registra los datos y reinicia el juego
                data.append([player.x, obstacle.x, obstacle.y])
                obstacles = []
                break

            # Elimina obstáculos que hayan salido de la pantalla
            if obstacle.y > HEIGHT:
                obstacles.remove(obstacle)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

    # Guarda los datos recolectados
    with open('obstacle_data.txt', 'w') as f:
        for entry in data:
            f.write(','.join(map(str, entry)) + '\n')

if __name__ == "__main__":
    main()
