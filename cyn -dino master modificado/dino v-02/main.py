#############
'''
sacado de https://github.com/maxontech/chrome-dinosaur.git

MODIFICACIONES V01:
- SOLO SALTA CACTUS chicos QUITE TODOS LOS CACTUS MEDIANO Y GRANDE Y LOS PAJAROS)
- CORREGI LA RUTA DE LAS IMAGENES PARA QUE LAS ENCUENTRE EN MI DIRECTORIO
- agregue try except para las imagenes por si hay algun error al cargar

MODIFICACIONES V02: 
- AGREGUE COMENTARIOS A LAS LINEAS
- le quite lineas para que NO MUERA (en el futuro lo usare para poner cantidad de vidas) 

'''
##############

import pygame  # Importa el módulo pygame para crear el juego
import os  # Importa el módulo os para manejar rutas de archivos
import random  # Importa el módulo random para generar números aleatorios

pygame.init()  # Inicializa pygame

# Constantes globales para el tamaño de la pantalla del juego
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Crea la pantalla del juego

# Intenta cargar las imágenes necesarias para el juego
try:
    # Carga las imágenes del dinosaurio corriendo
    RUNNING = [pygame.image.load(os.path.join("cyn -dino master modificado/dino v-01/Assets/Dino", "DinoRun1.png")),
               pygame.image.load(os.path.join("cyn -dino master modificado/dino v-01/Assets/Dino", "DinoRun2.png"))]
    # Carga la imagen del dinosaurio saltando
    JUMPING = pygame.image.load(os.path.join("cyn -dino master modificado/dino v-01/Assets/Dino", "DinoJump.png"))

    # Carga la imagen del cactus pequeño
    SMALL_CACTUS = [
        pygame.image.load(os.path.join("cyn -dino master modificado/dino v-01//Assets/Cactus", "SmallCactus1.png")),
    ]

    # Carga la imagen de la nube
    CLOUD = pygame.image.load(os.path.join("cyn -dino master modificado/dino v-01//Assets/Other", "Cloud.png"))

    # Carga la imagen del fondo del juego
    BG = pygame.image.load(os.path.join("cyn -dino master modificado/dino v-01//Assets/Other", "Track.png"))

except pygame.error as e:  # Maneja cualquier error al cargar las imágenes
    print("Error al cargar las imágenes:", e)

##################################################
# Clase que representa al dinosaurio en el juego
class Dinosaur:
    X_POS = 80  # Posición inicial en X del dinosaurio
    Y_POS = 310  # Posición inicial en Y del dinosaurio
    JUMP_VEL = 8.5  # Velocidad de salto del dinosaurio

    def __init__(self):
        self.run_img = RUNNING  # Imágenes del dinosaurio corriendo
        self.jump_img = JUMPING  # Imagen del dinosaurio saltando

        self.dino_run = True  # Bandera para indicar si el dinosaurio está corriendo
        self.dino_jump = False  # Bandera para indicar si el dinosaurio está saltando

        self.step_index = 0  # Índice para alternar entre las imágenes de correr
        self.jump_vel = self.JUMP_VEL  # Velocidad inicial de salto
        self.image = self.run_img[0]  # Imagen inicial del dinosaurio (corriendo)
        self.dino_rect = self.image.get_rect()  # Rectángulo que rodea al dinosaurio
        self.dino_rect.x = self.X_POS  # Posición X del rectángulo del dinosaurio
        self.dino_rect.y = self.Y_POS  # Posición Y del rectángulo del dinosaurio

    def update(self, userInput):
        if self.dino_run:  # Si el dinosaurio está corriendo
            self.run()  # Ejecutar el método para correr
        if self.dino_jump:  # Si el dinosaurio está saltando
            self.jump()  # Ejecutar el método para saltar

        if self.step_index >= 10:  # Si el índice de paso alcanza un valor límite
            self.step_index = 0  # Reiniciar el índice de paso

        # Verificar la entrada del usuario para determinar si el dinosaurio debe saltar
        if userInput[pygame.K_UP] and not self.dino_jump:
            self.dino_run = False  # El dinosaurio deja de correr
            self.dino_jump = True  # El dinosaurio comienza a saltar
        elif not self.dino_jump:
            self.dino_run = True  # Si no está saltando, el dinosaurio corre

    def run(self):
        # Actualiza la imagen del dinosaurio para que parezca que está corriendo
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()  # Actualiza el rectángulo del dinosaurio
        self.dino_rect.x = self.X_POS  # Posición X del rectángulo del dinosaurio
        self.dino_rect.y = self.Y_POS  # Posición Y del rectángulo del dinosaurio
        self.step_index += 1  # Incrementa el índice de paso

    def jump(self):
        # Actualiza la imagen del dinosaurio para que parezca que está saltando
        self.image = self.jump_img
        if self.dino_jump:  # Si el dinosaurio está saltando
            self.dino_rect.y -= self.jump_vel * 4  # Actualiza la posición Y del rectángulo del dinosaurio
            self.jump_vel -= 0.8  # Reduce la velocidad de salto
        if self.jump_vel < - self.JUMP_VEL:  # Si la velocidad de salto alcanza un límite negativo
            self.dino_jump = False  # El dinosaurio deja de saltar
            self.jump_vel = self.JUMP_VEL  # Restaura la velocidad de salto inicial

    def draw(self, SCREEN):
        # Dibuja la imagen del dinosaurio en la pantalla en la posición del rectángulo del dinosaurio
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))

##################################################
# Clase que representa una nube en el juego
class Cloud:
    def __init__(self):
        # Define la posición inicial aleatoria de la nube fuera de la pantalla
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = CLOUD  # Imagen de la nube
        self.width = self.image.get_width()  # Ancho de la imagen de la nube

    def update(self):
        # Actualiza la posición de la nube y vuelve a colocarla fuera de la pantalla cuando sale del lado izquierdo
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, SCREEN):
        # Dibuja la imagen de la nube en la pantalla en su posición actual
        SCREEN.blit(self.image, (self.x, self.y))

##################################################
# Clase base para los obstáculos en el juego
class Obstacle:
    def __init__(self, image):
        self.image = image  # Imagen del obstáculo
        self.rect = self.image.get_rect()  # Rectángulo que rodea al obstáculo
        self.rect.x = SCREEN_WIDTH  # Posición inicial en X fuera de la pantalla

    def update(self):
        # Actualiza la posición del obstáculo y lo elimina de la lista cuando sale del lado izquierdo
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):
        # Dibuja el obstáculo en la pantalla en su posición actual
        SCREEN.blit(self.image, self.rect)

##################################################
# Clase que representa un cactus pequeño como obstáculo
class SmallCactus(Obstacle):
    def __init__(self, image):
        super().__init__(image)  # Inicializa la clase base con la imagen del cactus
        self.rect.y = 325  # Posición Y del cactus pequeño

##################################################
# Función principal del juego
def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles
    run = True  # Variable para controlar el bucle principal del juego
    clock = pygame.time.Clock()  # Reloj para controlar la velocidad del juego
    player = Dinosaur()  # Instancia del dinosaurio
    cloud = Cloud()  # Instancia de la nube
    game_speed = 20  # Velocidad inicial del juego
    x_pos_bg = 0  # Posición inicial del fondo en X
    y_pos_bg = 380  # Posición inicial del fondo en Y
    points = 0  # Puntuación inicial del jugador
    font = pygame.font.Font('freesansbold.ttf', 20)  # Fuente para mostrar la puntuación
    obstacles = []  # Lista para almacenar los obstáculos
    death_count = 0  # Contador de muertes del jugador

    # Función para mostrar la puntuación del jugador
    def score():
        global points, game_speed
        points += 1  # Incrementa la puntuación en 1
        if points % 100 == 0:  # Aumenta la velocidad del juego cada 100 puntos
            game_speed += 1

        # Renderiza el texto de la puntuación en la pantalla
        text = font.render("Points: " + str(points), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (1000, 40)
        SCREEN.blit(text, textRect)

    # Función para dibujar el fondo del juego
    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed

    # Bucle principal del juego
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        SCREEN.fill((255, 255, 255))  # Rellena la pantalla con un color blanco
        userInput = pygame.key.get_pressed()  # Obtiene la entrada del usuario

        player.draw(SCREEN)  # Dibuja al dinosaurio en la pantalla
        player.update(userInput)  # Actualiza el estado del dinosaurio

        if len(obstacles) == 0:  # Si no hay obstáculos en la pantalla
            if random.randint(0, 2) == 0:  # Genera aleatoriamente un nuevo obstáculo (cactus pequeño)
                obstacles.append(SmallCactus(random.choice(SMALL_CACTUS)))

        for obstacle in obstacles:  # Para cada obstáculo en la lista de obstáculos
            obstacle.draw(SCREEN)  # Dibuja el obstáculo en la pantalla
            obstacle.update()  # Actualiza la posición del obstáculo
            if player.dino_rect.colliderect(obstacle.rect):  # Si el dinosaurio choca con el obstáculo
                pygame.time.delay(2000)  # Espera 2 segundos antes de continuar
                death_count += 1  # Incrementa el contador de muertes
                #menu(death_count)  # Muestra el menú de reinicio del juego

        background()  # Dibuja el fondo del juego

        cloud.draw(SCREEN)  # Dibuja la nube en la pantalla
        cloud.update()  # Actualiza la posición de la nube

        score()  # Actualiza y muestra la puntuación del jugador en la pantalla

        clock.tick(30)  # Limita el juego a 30 FPS
        pygame.display.update()  # Actualiza la pantalla

##################################################
# Función que muestra el menú de reinicio del juego
def menu(death_count):
    global points
    run = True
    while run:
        SCREEN.fill((255, 255, 255))  # Rellena la pantalla con un color blanco
        font = pygame.font.Font('freesansbold.ttf', 30)  # Define la fuente del texto

        if death_count == 0:  # Si el jugador no ha muerto
            text = font.render("Press any Key to Start", True, (0, 0, 0))  # Muestra el mensaje de inicio
        elif death_count > 0:  # Si el jugador ha muerto al menos una vez
            text = font.render("Press any Key to Restart", True, (0, 0, 0))  # Muestra el mensaje de reinicio
            score = font.render("Your Score: " + str(points), True, (0, 0, 0))  # Muestra la puntuación del jugador
            scoreRect = score.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            SCREEN.blit(score, scoreRect)  # Dibuja la puntuación en la pantalla
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        SCREEN.blit(text, textRect)  # Dibuja el texto en la pantalla
        SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 140))  # Dibuja al dinosaurio en el menú
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.KEYDOWN:
                main()  # Reinicia el juego al presionar cualquier tecla


menu(death_count=0)  # Llama a la función del menú para iniciar
