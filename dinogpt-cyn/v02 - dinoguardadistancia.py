'''
este codigo es para recoger datos

toma la distancia entre el dino y el objeto mas cercano cuando apreto la barra espaciadora

y le agrego que no cierre el juego al colisionar

'''


import pygame
import random

pygame.init()

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

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

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

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.all_sprites = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.dinosaur = Dinosaur()
        self.all_sprites.add(self.dinosaur)
        self.next_obstacle_time = 0
        self.closest_distance = float('inf')  # Inicializamos con una distancia muy grande
        self.distances = []  # Lista para almacenar las distancias

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

##############################################################################

                        # Calcular la distancia entre el dinosaurio y el obstáculo más cercano a la derecha
                        self.closest_distance = float('inf')  # Restablecer la distancia más cercana
                        for obstacle in self.obstacles:
                            distance = obstacle.rect.left - self.dinosaur.rect.right
                            if distance < self.closest_distance and distance > 0:  # Solo considerar obstáculos a la derecha
                                self.closest_distance = distance
                        # Guardar la distancia recién calculada solo si es finita (hay un obstáculo a la derecha)
                        if self.closest_distance != float('inf'):
                            self.distances.append(self.closest_distance)
                            print("Distancia recogida:", self.distances)


##############################################################################

            self.all_sprites.update()

            current_time = pygame.time.get_ticks()
            if current_time > self.next_obstacle_time:
                OBSTACLE_INTERVAL = random.randint(MIN_OBSTACLE_INTERVAL, MAX_OBSTACLE_INTERVAL)
                self.next_obstacle_time = current_time + OBSTACLE_INTERVAL
                obstacle = Obstacle()
                self.all_sprites.add(obstacle)
                self.obstacles.add(obstacle)

            if pygame.sprite.spritecollideany(self.dinosaur, self.obstacles):
                #running = False
                
                pass

            self.screen.fill(WHITE)
            self.all_sprites.draw(self.screen)
            pygame.display.flip()

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
