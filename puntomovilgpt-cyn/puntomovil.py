# hecho por chatgpt

import pygame
import sys

# Inicializar Pygame
pygame.init()

# Definir algunos colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)

# Definir el tamaño de la pantalla
ANCHO = 800
ALTO = 600

# Definir la velocidad de movimiento del punto
VELOCIDAD = 5

# Clase para el punto que se moverá en la pantalla
class Punto(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([10, 10])
        self.image.fill(BLANCO)
        self.rect = self.image.get_rect()
        self.rect.center = (ANCHO // 2, ALTO // 2)

    def update(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

# Función principal del juego
def main():
    # Configurar la pantalla
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Moviendo un punto")

    # Inicializar el reloj
    reloj = pygame.time.Clock()

    # Crear un sprite para el punto
    punto = Punto()

    # Crear un grupo de sprites
    todos_los_sprites = pygame.sprite.Group()
    todos_los_sprites.add(punto)

    # Bucle principal
    while True:
        # Manejar eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Obtener las teclas presionadas
        teclas = pygame.key.get_pressed()

        # Calcular el cambio en la posición del punto
        dx = 0
        dy = 0
        if teclas[pygame.K_LEFT]:
            dx = -VELOCIDAD
        if teclas[pygame.K_RIGHT]:
            dx = VELOCIDAD
        if teclas[pygame.K_UP]:
            dy = -VELOCIDAD
        if teclas[pygame.K_DOWN]:
            dy = VELOCIDAD

        # Actualizar la posición del punto
        punto.update(dx, dy)

        # Limpiar la pantalla
        pantalla.fill(NEGRO)

        # Dibujar todos los sprites en la pantalla
        todos_los_sprites.draw(pantalla)

        # Actualizar la pantalla
        pygame.display.flip()

        # Limitar la velocidad de fotogramas
        reloj.tick(60)

# Ejecutar la función principal del juego
if __name__ == "__main__":
    main()
