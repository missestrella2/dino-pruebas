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

MODIFICACIONES V03:
- agregado de lista para recolectar si salto o no salto
- correccion de no pueda saltar en el aire

'''
##############

import pygame
import os
import random
import pickle

pygame.init()

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Listas para almacenar los datos recolectados
speed_records = []
distance_records = []
jump_records = []
collision_records = []

try:
    # Carga de imágenes
    RUNNING = [pygame.image.load(os.path.join("cyn -dino master modificado/dino v-01/Assets/Dino", "DinoRun1.png")),
               pygame.image.load(os.path.join("cyn -dino master modificado/dino v-01/Assets/Dino", "DinoRun2.png"))]
    JUMPING = pygame.image.load(os.path.join("cyn -dino master modificado/dino v-01/Assets/Dino", "DinoJump.png"))
    SMALL_CACTUS = [pygame.image.load(os.path.join("cyn -dino master modificado/dino v-01//Assets/Cactus", "SmallCactus1.png"))]
    CLOUD = pygame.image.load(os.path.join("cyn -dino master modificado/dino v-01//Assets/Other", "Cloud.png"))
    BG = pygame.image.load(os.path.join("cyn -dino master modificado/dino v-01//Assets/Other", "Track.png"))
except pygame.error as e:
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

def save_data():
    with open('game_data.py', 'w') as f:
        f.write("# Datos recolectados durante el juego\n\n")
        f.write("# Lista de velocidades de obstáculos\n")
        f.write("speed_records = {}\n".format(speed_records))
        f.write("\n")
        f.write("# Lista de distancias entre el dinosaurio y los obstáculos\n")
        f.write("distance_records = {}\n".format(distance_records))
        f.write("\n")
        f.write("# Lista de registros de saltos del dinosaurio\n")
        f.write("jump_records = {}\n".format(jump_records))
        f.write("\n")
        f.write("# Lista de registros de colisiones del dinosaurio con obstáculos\n")
        f.write("collision_records = {}\n".format(collision_records))
        f.write("\n")

def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles
    run = True
    clock = pygame.time.Clock()
    player = Dinosaur()
    cloud = Cloud()
    game_speed = 20
    x_pos_bg = 0
    y_pos_bg = 380
    points = 0
    font = pygame.font.Font('freesansbold.ttf', 20)
    obstacles = []
    death_count = 0

    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1
        text = font.render("Points: " + str(points), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (1000, 40)
        SCREEN.blit(text, textRect)

    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                save_data()  # Guarda los datos antes de salir del juego

        SCREEN.fill((255, 255, 255))
        userInput = pygame.key.get_pressed()

        player.draw(SCREEN)
        player.update(userInput)

        # Ajusta la posición del dinosaurio si cae por debajo del suelo
        if player.dino_rect.y > player.Y_POS:
            player.dino_rect.y = player.Y_POS

        if len(obstacles) == 0:
            if random.randint(0, 2) == 0:
                obstacles.append(SmallCactus(random.choice(SMALL_CACTUS)))
                # Registra la velocidad del obstáculo
                speed_records.append(game_speed)
                print("Speed Records:", speed_records)
                # Calcula la distancia entre el dinosaurio y el obstáculo
                distance_records.append(obstacles[0].rect.x - player.dino_rect.x)
                print("Distance Records:", distance_records)
                # Registra si el dinosaurio saltó o no después de pasar un obstáculo
                if player.dino_jump:
                    jump_records.append(True)
                    print("Jump Records:", jump_records)
                    player.dino_jump = False
                else:
                    jump_records.append(False)
                    print("Jump Records:", jump_records)

        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            if player.dino_rect.colliderect(obstacle.rect):
                death_count += 1
                # Registra si el dinosaurio chocó o no con el obstáculo
                collision_records.append(True)
                print("Collision Records:", collision_records)
            else:
                collision_records.append(False)
                print("Collision Records:", collision_records)

        # Verifica si el dinosaurio está en el suelo antes de permitirle saltar nuevamente
        if userInput[pygame.K_UP] and player.dino_rect.y == player.Y_POS:
            player.dino_jump = True

        background()

        cloud.draw(SCREEN)
        cloud.update()

        score()

        clock.tick(30)
        pygame.display.update()

if __name__ == "__main__":
    main()