import pygame
from pathlib import Path
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS

ANCHO = SCREEN_WIDTH
ALTO = SCREEN_HEIGHT

COLOR_FONDO = (40, 65, 160)
COLOR_OBJETIVO = (0, 245, 255)
COLOR_ANILLO = (255, 40, 255)
COLOR_TEXTO = (255, 255, 255)

COLOR_PERFECTO = (255, 215, 0)
COLOR_BIEN = (80, 220, 80)
COLOR_REGULAR = (255, 165, 0)
COLOR_MAL = (220, 60, 60)

COLOR_MENU_FONDO = (15, 15, 25)
COLOR_ACENTO = (0, 220, 220)
COLOR_BOTON = (40, 40, 65)
COLOR_BOTON_HOVER = (60, 60, 100)
COLOR_SELECCION = (0, 180, 180)

RADIO_OBJETIVO = 40
MAX_CIRCULOS_PANTALLA = 4
GROSOR_LINEA = 3

MODO_INFINITO = "infinito"
MODO_NORMAL = "normal"

DIFICULTADES = {
    "facil":   {"velocidad": 0.8, "intervalo": 1000, "radio_inicial": 4.0, "max_circulos": 3},
    "normal":  {"velocidad": 1.3, "intervalo": 500,  "radio_inicial": 3.6, "max_circulos": 4},
    "dificil": {"velocidad": 1.9, "intervalo": 250,  "radio_inicial": 3.3, "max_circulos": 5},
}

UMBRAL_PERFECTO = 0.85
UMBRAL_BIEN = 0.60
UMBRAL_REGULAR = 0.35

PUNTOS_JUICIO = {
    "Perfecto": 300,
    "Bien": 100,
    "Regular": 50,
    "Mal": 10,
}

VIDAS_NORMALES = 3
TIEMPO_APARICION_INICIAL = 1200

GAME_DIR = Path(__file__).resolve().parent
ASSETS_DIR = GAME_DIR / "assets" / "imagenes"

RUTA_FONDO_MENU = ASSETS_DIR / "imagen_fondo_menu.png"     
RUTA_FONDO_JUEGO = ASSETS_DIR / "imagen_fondo_juego.png"   
RUTA_TITULO = ASSETS_DIR / "titulo_arcade.png"
RUTA_GAMEOVER = ASSETS_DIR / "icono_gameover.png"

def cargar_recursos():
    fondo_menu = None
    fondo_juego = None
    titulo = None
    gameover = None
    
    try:
        if RUTA_FONDO_MENU.exists():
            fondo_menu = pygame.image.load(str(RUTA_FONDO_MENU)).convert()
            fondo_menu = pygame.transform.scale(fondo_menu, (ANCHO, ALTO))

        if RUTA_FONDO_JUEGO.exists():
            fondo_juego = pygame.image.load(str(RUTA_FONDO_JUEGO)).convert()
            oscurecer = pygame.Surface((ANCHO, ALTO))
            oscurecer.set_alpha(150)
            oscurecer.fill((0, 0, 0))
            fondo_juego.blit(oscurecer, (0, 0))
            fondo_juego = pygame.transform.scale(fondo_juego, (ANCHO, ALTO))

        if RUTA_TITULO.exists():
            titulo = pygame.image.load(str(RUTA_TITULO)).convert_alpha()
            titulo = pygame.transform.scale(titulo, (400, 150)) 
            
        if RUTA_GAMEOVER.exists():
            gameover = pygame.image.load(str(RUTA_GAMEOVER)).convert_alpha()
            gameover = pygame.transform.smoothscale(gameover, (500, 120))

    except Exception:
        pass
    
    return fondo_menu, fondo_juego, titulo, gameover