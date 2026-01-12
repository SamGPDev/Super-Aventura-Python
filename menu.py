import pygame

# Definimos algunos colores básicos para usar en el menú
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
AMARILLO = (255, 215, 0)

def escribir_texto(pantalla, texto, tamaño, color, x, y):
    """
    Función auxiliar para dibujar texto de forma sencilla.
    Cambiamos SysFont por Font(None) para asegurar compatibilidad en Mac.
    """
    # None cargará la fuente por defecto de Pygame
    fuente = pygame.font.Font(None, tamaño)
    superficie_texto = fuente.render(texto, True, color)
    rectangulo_texto = superficie_texto.get_rect()
    rectangulo_texto.center = (x, y)
    pantalla.blit(superficie_texto, rectangulo_texto)

def mostrar_inicio(pantalla, ancho, alto):
    """Dibuja la pantalla de bienvenida."""
    pantalla.fill((50, 50, 150)) # Azul oscuro
    
    escribir_texto(pantalla, "SUPER AVENTURA PYTHON", 60, AMARILLO, ancho // 2, alto // 3)
    escribir_texto(pantalla, "Presiona ESPACIO para comenzar", 35, BLANCO, ancho // 2, alto // 2 + 50)
    escribir_texto(pantalla, "Flechas: Mover | P: Pausa", 25, BLANCO, ancho // 2, alto - 50)

def mostrar_fin_juego(pantalla, ancho, alto, puntuacion):
    """Dibuja la pantalla cuando el jugador pierde."""
    pantalla.fill((150, 0, 0)) # Rojo
    
    escribir_texto(pantalla, "GAME OVER", 80, BLANCO, ancho // 2, alto // 3)
    escribir_texto(pantalla, f"Puntos totales: {puntuacion}", 40, AMARILLO, ancho // 2, alto // 2)
    escribir_texto(pantalla, "Presiona R para reiniciar", 30, BLANCO, ancho // 2, alto // 2 + 100)

def mostrar_pausa(pantalla, ancho, alto):
    """Dibuja una capa de pausa semitransparente sobre el juego."""
    # Creamos la superficie para la transparencia
    superficie_overlay = pygame.Surface((ancho, alto), pygame.SRCALPHA)
    superficie_overlay.fill((0, 0, 0, 180)) # Un poco más oscuro para que resalte
    pantalla.blit(superficie_overlay, (0, 0))
    
    escribir_texto(pantalla, "PAUSA", 70, AMARILLO, ancho // 2, alto // 3)
    escribir_texto(pantalla, "P para continuar", 35, BLANCO, ancho // 2, alto // 2)
    escribir_texto(pantalla, "R para reiniciar", 25, BLANCO, ancho // 2, alto // 2 + 70)