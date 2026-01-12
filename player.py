import pygame

class Jugador:
    def __init__(self, x, y):
        # --- CARGA DE ANIMACIONES ---
        ruta = "archivos/Sprites/Characters/purple/"
        
        self.sprites = {
            "idle": self.cargar_y_escalar(f"{ruta}idle.png"),
            "jump": self.cargar_y_escalar(f"{ruta}jump.png"),
            "down": self.cargar_y_escalar(f"{ruta}down.png"),
            "hit": self.cargar_y_escalar(f"{ruta}hit.png"),
            "walk": [
                self.cargar_y_escalar(f"{ruta}walk1.png"),
                self.cargar_y_escalar(f"{ruta}walk2.png")
            ]
        }
        
        self.imagen = self.sprites["idle"]
        self.rect = self.imagen.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # --- HITBOX DE PIES (Para no flotar) ---
        self.hitbox_pies = pygame.Rect(0, 0, 20, 10) 

        # --- FÍSICA ---
        self.velocidad_x = 0
        self.velocidad_y = 0
        self.gravedad = 0.8
        self.potencia_salto = -16
        self.velocidad_caminar = 6
        self.en_el_suelo = False

        # --- ANIMACIÓN ---
        self.mirando_derecha = True
        self.frame_walk = 0
        self.timer_walk = 0

        # --- INMUNIDAD ---
        self.invencible = False
        self.tiempo_invencible = 0
        self.duracion_inmunidad = 120 

    def cargar_y_escalar(self, ruta_archivo):
        img = pygame.image.load(ruta_archivo).convert_alpha()
        return pygame.transform.scale(img, (50, 50))

    def controles(self):
        keys = pygame.key.get_pressed()
        self.velocidad_x = 0
        
        # Al soltar las teclas, velocidad_x vuelve a 0, 
        # pero mirando_derecha MANTIENE su último valor.
        if keys[pygame.K_LEFT]:
            self.velocidad_x = -self.velocidad_caminar
            self.mirando_derecha = False
        elif keys[pygame.K_RIGHT]:
            self.velocidad_x = self.velocidad_caminar
            self.mirando_derecha = True

    def aplicar_fisica(self):
        self.velocidad_y += self.gravedad
        self.rect.x += self.velocidad_x
        self.rect.y += self.velocidad_y
        
        # Sincronizar hitbox de pies
        self.hitbox_pies.midbottom = self.rect.midbottom

        if self.rect.left < 0: self.rect.left = 0
        if self.rect.right > 800: self.rect.right = 800

    def saltar(self):
        if self.en_el_suelo: # <--- AGREGAR ESTA CONDICIÓN
            self.velocidad_y = self.potencia_salto
            self.en_el_suelo = False

    def rebotar(self):
        self.velocidad_y = self.potencia_salto // 2

    def recibir_daño(self):
        if not self.invencible:
            self.invencible = True
            self.tiempo_invencible = 0
            return True
        return False

    def actualizar_animacion(self):
        # 1. Determinar el estado visual
        if self.en_el_suelo or abs(self.velocidad_y) < 1.0:
            # ESTADO: SUELO
            if abs(self.velocidad_x) > 0.1:
                # Caminando
                self.timer_walk += 1
                if self.timer_walk > 8:
                    self.frame_walk = (self.frame_walk + 1) % 2
                    self.timer_walk = 0
                nueva_img = self.sprites["walk"][self.frame_walk]
            else:
                # Quieto
                nueva_img = self.sprites["idle"]
        else:
            # ESTADO: AIRE
            if self.velocidad_y < 0:
                # Subiendo (Salto)
                nueva_img = self.sprites["jump"]
            else:
                # Bajando (Caída) -> Aquí insertamos la animación "down"
                nueva_img = self.sprites["down"]

        # 2. Aplicar orientación (Flip)
        if not self.mirando_derecha:
            self.imagen = pygame.transform.flip(nueva_img, True, False)
        else:
            self.imagen = nueva_img

    def dibujar(self, pantalla):
        if self.invencible:
            if (self.tiempo_invencible // 5) % 2 == 0:
                pantalla.blit(self.imagen, self.rect)
        else:
            pantalla.blit(self.imagen, self.rect)