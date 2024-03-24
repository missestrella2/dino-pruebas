############
'''

con ayuda de chatgpt, juego del dino de google
pero que cuente las vidas y las descuente cuando colisione

no funciona! necesita los jpg de los objetos


'''
############

import pygame
import random

# Inicializar Pygame
pygame.init()

# Definir colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)

# Definir las dimensiones de la ventana
ANCHO = 800
ALTO = 300

# Definir la velocidad del juego
VELOCIDAD = 6

# Definir la cantidad de vidas
VIDAS = 2000

# Crear la ventana del juego
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego del Dinosaurio")

# Cargar imágenes
dinosaurio_img = pygame.image.load('dino.png')
obstaculo_img = pygame.image.load('cactus.png')

# Obtener dimensiones de las imágenes
dino_ancho, dino_alto = dinosaurio_img.get_size()
obstaculo_ancho, obstaculo_alto = obstaculo_img.get_size()

# Definir la clase Dinosaurio
class Dinosaurio(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = dinosaurio_img
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = ALTO - dino_alto
        self.vidas = VIDAS

    def update(self):
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_SPACE] and self.rect.y == ALTO - dino_alto:
            self.rect.y -= VELOCIDAD
        elif self.rect.y < ALTO - dino_alto:
            self.rect.y += VELOCIDAD

# Definir la clase Obstáculo
class Obstaculo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = obstaculo_img
        self.rect = self.image.get_rect()
        self.rect.x = ANCHO
        self.rect.y = ALTO - obstaculo_alto

    def update(self):
        self.rect.x -= VELOCIDAD
        if self.rect.x < -obstaculo_ancho:
            self.rect.x = ANCHO
            self.rect.y = ALTO - obstaculo_alto

# Crear grupos de sprites
todos_los_sprites = pygame.sprite.Group()
obstaculos = pygame.sprite.Group()

# Crear el dinosaurio y agregarlo al grupo de sprites
dinosaurio = Dinosaurio()
todos_los_sprites.add(dinosaurio)

# Generar obstáculos y agregarlos al grupo de sprites
for i in range(2):
    obstaculo = Obstaculo()
    obstaculos.add(obstaculo)
    todos_los_sprites.add(obstaculo)

# Crear el reloj para controlar la velocidad de actualización del juego
reloj = pygame.time.Clock()

# Función principal del juego
def main():
    juego_terminado = False

    while not juego_terminado:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                juego_terminado = True

        # Detectar colisiones
        colisiones = pygame.sprite.spritecollide(dinosaurio, obstaculos, False)
        if colisiones:
            dinosaurio.vidas -= 1

        # Actualizar el juego
        todos_los_sprites.update()

        # Limpiar la pantalla
        ventana.fill(BLANCO)

        # Dibujar todos los sprites en la pantalla
        todos_los_sprites.draw(ventana)

        # Mostrar las vidas restantes
        fuente = pygame.font.SysFont(None, 36)
        texto = fuente.render(f'Vidas: {dinosaurio.vidas}', True, NEGRO)
        ventana.blit(texto, (10, 10))

        # Actualizar la ventana
        pygame.display.flip()

        # Controlar la velocidad de actualización del juego
        reloj.tick(30)

        # Terminar el juego si se quedan sin vidas
        if dinosaurio.vidas <= 0:
            juego_terminado = True

    pygame.quit()

if __name__ == "__main__":
    main()
