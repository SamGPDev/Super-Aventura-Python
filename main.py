import pygame
import sys
import random
import game_states as estados
import menu
from player import Jugador
from enemy import Enemigo

# --- 1. CONFIGURACIÓN DE AUDIO ---
try:
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.init()
except Exception as e:
    pygame.init()

# --- 2. CONFIGURACIÓN DE VENTANA ---
ANCHO, ALTO = 800, 600
NIVEL_SUELO = 500 
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Mi Super Juego Arcade")
reloj = pygame.time.Clock()

# --- 3. CARGA DE RECURSOS ---
ruta_musica = "archivos/sounds/sountrackpy.wav"
musica_cargada = False

if pygame.mixer.get_init():
    try:
        pygame.mixer.music.load(ruta_musica)
        pygame.mixer.music.set_volume(0.6)
        musica_cargada = True
    except:
        pass

try:
    sonido_salto = pygame.mixer.Sound("archivos/sounds/salto.ogg")
    sonido_golpe = pygame.mixer.Sound("archivos/sounds/golpe.ogg")
    sonido_danio = pygame.mixer.Sound("archivos/sounds/daño.ogg")
    sonido_pausa = pygame.mixer.Sound("archivos/sounds/pausa.ogg")
except:
    print("⚠️ Revisa que los archivos .ogg estén en archivos/sounds/")

img_fondo = pygame.image.load("archivos/Sprites/Backgrounds/fondo.png").convert()
img_fondo = pygame.transform.scale(img_fondo, (ANCHO, ALTO))

# Suelo
img_pasto_izq = pygame.image.load("archivos/Sprites/Tiles/izquierda.png").convert_alpha()
img_pasto_centro = pygame.image.load("archivos/Sprites/Tiles/centro.png").convert_alpha()
img_pasto_der = pygame.image.load("archivos/Sprites/Tiles/derecha.png").convert_alpha()
img_inferior_izq = pygame.image.load("archivos/Sprites/Tiles/inferiorleft.png").convert_alpha()
img_inferior_centro = pygame.image.load("archivos/Sprites/Tiles/inferior.png").convert_alpha()
img_inferior_der = pygame.image.load("archivos/Sprites/Tiles/inferiorright.png").convert_alpha()

img_pasto_izq = pygame.transform.scale(img_pasto_izq, (50, 50))
img_pasto_centro = pygame.transform.scale(img_pasto_centro, (50, 50))
img_pasto_der = pygame.transform.scale(img_pasto_der, (50, 50))
img_inferior_izq = pygame.transform.scale(img_inferior_izq, (50, 50))
img_inferior_centro = pygame.transform.scale(img_inferior_centro, (50, 50))
img_inferior_der = pygame.transform.scale(img_inferior_der, (50, 50))

# Plataformas
img_plat_izq = pygame.image.load("archivos/Sprites/Tiles/platiz.png").convert_alpha()
img_plat_centro = pygame.image.load("archivos/Sprites/Tiles/platcentro.png").convert_alpha()
img_plat_der = pygame.image.load("archivos/Sprites/Tiles/platder.png").convert_alpha()

dict_plat = {
    'izq': pygame.transform.scale(img_plat_izq, (50, 50)),
    'centro': pygame.transform.scale(img_plat_centro, (50, 50)),
    'der': pygame.transform.scale(img_plat_der, (50, 50))
}

class Plataforma(pygame.sprite.Sprite):
    def __init__(self, x, y, ancho, imagenes):
        super().__init__()
        self.image = pygame.Surface((ancho, 50), pygame.SRCALPHA)
        tile_size = 50
        for i in range(0, ancho, tile_size):
            if i == 0:
                self.image.blit(imagenes['izq'], (i, 0))
            elif i >= ancho - tile_size:
                self.image.blit(imagenes['der'], (i, 0))
            else:
                self.image.blit(imagenes['centro'], (i, 0))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.hitbox = pygame.Rect(x, y, ancho, 15) # Hitbox ligeramente más alta

    def dibujar(self, pantalla):
        pantalla.blit(self.image, self.rect)

# --- 4. FUNCIONES DE APOYO ---
def pintar_suelo(superficie):
    tamanio = 50
    for x in range(0, ANCHO, tamanio):
        if x == 0:
            superficie.blit(img_pasto_izq, (x, NIVEL_SUELO))
        elif x >= ANCHO - tamanio:
            superficie.blit(img_pasto_der, (x, NIVEL_SUELO))
        else:
            superficie.blit(img_pasto_centro, (x, NIVEL_SUELO))
        
        for y_relleno in range(NIVEL_SUELO + tamanio, ALTO, tamanio):
            if x == 0:
                superficie.blit(img_inferior_izq, (x, y_relleno))
            elif x >= ANCHO - tamanio:
                superficie.blit(img_inferior_der, (x, y_relleno))
            else:
                superficie.blit(img_inferior_centro, (x, y_relleno))

def reiniciar_juego():
    jugador = Jugador(100, 450)
    
    # Enemigos iniciales
    enemigos = []
    for i in range(3):
        x_ini = random.randint(200, ANCHO - 50)
        y_ini = random.randint(100, 300)
        enemigos.append(Enemigo(x_ini, y_ini, ANCHO, ALTO))
        
    # SOLO 3 PLATAFORMAS
    plataformas = [
        Plataforma(50, 350, 200, dict_plat),   # Lateral izquierda (más alta)
        Plataforma(550, 350, 200, dict_plat),  # Lateral derecha (más alta)
        Plataforma(300, 200, 200, dict_plat)   # Centro arriba
    ]
    return jugador, enemigos, plataformas, 60, 3

# --- 5. VARIABLES DE INICIO ---
jugador, enemigos, plataformas, tiempo_restante, vidas_restantes = reiniciar_juego()
estado_actual = estados.MENU
puntos = 0
ejecutando = True
frames_contados = 0 
timer_aparicion = 0 

# --- 6. LOOP PRINCIPAL ---
while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

        if evento.type == pygame.KEYDOWN:
            if estado_actual == estados.PLAYING and evento.key == pygame.K_SPACE:

                if jugador.en_el_suelo:
                    if 'sonido_salto' in locals(): 
                        sonido_salto.play()
                jugador.saltar()

            if estado_actual == estados.MENU and evento.key == pygame.K_SPACE:
                jugador, enemigos, plataformas, tiempo_restante, vidas_restantes = reiniciar_juego()
                puntos = 0
                if musica_cargada:
                    pygame.mixer.music.play(-1)
                estado_actual = estados.PLAYING

            elif evento.key == pygame.K_r:
                if estado_actual in [estados.PAUSE, estados.GAME_OVER]:
                    jugador, enemigos, plataformas, tiempo_restante, vidas_restantes = reiniciar_juego()
                    puntos = 0
                    if musica_cargada:
                        pygame.mixer.music.play(-1)
                    estado_actual = estados.PLAYING
            
            elif evento.key == pygame.K_p:
                if 'sonido_pausa' in locals(): sonido_pausa.play()
                if estado_actual == estados.PLAYING:
                    pygame.mixer.music.pause()
                    estado_actual = estados.PAUSE
                elif estado_actual == estados.PAUSE:
                    pygame.mixer.music.unpause()
                    estado_actual = estados.PLAYING

    if estado_actual == estados.MENU:
        menu.mostrar_inicio(pantalla, ANCHO, ALTO)

    elif estado_actual == estados.PLAYING:
        frames_contados += 1
        if frames_contados >= 60:
            tiempo_restante -= 1
            frames_contados = 0
        
        if tiempo_restante <= 0:
            estado_actual = estados.GAME_OVER

        # --- LÓGICA DE APARICIÓN ---
        if len(enemigos) < 10:  
            timer_aparicion += 1
            if timer_aparicion >= 50:  # Bajamos de 120 a 50 (Mucho más frecuente)
                lado = random.choice(["izq", "der"])
                if lado == "izq":
                    x_spawn, direccion = -60, 1
                else:
                    x_spawn, direccion = ANCHO + 60, -1

                y_spawn = random.randint(50, 300)
                nueva_abeja = Enemigo(x_spawn, y_spawn, ANCHO, ALTO)
                if hasattr(nueva_abeja, 'vel_x'):
                    nueva_abeja.vel_x = abs(nueva_abeja.vel_x) * direccion
                
                enemigos.append(nueva_abeja)
                timer_aparicion = 0

        #fondo
    
        pantalla.blit(img_fondo, (0, 0))
        pintar_suelo(pantalla)

        # --- FÍSICA Y COLISIONES ---
        jugador.controles()
        jugador.aplicar_fisica() 
        
        # 1. Suelo base (Detección inicial)
        if jugador.rect.bottom >= NIVEL_SUELO:
            jugador.rect.bottom = NIVEL_SUELO
            jugador.velocidad_y = 0
            jugador.en_el_suelo = True
        else:
            jugador.en_el_suelo = False 

        # 2. DIBUJO DE PLATAFORMAS (Primero dibujamos todas para evitar parpadeo)
        for plat in plataformas:
            plat.dibujar(pantalla)

        # 3. LÓGICA DE COLISIÓN EN PLATAFORMAS (Separada del dibujo)
        for plat in plataformas:
            # Colisión para el Jugador
            if jugador.velocidad_y >= 0:
                if jugador.hitbox_pies.colliderect(plat.hitbox):
                    if jugador.rect.bottom <= plat.rect.top + 15:
                        jugador.rect.bottom = plat.rect.top
                        jugador.velocidad_y = 0
                        jugador.en_el_suelo = True
                        # No usamos break aquí para permitir que los enemigos también procesen
            
            # Rebote de enemigos en plataformas 
            for enemigo in enemigos:
                if enemigo.esta_viva and enemigo.rect.colliderect(plat.rect):
                    # Invertimos dirección
                    enemigo.vel_y *= -1
                    
                    # SEPARACIÓN FÍSICA: La sacamos de la plataforma según hacia dónde iba
                    if enemigo.vel_y > 0: 
                        # Si ahora va hacia abajo, es que chocó con la parte inferior
                        enemigo.rect.top = plat.rect.bottom + 1
                    else: 
                        # Si ahora va hacia arriba, es que chocó con la parte superior
                        enemigo.rect.bottom = plat.rect.top - 1

        jugador.actualizar_animacion()

        if jugador.invencible:
            jugador.tiempo_invencible += 1
            if jugador.tiempo_invencible >= jugador.duracion_inmunidad:
                jugador.invencible = False
        jugador.dibujar(pantalla)
        
        # 5. LÓGICA DE ENEMIGOS (Con limpieza de bordes laterales)
        for enemigo in enemigos[:]:
            enemigo.actualizar(pantalla)
            
            # ELIMINACIÓN: Si salen por los lados o abajo
            if enemigo.rect.x < -200 or enemigo.rect.x > ANCHO + 200 or enemigo.rect.top > ALTO:
                enemigos.remove(enemigo)
                continue

            if enemigo.esta_viva and jugador.rect.colliderect(enemigo.rect):
                if jugador.velocidad_y > 0 and jugador.rect.bottom < enemigo.rect.centery + 10:
                    if 'sonido_golpe' in locals(): sonido_golpe.play()
                    enemigo.morir()
                    jugador.rebotar()
                    puntos += 10
                else:
                    if jugador.recibir_daño():
                        if 'sonido_danio' in locals(): sonido_danio.play()
                        vidas_restantes -= 1
                        if vidas_restantes <= 0:
                            estado_actual = estados.GAME_OVER
                        else:
                            jugador.rect.x, jugador.rect.y = 100, 450
                            jugador.velocidad_y = 0

        # HUD
        menu.escribir_texto(pantalla, f"Puntos: {puntos}", 25, (0, 0, 0), 80, 30)
        color_reloj = (0, 0, 0) if tiempo_restante > 10 else (200, 0, 0)
        menu.escribir_texto(pantalla, f"Tiempo: {tiempo_restante}", 25, color_reloj, ANCHO // 2, 30)
        menu.escribir_texto(pantalla, f"Vidas: {vidas_restantes}", 25, (200, 0, 0), ANCHO - 80, 30)

    elif estado_actual == estados.PAUSE:
        menu.mostrar_pausa(pantalla, ANCHO, ALTO)
    elif estado_actual == estados.GAME_OVER:
        menu.mostrar_fin_juego(pantalla, ANCHO, ALTO, puntos)

    pygame.display.flip()
    reloj.tick(60)

pygame.quit()
sys.exit()