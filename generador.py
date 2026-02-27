import pygame
from objetivo import Objetivo
from configuracion import TIEMPO_APARICION_INICIAL

class Generador:
    def __init__(self, tiempo_espera=None, velocidad=None, radio_inicial=None):
        self.tiempo_espera = tiempo_espera or TIEMPO_APARICION_INICIAL
        self.velocidad = velocidad or 1.0
        self.radio_inicial = radio_inicial or 2.5
        self.acumulador_tiempo = 0.0

    def actualizar(self, dt, font_num):
        self.acumulador_tiempo += dt * 1000
        
        if self.acumulador_tiempo > self.tiempo_espera:
            self.acumulador_tiempo -= self.tiempo_espera
            return Objetivo(self.velocidad, self.radio_inicial, font_num)
            
        return None