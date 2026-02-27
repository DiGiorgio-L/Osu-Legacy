# 🎵 Osu! Legacy: Rhythm Arcade Edition

![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![Pygame](https://img.shields.io/badge/Pygame-2.6.0%2B-green)
![SDK](https://img.shields.io/badge/SDK-Arcade_Machine-red)

**Osu! Legacy** es un videojuego de ritmo dinámico desarrollado en Python. Este proyecto fue diseñado específicamente para ser integrado en la **Arcade Machine SDK**, cumpliendo con los estándares de arquitectura modular, manejo de rutas relativas y renderizado por Delta Time (`dt`) exigidos para el proyecto integrador.

---

## 📖 Descripción del Proyecto

Inspirado en los clásicos juegos de ritmo, el jugador debe usar el ratón para hacer clic en los objetivos (círculos) en el momento exacto en que el "anillo de aproximación" se cierra, sincronizado con el ritmo de la música. 

El juego implementa una arquitectura basada en **Máquina de Estados** (Menú -> Jugando -> GameOver) y delega el control del bucle principal (`Inversión de Control`) al *Core* del SDK de la máquina arcade.

### ✨ Características Principales
* **Múltiples Modos de Juego:** Juega en modo "Normal" (con 3 vidas) o "Infinito".
* **Dificultades Dinámicas:** Fácil, Normal y Difícil, que alteran la velocidad y la tasa de aparición de los círculos (BPM scaling).
* **Selector de Canciones:** Diferentes pistas musicales elegibles desde el menú.
* **VFX Completos:** Animaciones de explosión basadas en sprites, estela del cursor profesional y textos de juicio flotantes (Perfecto, Bien, Mal).
* **Independencia de FPS:** Todo el movimiento y las animaciones están multiplicadas por el `dt` (Delta Time) para garantizar que el ritmo nunca se pierda.

---

## 🛠️ Requisitos e Instalación

1. Clona este repositorio en tu máquina local.
2. Asegúrate de tener instalado **Python 3.11** o superior.
3. Instala las dependencias necesarias ejecutando:

\`\`\`bash
pip install -r requirements.txt
\`\`\`

*(El archivo requirements.txt incluye el `arcade-machine-sdk` y `pygame>=2.6.0`)*

---

## 🚀 Cómo Jugar (Ejecución Independiente)

Gracias al método `run_independently()` del SDK, el juego puede ser probado de forma autónoma simulando el entorno de la máquina arcade.

Desde la terminal, en la raíz del proyecto, ejecuta:
\`\`\`bash
python main.py
\`\`\`

### 🎮 Controles
* **Ratón (Movimiento):** Mueve la estela del cursor hacia los círculos.
* **Clic Izquierdo:** Golpea el círculo al ritmo de la música.
* **ESC:** Termina la partida actual o regresa al menú.

---

## 📂 Estructura del Proyecto

El código está refactorizado aplicando **Programación Orientada a Objetos (POO)**:
* `main.py`: Punto de entrada, contiene la clase `OsuLegacyGame` (hereda de `GameBase`) y la Máquina de Estados.
* `menu.py`: Maneja los selectores de dificultad, modos y música.
* `objetivo.py`: Lógica matemática de los anillos de aproximación y colisiones.
* `generador.py`: Spawner de objetivos basado en acumuladores de tiempo.
* `hud.py`: Renderizado de vidas y puntaje.
* `configuracion.py`: Constantes unificadas del SDK y manejo dinámico de rutas con `pathlib`.

---

## 🎓 Créditos Académicos
Desarrollado para la asignatura **Taller de Objetos y Abstracción de Datos** de la **Universidad de Oriente**.

* **Autores:** 
* **Grupo:** 1
* **Fecha de entrega:** Marzo 2026