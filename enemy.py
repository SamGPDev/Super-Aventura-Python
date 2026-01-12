import pygame
import math
import random

class Enemigo:
    def __init__(self, x, y, ancho_pantalla, alto_pantalla):
        # 1. Cargamos los frames de vuelo
        self.frame1 = pygame.image.load("archivos/Sprites/Enemies/Default/bee_a.png").convert_alpha()
        self.frame2 = pygame.image.load("archivos/Sprites/Enemies/Default/bee_b.png").convert_alpha()
        # 2. Cargamos la imagen de descanso/muerte
        self.img_muerta = pygame.image.load("archivos/Sprites/Enemies/Default/bee_rest.png").convert_alpha()
        
        # Escalado a 40x40
        self.frame1 = pygame.transform.scale(self.frame1, (40, 40))
        self.frame2 = pygame.transform.scale(self.frame2, (40, 40))
        self.img_muerta = pygame.transform.scale(self.img_muerta, (40, 40))
        
        self.frames_originales = [self.frame1, self.frame2]
        self.indice_animacion = 0
        self.imagen = self.frames_originales[self.indice_animacion]
        
        self.rect = self.imagen.get_rect(topleft=(x, y))
        
        self.ancho_pantalla = ancho_pantalla
        self.alto_pantalla = alto_pantalla
        
        self.vel_x = random.choice([-3, -4, 4, 3])
        self.vel_y = random.choice([-3,-2, 2, 3])
        
        self.contador_animacion = 0
        
        # --- NUEVOS ESTADOS ---
        self.esta_viva = True
        self.velocidad_caida = 0

    def morir(self):
        """Activa el estado de muerte y cambia la imagen."""
        if self.esta_viva:
            self.esta_viva = False
            self.imagen = self.img_muerta
            self.velocidad_caida = -5 # Pequeño salto hacia arriba al morir

    def animar(self):
        if self.esta_viva:
            self.contador_animacion += 0.15
            if self.contador_animacion >= len(self.frames_originales):
                self.contador_animacion = 0
            
            self.indice_animacion = int(self.contador_animacion)
            self.imagen = self.frames_originales[self.indice_animacion]
            
            # Volteo según dirección
            if self.vel_x > 0:
                self.imagen = pygame.transform.flip(self.imagen, True, False)
        else:
            # Si está muerta, mantenemos bee_rest y si caía hacia la derecha, mantenemos el flip
            self.imagen = self.img_muerta
            if self.vel_x > 0:
                self.imagen = pygame.transform.flip(self.imagen, True, False)

    def mover(self):
        if self.esta_viva:
            self.rect.x += self.vel_x
            
            # Movimiento "flotante": sumamos una onda senoidal a la velocidad base
            # Esto hace que suban y bajen suavemente mientras avanzan
            oscilacion = math.sin(pygame.time.get_ticks() * 0.005) * 2
            self.rect.y += self.vel_y + oscilacion
            
            # Rebote suave en techo y suelo
            if self.rect.top <= 0:
                self.rect.top = 1
                self.vel_y *= -1
            elif self.rect.bottom >= 500:
                self.rect.bottom = 499
                self.vel_y *= -1 
        else:
            # Gravedad al morir
            self.velocidad_caida += 0.5
            self.rect.y += self.velocidad_caida

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, self.rect)

    def actualizar(self, pantalla):
        self.mover()
        self.animar()
        self.dibujar(pantalla)