## BY CHATGPT

import pygame  # Importar la biblioteca pygame para crear el juego
import random  # Importar la biblioteca random para generar números aleatorios

# Inicializar pygame
pygame.init()

# Definir constantes para el tamaño de la pantalla, altura del suelo, gravedad, fuerza de salto, etc.
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

# Definir colores usando tuplas RGB
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Definir la clase del dinosaurio
class Dinosaur(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))  # Crear una superficie para representar al dinosaurio
        self.image.fill(BLACK)  # Rellenar la superficie con el color negro
        self.rect = self.image.get_rect()  # Obtener el rectángulo del dinosaurio
        self.rect.bottom = SCREEN_HEIGHT - GROUND_HEIGHT  # Colocar el dinosaurio en la parte inferior de la pantalla
        self.rect.left = 50  # Posición inicial del dinosaurio en el eje x
        self.velocity_y = 0  # Velocidad inicial en el eje y
        self.on_ground = True  # Indicador para verificar si el dinosaurio está en el suelo

    def update(self):
        self.velocity_y += GRAVITY  # Aplicar la gravedad al movimiento del dinosaurio
        self.rect.y += self.velocity_y  # Actualizar la posición vertical del dinosaurio
        if self.rect.bottom >= SCREEN_HEIGHT - GROUND_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT - GROUND_HEIGHT
            self.velocity_y = 0
            self.on_ground = True
        else:
            self.on_ground = False

    def jump(self):
        if self.on_ground:
            self.velocity_y = JUMP_FORCE  # Hacer que el dinosaurio salte cambiando su velocidad vertical

# Definir la clase del obstáculo
class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((OBSTACLE_WIDTH, OBSTACLE_HEIGHT))  # Crear una superficie para representar el obstáculo
        self.image.fill(RED)  # Rellenar la superficie con el color rojo
        self.rect = self.image.get_rect()  # Obtener el rectángulo del obstáculo
        self.rect.bottom = SCREEN_HEIGHT - GROUND_HEIGHT  # Colocar el obstáculo en la parte inferior de la pantalla
        self.rect.left = SCREEN_WIDTH  # Posición inicial del obstáculo en el eje x

    def update(self):
        self.rect.x -= OBSTACLE_SPEED  # Mover el obstáculo hacia la izquierda

# Definir la clase del juego
class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Crear la pantalla del juego
        self.clock = pygame.time.Clock()  # Crear un reloj para controlar la velocidad de actualización
        self.all_sprites = pygame.sprite.Group()  # Crear un grupo para todos los sprites
        self.obstacles = pygame.sprite.Group()  # Crear un grupo para los obstáculos
        self.dinosaur = Dinosaur()  # Crear una instancia del dinosaurio
        self.all_sprites.add(self.dinosaur)  # Agregar el dinosaurio al grupo de todos los sprites
        self.next_obstacle_time = 0  # Variable para controlar el tiempo de aparición del próximo obstáculo

    def run(self):
        running = True
        while running:
            self.clock.tick(30)  # Limitar la velocidad de fotogramas a 30 por segundo
            for event in pygame.event.get():  # Manejar eventos del juego
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.dinosaur.jump()  # Hacer que el dinosaurio salte al presionar la barra espaciadora

            self.all_sprites.update()  # Actualizar todos los sprites en el juego

            current_time = pygame.time.get_ticks()
            if current_time > self.next_obstacle_time:  # Controlar la aparición de obstáculos
                OBSTACLE_INTERVAL = random.randint(MIN_OBSTACLE_INTERVAL, MAX_OBSTACLE_INTERVAL)
                self.next_obstacle_time = current_time + OBSTACLE_INTERVAL
                obstacle = Obstacle()  # Crear un nuevo obstáculo
                self.all_sprites.add(obstacle)  # Agregar el obstáculo al grupo de todos los sprites
                self.obstacles.add(obstacle)  # Agregar el obstáculo al grupo de obstáculos

            # Verificar colisiones entre el dinosaurio y los obstáculos
            if pygame.sprite.spritecollideany(self.dinosaur, self.obstacles):
                running = False  # Terminar el juego si hay una colisión

            self.screen.fill(WHITE)  # Llenar la pantalla con el color blanco
            self.all_sprites.draw(self.screen)  # Dibujar todos los sprites en la pantalla
            pygame.display.flip()  # Actualizar la pantalla

        pygame.quit()  # Salir del juego al finalizar

# Iniciar el juego si este archivo es ejecutado directamente
if __name__ == "__main__":
    game = Game()  # Crear una instancia del juego
    game.run()  # Ejecutar el juego
                  
