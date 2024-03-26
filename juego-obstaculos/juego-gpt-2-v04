import pygame
import random
import sys

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

    def move(self):
        # Mueve al jugador según su velocidad
        self.rect.move_ip(self.velocity[0], self.velocity[1])

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

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Esquivar Obstáculos")

    clock = pygame.time.Clock()
    player = Player()
    obstacles = []

    data = []

    running = True
    iterations = 0
    max_iterations = 5000  # Cambia este valor según cuántos datos quieras recolectar

    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    # Imprimir datos recolectados por consola
                    print("Datos recolectados:")
                    for entry in data:
                        print(entry)

        # Cambia la velocidad del jugador de forma aleatoria cada 100 iteraciones
        if iterations % 100 == 0:
            player.velocity = [random.randint(-2, 2), random.randint(-2, 2)]

        # Mueve al jugador
        player.move()
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
                # Si hay colisión, registra los datos
                data.append([player.rect.x, obstacle.rect.x, obstacle.rect.y])

            # Elimina obstáculos que hayan salido de la pantalla
            if obstacle.rect.y > HEIGHT:
                obstacles.remove(obstacle)

        pygame.display.flip()
        clock.tick(60)
        iterations += 1

        # Guarda los datos recolectados periódicamente
        if iterations % 100 == 0:
            with open('obstacle_data.txt', 'a') as f:
                for entry in data:
                    f.write(','.join(map(str, entry)) + '\n')
            data = []

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

