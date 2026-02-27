import pygame
from configuracion import *

class HUD:
    """Esta clase se encarga de gestionar la información en pantalla como vidas y puntaje."""

    def __init__(self, modo):
        self.modo = modo
        self.puntos = 0
        self.vidas = VIDAS_NORMALES
        
        pygame.font.init()
        #Usamos fuentes del sistema
        self.font_puntos = pygame.font.SysFont("Arial", 38, bold=True)
        self.font_vidas = pygame.font.SysFont("Arial", 34, bold=True)

    def mostrar_juicio(self, texto, color):
        """Mantenemos la función para no romper main.py, pero la dejamos vacía (pass)."""
        pass

    def agregar_puntos(self, cantidad):
        """Esta funcion se encarga de acumular puntos."""
        self.puntos += cantidad

    def perder_vida(self):
        """Esta funcion se encarga de restar salud en el modo estandar."""
        self.vidas -= 1

    def sin_vidas(self):
        """Esta funcion se encarga de reportar un game over si la salud llega a cero."""
        return self.modo == MODO_NORMAL and self.vidas <= 0

    #Agregamos 'dt' (Delta Time) por exigencia del SDK
    def actualizar(self, dt):
        """Mantenemos la función vacía, pero recibe dt para mantener la compatibilidad arquitectónica."""
        pass

    def dibujar(self, superficie):
        """Esta funcion se encarga de estampar la interfaz sobre el juego activo."""
        texto_pts = self.font_puntos.render(f"Puntos: {self.puntos:,}", True, COLOR_TEXTO)
        superficie.blit(texto_pts, (16, 12))

        if self.modo == MODO_NORMAL:
            texto_vidas = self.font_vidas.render("♥ " * self.vidas, True, (220, 60, 60))
            superficie.blit(texto_vidas, (ANCHO - texto_vidas.get_width() - 16, 16))