###############################
'''

en este codigo queria que guarde cuando colisionaba paralelo a las distancias

NO FUNCIONA!!!!

empece de nuevo en el archivo "dino con vidas"


'''
###############################

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
        self.image = pygame.Surface((50, 50))  # Crear una superficie para representar al dinosaurio
        self.image.fill(BLACK)  # Rellenar la superficie con el color negro
        self.rect = self.image.get_rect()  # Obtener el rectángulo que delimita al dinosaurio
        self.rect.bottom = SCREEN_HEIGHT - GROUND_HEIGHT  # Establecer la posición inicial del dinosaurio en la parte inferior de la pantalla
        self.rect.left = 50  # Establecer la posición inicial del dinosaurio en el lado izquierdo de la pantalla
        self.velocity_y = 0  # Velocidad vertical inicial del dinosaurio
        self.on_ground = True  # Indicador de si el dinosaurio está en el suelo o en el aire

    def update(self):
        self.velocity_y += GRAVITY  # Aplicar la gravedad al dinosaurio
        self.rect.y += self.velocity_y  # Actualizar la posición vertical del dinosaurio según su velocidad
        if self.rect.bottom >= SCREEN_HEIGHT - GROUND_HEIGHT:  # Verificar si el dinosaurio ha alcanzado el suelo
            self.rect.bottom = SCREEN_HEIGHT - GROUND_HEIGHT  # Ajustar la posición del dinosaurio para que esté en el suelo
            self.velocity_y = 0  # Detener la velocidad vertical del dinosaurio
            self.on_ground = True  # Indicar que el dinosaurio está en el suelo
        else:
            self.on_ground = False  # Indicar que el dinosaurio no está en el suelo

    def jump(self):
        if self.on_ground:  # Verificar si el dinosaurio está en el suelo
            self.velocity_y = JUMP_FORCE  # Aplicar una fuerza de salto al dinosaurio

class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((OBSTACLE_WIDTH, OBSTACLE_HEIGHT))  # Crear una superficie para representar al obstáculo
        self.image.fill(RED)  # Rellenar la superficie con el color rojo
        self.rect = self.image.get_rect()  # Obtener el rectángulo que delimita al obstáculo
        self.rect.bottom = SCREEN_HEIGHT - GROUND_HEIGHT  # Establecer la posición inicial del obstáculo en la parte inferior de la pantalla
        self.rect.left = SCREEN_WIDTH  # Establecer la posición inicial del obstáculo fuera de la pantalla

    def update(self):
        self.rect.x -= OBSTACLE_SPEED  # Mover el obstáculo hacia la izquierda

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Crear la pantalla del juego
        self.clock = pygame.time.Clock()  # Crear un reloj para controlar la velocidad de fotogramas
        self.all_sprites = pygame.sprite.Group()  # Grupo que contendrá todos los sprites del juego
        self.obstacles = pygame.sprite.Group()  # Grupo que contendrá solo los obstáculos del juego
        self.dinosaur = Dinosaur()  # Crear un objeto de dinosaurio
        self.all_sprites.add(self.dinosaur)  # Agregar el dinosaurio al grupo de todos los sprites
        self.next_obstacle_time = 0  # Tiempo para la aparición del próximo obstáculo
        self.closest_distance = float('inf')  # Inicializar la distancia más cercana como infinito (no hay obstáculos en pantalla)
        self.distances = []  # Lista para almacenar las distancias entre el dinosaurio y los obstáculos
        self.outcomes = []  # Lista para almacenar los resultados de los saltos del dinosaurio

    def run(self):
        running = True
        while running:
            self.clock.tick(30)  # Limitar el juego a 30 fotogramas por segundo
            for event in pygame.event.get():  # Manejar eventos del juego
                if event.type == pygame.QUIT:  # Verificar si se ha solicitado cerrar el juego
                    running = False

                elif event.type == pygame.KEYDOWN:  # Verificar si se ha presionado una tecla
                    if event.key == pygame.K_SPACE:  # Verificar si se ha presionado la tecla de espacio
                        self.dinosaur.jump()  # Hacer que el dinosaurio salte
                        self.check_jump_outcome()  # Verificar el resultado del salto

            self.all_sprites.update()  # Actualizar todos los sprites del juego

            current_time = pygame.time.get_ticks()  # Obtener el tiempo actual del juego en milisegundos
            if current_time > self.next_obstacle_time:  # Verificar si es tiempo de crear un nuevo obstáculo
                OBSTACLE_INTERVAL = random.randint(MIN_OBSTACLE_INTERVAL, MAX_OBSTACLE_INTERVAL)  # Calcular el intervalo de tiempo para el próximo obstáculo
                self.next_obstacle_time = current_time + OBSTACLE_INTERVAL  # Actualizar el tiempo para el próximo obstáculo
                obstacle = Obstacle()  # Crear un nuevo obstáculo
                self.all_sprites.add(obstacle)  # Agregar el obstáculo al grupo de todos los sprites
                self.obstacles.add(obstacle)  # Agregar el obstáculo al grupo de obstáculos

            if pygame.sprite.spritecollideany(self.dinosaur, self.obstacles):  # Verificar colisiones entre el dinosaurio y los obstáculos
                self.outcomes.append(0)  # Colisión
            else:
                self.outcomes.append(1)  # Salto exitoso

            self.screen.fill(WHITE)  # Llenar la pantalla con color blanco
            self.all_sprites.draw(self.screen)  # Dibujar todos los sprites en la pantalla
            pygame.display.flip()  # Actualizar la pantalla

        pygame.quit()  # Cerrar Pygame y salir del juego

    def check_jump_outcome(self):
        # Calcular la distancia entre
        # Calcular la distancia entre el dinosaurio y el obstáculo más cercano a la derecha
        self.closest_distance = float('inf')  # Restablecer la distancia más cercana
        for obstacle in self.obstacles:  # Iterar sobre todos los obstáculos en pantalla
            distance = obstacle.rect.left - self.dinosaur.rect.right  # Calcular la distancia entre el obstáculo y el borde derecho del dinosaurio
            if distance < self.closest_distance and distance > 0:  # Verificar si esta distancia es la más cercana hasta ahora y si el obstáculo está a la derecha del dinosaurio
                self.closest_distance = distance  # Actualizar la distancia más cercana

        # Guardar el resultado del salto (0 si colisiona, 1 si lo sortea)
        if self.closest_distance == float('inf'):  # Si no hay obstáculos a la derecha del dinosaurio
            self.outcomes.append(1)  # Se considera que el salto es exitoso
        elif self.closest_distance < 50:  # Si la distancia al obstáculo más cercano es menor que 50 (un valor arbitrario), se considera que hay una colisión
            self.outcomes.append(0)  # Se considera que hay una colisión
        else:
            self.outcomes.append(1)  # En otro caso, se considera que el salto es exitoso

        # Guardar la distancia recién calculada solo si hay un obstáculo a la derecha del dinosaurio
        if self.closest_distance != float('inf'):
            self.distances.append(self.closest_distance)  # Agregar la distancia a la lista de distancias

        # Imprimir las listas de resultados
        print("Colisiones:", self.outcomes)
        print("Distancias recogidas:", self.distances)

if __name__ == "__main__":
    game = Game()
    game.run()

