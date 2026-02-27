import pygame
import random
from configuracion import *

class Objetivo:
    """Esta clase se encarga de representar un círculo clickeable y su lógica visual."""

    def __init__(self, velocidad, radio_inicial, font_num):
        self.activo = True
        self.tocado = False
        
        self.image = pygame.Surface((RADIO_OBJETIVO * 2, RADIO_OBJETIVO * 2), pygame.SRCALPHA)
        self.rect  = self.image.get_rect()
        # ANCHO y ALTO ahora vienen del SDK
        self.rect.x = random.randint(50, ANCHO - 50 - self.rect.width)
        self.rect.y = random.randint(50, ALTO  - 50 - self.rect.height)

        centro = (RADIO_OBJETIVO, RADIO_OBJETIVO)
        pygame.draw.circle(self.image, (*COLOR_OBJETIVO, 160), centro, RADIO_OBJETIVO - 1)
        pygame.draw.circle(self.image, COLOR_OBJETIVO, centro, RADIO_OBJETIVO, GROSOR_LINEA)
        
        self.numero = 0
        self._font_num = font_num
        self.radio_anillo = RADIO_OBJETIVO * radio_inicial
        self.radio_inicial_anillo = self.radio_anillo
        self.velocidad = velocidad

    #recibimos 'dt' para que el ritmo nunca se desincronice
    def update(self, dt):
        """Esta funcion se encarga de encoger el anillo de aproximación usando Delta Time."""
        recorrido = self.radio_inicial_anillo - RADIO_OBJETIVO
        progreso = 1.0 - (self.radio_anillo - RADIO_OBJETIVO) / recorrido if recorrido > 0 else 1.0

        vel_actual = self.velocidad
        if progreso >= 0.5:
            t = (progreso - 0.5) / 0.5
            vel_actual *= (1.0 + 2.0 * t * t)

        #multiplicamos por (dt * 60) para compensar cualquier lag de la maquina arcade
        self.radio_anillo -= vel_actual * (dt * 60) 
        
        if self.radio_anillo <= RADIO_OBJETIVO:
            self.activo = False

    def dibujar_anillo(self, superficie):
        """Esta funcion se encarga de plasmar el anillo perimetral en pantalla."""
        if self.radio_anillo > RADIO_OBJETIVO:
            pygame.draw.circle(superficie, COLOR_ANILLO, self.rect.center, int(self.radio_anillo), 2)

    def dibujar_numero(self, superficie):
        """Esta funcion se encarga de renderizar el número asignado en el centro de la forma."""
        color_num = (255, 255, 255) if self.numero == 1 else (200, 200, 200)
        surf_num = self._font_num.render(str(self.numero), True, color_num)
        x = self.rect.centerx - surf_num.get_width()  // 2
        y = self.rect.centery - surf_num.get_height() // 2
        superficie.blit(surf_num, (x, y))

    def calcular_precision(self):
        """Esta funcion se encarga de retornar un flotante entre 0 y 1 según el momento del impacto."""
        recorrido = self.radio_inicial_anillo - RADIO_OBJETIVO
        if recorrido <= 0: return 0.0
        precision = 1.0 - ((self.radio_anillo - RADIO_OBJETIVO) / recorrido)
        return max(0.0, min(1.0, precision))

    def obtener_juicio(self):
        """Esta funcion se encarga de retornar el nivel de acierto, su color y puntos ganados."""
        p = self.calcular_precision()
        if p >= UMBRAL_PERFECTO: return "Perfecto", COLOR_PERFECTO, PUNTOS_JUICIO["Perfecto"]
        if p >= UMBRAL_BIEN: return "Bien", COLOR_BIEN, PUNTOS_JUICIO["Bien"]
        if p >= UMBRAL_REGULAR: return "Regular", COLOR_REGULAR, PUNTOS_JUICIO["Regular"]
        return "Mal", COLOR_MAL, PUNTOS_JUICIO["Mal"]

    def verificar_click(self, pos_mouse):
        """Esta funcion se encarga de confirmar si el ratón chocó con el rectángulo de la imagen."""
        return self.rect.collidepoint(pos_mouse)