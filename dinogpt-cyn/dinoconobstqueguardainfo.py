
######### OJO

####### este codigo lo estoy trabajando, aun no funciona bien

import pygame
import random

# Inicializar pygame
pygame.init()

# Definir constantes
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 200
GROUND_HEIGHT = 50
GRAVITY = 0.5
JUMP_FORCE = -10
OBSTACLE_WIDTH = 20
OBSTACLE_HEIGHT = 50
OBSTACLE_SPEED = 5
MIN_OBSTACLE_INTERVAL = 700
MAX_OBSTACLE_INTERVAL = 3500

# Definir colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Clase del dinosaurio
class Dinosaur(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = SCREEN_HEIGHT - GROUND_HEIGHT
        self.rect.left = 50
        self.velocity_y = 0
        self.on_ground = True

    def update(self):
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y
        if self.rect.bottom >= SCREEN_HEIGHT - GROUND_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT - GROUND_HEIGHT
            self.velocity_y = 0
            self.on_ground = True
        else:
            self.on_ground = False

    def jump(self):
        if self.on_ground:
            self.velocity_y = JUMP_FORCE

# Clase del obstáculo
class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.bottom = SCREEN_HEIGHT - GROUND_HEIGHT
        self.rect.left = SCREEN_WIDTH

    def update(self):
        self.rect.x -= OBSTACLE_SPEED

# Clase del juego
class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.all_sprites = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.dinosaur = Dinosaur()
        self.all_sprites.add(self.dinosaur)
        self.next_obstacle_time = 0
        self.jump_distances = []  # Array para almacenar las distancias al saltar
        self.collision_data = []  # Array para almacenar los datos de colisión

    def run(self):
        running = True
        while running:
            self.clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.dinosaur.jump()
                        self.record_jump_distance()  # Llamar a la función para registrar la distancia al saltar

            self.all_sprites.update()

            current_time = pygame.time.get_ticks()
            if current_time > self.next_obstacle_time:
                OBSTACLE_INTERVAL = random.randint(MIN_OBSTACLE_INTERVAL, MAX_OBSTACLE_INTERVAL)
                self.next_obstacle_time = current_time + OBSTACLE_INTERVAL
                obstacle = Obstacle()
                self.all_sprites.add(obstacle)
                self.obstacles.add(obstacle)

                self.record_collision()  # Llamar a la función para registrar la colisión

            self.screen.fill(WHITE)
            self.all_sprites.draw(self.screen)
            pygame.display.flip()

            # Imprimir los datos recopilados en cada iteración
            print("Distancias al saltar:", self.jump_distances)
            print("Datos de colisión:", self.collision_data)

        pygame.quit()

    def record_jump_distance(self):
        for obstacle in self.obstacles:
            if obstacle.rect.left > self.dinosaur.rect.right:  # Verificar que el obstáculo está delante del dinosaurio
                distance = obstacle.rect.left - self.dinosaur.rect.right
                self.jump_distances.append(distance)
                break  # Salir del bucle después de guardar una distancia

    def record_collision(self):
        # Verificar colisión y registrar el resultado en el array
        if pygame.sprite.spritecollideany(self.dinosaur, self.obstacles):
            self.collision_data.append(1)
        else:
            self.collision_data.append(0)

# Iniciar el juego
if __name__ == "__main__":
    game = Game()
    game.run()
