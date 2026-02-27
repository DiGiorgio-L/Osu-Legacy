import pygame
from objetivo import Objetivo
from configuracion import TIEMPO_APARICION_INICIAL

class Generador:
    """Esta clase se encarga de instanciar nuevos objetivos respetando el tiempo de espera."""

    def __init__(self, tiempo_espera=None, velocidad=None, radio_inicial=None):
        self.tiempo_espera = tiempo_espera or TIEMPO_APARICION_INICIAL
        self.velocidad = velocidad or 1.0
        self.radio_inicial = radio_inicial or 2.5
        
        #reemplazamos pygame.time.get_ticks() por un acumulador
        self.acumulador_tiempo = 0.0

    #recibimos 'dt'
    def actualizar(self, dt, font_num):
        """Esta funcion se encarga de retornar un nuevo objetivo si el temporizador lo permite, o None."""
        #el SDK entrega 'dt' en segundos.
        self.acumulador_tiempo += dt * 1000
        
        if self.acumulador_tiempo > self.tiempo_espera:
            self.acumulador_tiempo -= self.tiempo_espera
            return Objetivo(self.velocidad, self.radio_inicial, font_num)
            
        return None