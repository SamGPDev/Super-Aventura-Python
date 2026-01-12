# Super Aventura Python - Arcade 2D

¡Bienvenido a **Super Aventura Python**! Un vibrante videojuego de plataformas y acción estilo arcade desarrollado con Python y Pygame. Enfréntate a enemigos voladores, salta entre plataformas y sobrevive el mayor tiempo posible para conseguir la puntuación más alta.

## 🎮 Descripción

Este proyecto es un juego de plataformas en 2D donde el jugador controla a un personaje dinámico a través de un escenario con gravedad y plataformas flotantes. El objetivo es sobrevivir al ataque constante de enemigos (abejas) que aparecen aleatoriamente, mientras se gestionan vidas y tiempo. El juego cuenta con un sistema de físicas personalizado, animaciones fluidas y una estructura robusta basada en estados.

## 🛠️ Tecnologías Utilizadas

- **Python 3.x**: Lenguaje principal de desarrollo.
- **Pygame**: Biblioteca para la gestión de gráficos, sonidos y eventos en tiempo real.

## ✨ Características Técnicas

El juego implementa diversas mecánicas y patrones de desarrollo de videojuegos:

- **Físicas Personalizadas**: Sistema de gravedad, inercia y colisiones precisas con el suelo y plataformas (incluyendo detección de hitboxes superiores e inferiores).
- **Sistema de Animación por Estados**: El personaje cambia visualmente según su acción (Idle, Walk, Jump, Fall, Hit) con animaciones de sprites.
- **Inteligencia Artificial de Enemigos**: Lógica de movimiento sinusoidal y generación aleatoria (spawning) de enemigos con velocidad y dirección variables.
- **Gestión de Estados de Juego**: Arquitectura basada en Máquina de Estados Finitos para manejar fluidamente:
  - **Menú Principal**: Pantalla de bienvenida.
  - **Juego**: Ejecución principal del bucle de juego.
  - **Pausa**: Suspensión temporal de la lógica.
  - **Game Over**: Pantalla de finalización y resumen de puntaje.
- **Sistema de Audio**: Música de fondo en bucle y efectos de sonido para acciones específicas (salto, golpe, daño).
- **HUD en Tiempo Real**: Visualización de Puntos, Tiempo Restante y Vidas.

## 🚀 Instrucciones de Instalación

1.  Asegúrate de tener Python 3.x instalado en tu sistema.
2.  Instala la librería **pygame**:
    ```bash
    python3 -m pip install pygame
    ```
3.  Ejecuta el juego desde el archivo principal:
    ```bash
    python3 main.py
    ```

## 🕹️ Controles

| Acción               | Tecla                      |
| :------------------- | :------------------------- |
| **Mover Izquierda**  | `Flecha Izquierda`         |
| **Mover Derecha**    | `Flecha Derecha`           |
| **Saltar / Iniciar** | `Espacio`                  |
| **Pausa**            | `P`                        |
| **Reiniciar Juego**  | `R` (En Pausa o Game Over) |

## 📂 Estructura del Proyecto

- **`main.py`**: Punto de entrada del juego. Contiene el bucle principal, la inicialización de Pygame, y la lógica central de estados.
- **`player.py`**: Define la clase `Jugador`. Maneja las físicas de movimiento, colisiones, lógica de invencibilidad y el gestor de animaciones.
- **`enemy.py`**: Contiene la clase `Enemigo`. Define el comportamiento, movimiento y ciclo de vida de los enemigos.
- **`menu.py`**: Módulo auxiliar para renderizar texto y dibujar las interfaces de Menú, Pausa y Game Over.
- **`game_states.py`**: Define las constantes para los diferentes estados del juego.
- **`archivos/`**: Directorio de recursos que contiene los _sprites_ (imágenes) y efectos de sonido.

## 🌟 Créditos

- **Desarrollo y Música**: Samuel García Palencia
  - _Email_: samuelgpmusic@gmail.com
  - _Música_: Composición original de Samuel García Palencia.
- **Arte y Assets**: Recursos gráficos obtenidos gratuitamente en **itch.io**.

---

_Desarrollado como proyecto de demostración de capacidades en Pygame._
