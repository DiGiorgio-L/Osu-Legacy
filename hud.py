import pygame
from configuracion import *

class HUD:
    def __init__(self, modo):
        self.modo = modo
        self.puntos = 0
        self.vidas = VIDAS_NORMALES
        
        pygame.font.init()
        self.font_puntos = pygame.font.SysFont("Arial", 38, bold=True)
        self.font_vidas = pygame.font.SysFont("Arial", 34, bold=True)

    def mostrar_juicio(self, texto, color):
        pass

    def agregar_puntos(self, cantidad):
        self.puntos += cantidad

    def perder_vida(self):
        self.vidas -= 1

    def sin_vidas(self):
        return self.modo == MODO_NORMAL and self.vidas <= 0

    def actualizar(self, dt):
        pass

    def dibujar(self, superficie):
        texto_pts = self.font_puntos.render(f"Puntos: {self.puntos:,}", True, COLOR_TEXTO)
        superficie.blit(texto_pts, (16, 12))

        if self.modo == MODO_NORMAL:
            texto_vidas = self.font_vidas.render("♥ " * self.vidas, True, (220, 60, 60))
            superficie.blit(texto_vidas, (ANCHO - texto_vidas.get_width() - 16, 16))