import pygame
from pathlib import Path
from configuracion import *

class Menu:
    def __init__(self, imagen_fondo=None, imagen_titulo=None):
        self.imagen_fondo = imagen_fondo
        self.imagen_titulo = imagen_titulo 

        pygame.font.init()
        self.font_titulo = pygame.font.SysFont("Arial", 56, bold=True)
        self.font_sub = pygame.font.SysFont("Arial", 22)
        self.font_opcion = pygame.font.SysFont("Arial", 30, bold=True)
        self.font_btn = pygame.font.SysFont("Arial", 32, bold=True)

        self.modos = [MODO_INFINITO, MODO_NORMAL]
        self.lbls_modo = ["Infinito", "Normal"]
        self.idx_modo = 0

        self.difs = ["facil", "normal", "dificil"]
        self.lbls_dif = ["Fácil", "Normal", "Difícil"]
        self.idx_dif = 1
        
        game_dir = Path(__file__).resolve().parent
        assets_dir = game_dir / "assets" / "sonidos"
        
        self.canciones = [
            {"nombre": "ILLEGAL LEGACY", "archivo": str(assets_dir / "cancion1.mp3")},
            {"nombre": "SILENT", "archivo": str(assets_dir / "cancion2.mp3")},
            {"nombre": "CYBER BEAT", "archivo": str(assets_dir / "cancion3.ogg")}
        ]
        self.lbls_cancion = [c["nombre"] for c in self.canciones]
        self.idx_cancion = 0

        self._tick = 0

        try:
            ruta_musica = str(assets_dir / "musica_menu.mp3")
            pygame.mixer.music.load(ruta_musica)
            pygame.mixer.music.set_volume(0.4)
            pygame.mixer.music.play(-1) 
        except Exception:
            pass

        try:
            ruta_img_btn = str(game_dir / "assets" / "imagenes" / "icono_jugar.png")
            img_raw = pygame.image.load(ruta_img_btn).convert_alpha()
            self.img_btn_jugar = pygame.transform.smoothscale(img_raw, (180, 40))
        except:
            self.img_btn_jugar = None
            
        self.cx = ANCHO // 2
        self.btn_jugar = pygame.Rect(self.cx - 110, ALTO - 240, 220, 54)
        
        self.fiz_m = self.fdc_m = pygame.Rect(0,0,0,0)
        self.fiz_d = self.fdc_d = pygame.Rect(0,0,0,0)
        self.fiz_c = self.fdc_c = pygame.Rect(0,0,0,0)

    def handle_events(self, events):
        for evento in events:
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                pos = evento.pos
                if self.fiz_m.collidepoint(pos): self.idx_modo = (self.idx_modo - 1) % len(self.modos)
                elif self.fdc_m.collidepoint(pos): self.idx_modo = (self.idx_modo + 1) % len(self.modos)
                elif self.fiz_d.collidepoint(pos): self.idx_dif = (self.idx_dif - 1) % len(self.difs)
                elif self.fdc_d.collidepoint(pos): self.idx_dif = (self.idx_dif + 1) % len(self.difs)
                elif self.fiz_c.collidepoint(pos): self.idx_cancion = (self.idx_cancion - 1) % len(self.canciones)
                elif self.fdc_c.collidepoint(pos): self.idx_cancion = (self.idx_cancion + 1) % len(self.canciones)
                elif self.btn_jugar.collidepoint(pos): 
                    pygame.mixer.music.stop()
                    return self.modos[self.idx_modo], self.difs[self.idx_dif], self.canciones[self.idx_cancion]["archivo"]
                    
            elif evento.type == pygame.KEYDOWN and evento.key in (pygame.K_RETURN, pygame.K_SPACE):
                pygame.mixer.music.stop()
                return self.modos[self.idx_modo], self.difs[self.idx_dif], self.canciones[self.idx_cancion]["archivo"]
        
        return None

    def actualizar(self, dt):
        self._tick += 1

    def dibujar(self, superficie):
        if self.imagen_fondo:
            superficie.blit(self.imagen_fondo, (0, 0))
            oscurecer = pygame.Surface((ANCHO, ALTO))
            oscurecer.set_alpha(100) 
            oscurecer.fill((0, 0, 0))
            superficie.blit(oscurecer, (0, 0))
        else:
            superficie.fill(COLOR_MENU_FONDO)

        if self.imagen_titulo:
            pos_x_titulo = self.cx - self.imagen_titulo.get_width() // 2
            superficie.blit(self.imagen_titulo, (pos_x_titulo, 30))
        else:
            titulo = self.font_titulo.render("OSU! LEGACY", True, COLOR_ACENTO)
            superficie.blit(titulo, (self.cx - titulo.get_width() // 2, 50))

        self.fiz_m, self.fdc_m = self._dibujar_selector(superficie, "Modo de Juego", self.lbls_modo, self.idx_modo, self.cx, 240)
        self.fiz_d, self.fdc_d = self._dibujar_selector(superficie, "Dificultad", self.lbls_dif, self.idx_dif, self.cx, 350) 
        self.fiz_c, self.fdc_c = self._dibujar_selector(superficie, "Música", self.lbls_cancion, self.idx_cancion, self.cx, 460) 

        col = COLOR_BOTON_HOVER if self.btn_jugar.collidepoint(pygame.mouse.get_pos()) else COLOR_BOTON
        pygame.draw.rect(superficie, col, self.btn_jugar, border_radius=12)
        pygame.draw.rect(superficie, COLOR_ACENTO, self.btn_jugar, 2, border_radius=12)
        
        if self.img_btn_jugar:
            rect_img = self.img_btn_jugar.get_rect(center=self.btn_jugar.center)
            superficie.blit(self.img_btn_jugar, rect_img)
        else:
            txt_btn = self.font_btn.render("▶  JUGAR", True, COLOR_ACENTO)
            superficie.blit(txt_btn, (self.btn_jugar.centerx - txt_btn.get_width() // 2, self.btn_jugar.centery - txt_btn.get_height() // 2))

    def _dibujar_selector(self, superficie, etiqueta, opciones, idx, cx, cy):
        fiz = pygame.Rect(cx - 180, cy - 18, 36, 36)
        fdc = pygame.Rect(cx + 144, cy - 18, 36, 36)

        pygame.draw.polygon(superficie, COLOR_ACENTO, [(fiz.right, fiz.top), (fiz.left + 8, fiz.centery), (fiz.right, fiz.bottom)])
        pygame.draw.polygon(superficie, COLOR_ACENTO, [(fdc.left, fdc.top), (fdc.right - 8, fdc.centery), (fdc.left, fdc.bottom)])

        texto = self.font_opcion.render(opciones[idx], True, COLOR_SELECCION)
        superficie.blit(texto, (cx - texto.get_width() // 2, cy - texto.get_height() // 2))

        lbl = self.font_sub.render(etiqueta, True, COLOR_TEXTO)
        superficie.blit(lbl, (cx - 180, cy - lbl.get_height() // 2 - 40))
        return fiz, fdc