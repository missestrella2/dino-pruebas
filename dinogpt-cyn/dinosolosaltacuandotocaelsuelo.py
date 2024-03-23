#### hecho por chatgpt

import pygame

# Inicializar pygame
pygame.init()

# Definir constantes
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 200
GROUND_HEIGHT = 50
GRAVITY = 0.5
JUMP_FORCE = -10

# Definir colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Definir la clase del dinosaurio
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

# Definir la clase del juego
class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.all_sprites = pygame.sprite.Group()
        self.dinosaur = Dinosaur()
        self.all_sprites.add(self.dinosaur)

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

            self.all_sprites.update()

            self.screen.fill(WHITE)
            self.all_sprites.draw(self.screen)
            pygame.display.flip()

        pygame.quit()

# Iniciar el juego
if __name__ == "__main__":
    game = Game()
    game.run()
