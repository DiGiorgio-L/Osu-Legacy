import pygame
import sys
from pathlib import Path

#IMPORTACIONES DEL SDK
from arcade_machine_sdk import GameBase, GameMeta

from configuracion import *
from generador import Generador
from hud import HUD
from menu import Menu


# CLASES DE EFECTOS VISUALES
class EfectoVisual(pygame.sprite.Sprite):
    def __init__(self, centro, frames_lista):
        super().__init__()
        self.frames = frames_lista 
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=centro)
        
        self.acumulador = 0.0
        self.velocidad_animacion = 30 # milisegundos por frame

    def update(self, dt):
        self.acumulador += dt * 1000
        if self.acumulador > self.velocidad_animacion:
            self.acumulador -= self.velocidad_animacion
            self.frame_index += 1
            if self.frame_index < len(self.frames):
                self.image = self.frames[self.frame_index]
                self.rect = self.image.get_rect(center=self.rect.center)
            else:
                self.kill() 

class TextoFlotante(pygame.sprite.Sprite):
    def __init__(self, posicion, texto, color, fuente):
        super().__init__()
        self.image_original = fuente.render(texto, True, color)
        self.image = self.image_original.copy()
        self.rect = self.image.get_rect(center=posicion)
        
        self.alpha = 255 
        self.pos_y = float(self.rect.y)

    def update(self, dt):
        # Mover hacia arriba
        self.pos_y -= 120 * dt
        self.rect.y = int(self.pos_y)
        
        # Reducir opacidad
        self.alpha -= 300 * dt
        
        if self.alpha <= 0:
            self.kill() 
        else:
            self.image = self.image_original.copy()
            self.image.set_alpha(int(self.alpha))                

# PANTALLA GAMEOVER 
class PantallaGameOver:
    def __init__(self, puntos, imagen_fondo=None, imagen_gameover=None):
        self.puntos = puntos
        self.imagen_fondo = imagen_fondo
        self.imagen_gameover = imagen_gameover
        
        pygame.font.init()
        self.font_grande = pygame.font.SysFont("Arial", 72, bold=True)
        self.font_normal = pygame.font.SysFont("Arial", 40, bold=True)
        self.font_pequena = pygame.font.SysFont("Arial", 32)

        self.btn_menu = pygame.Rect(ANCHO // 2 - 160, ALTO // 2 + 80, 140, 56)
        self.btn_salir = pygame.Rect(ANCHO // 2 + 20, ALTO // 2 + 80, 140, 56)

    def handle_events(self, events):
        for evento in events:
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if self.btn_menu.collidepoint(evento.pos): return "MENU"
                if self.btn_salir.collidepoint(evento.pos): return "SALIR"
        return None

    def actualizar(self, dt):
        pass

    def dibujar(self, superficie):
        if self.imagen_fondo:
            superficie.blit(self.imagen_fondo, (0, 0))
            overlay = pygame.Surface((ANCHO, ALTO))
            overlay.set_alpha(150) 
            overlay.fill((0, 0, 0))
            superficie.blit(overlay, (0, 0))
        else:
            superficie.fill(COLOR_MENU_FONDO)
        
        if self.imagen_gameover:
            rect_go = self.imagen_gameover.get_rect(center=(ANCHO // 2, ALTO // 2 - 140))
            superficie.blit(self.imagen_gameover, rect_go)
        else:
            surf_go = self.font_grande.render("GAME OVER", True, (220, 60, 60))
            superficie.blit(surf_go, (ANCHO // 2 - surf_go.get_width() // 2, ALTO // 2 - 140))
        
        surf_pts = self.font_normal.render(f"Puntaje final: {self.puntos:,}", True, COLOR_TEXTO)
        superficie.blit(surf_pts, (ANCHO // 2 - surf_pts.get_width() // 2, ALTO // 2 - 30))

        mouse = pygame.mouse.get_pos()
        
        #Botn Menu
        pygame.draw.rect(superficie, COLOR_BOTON_HOVER if self.btn_menu.collidepoint(mouse) else COLOR_BOTON, self.btn_menu, border_radius=12)
        pygame.draw.rect(superficie, COLOR_ACENTO, self.btn_menu, 2, border_radius=12)
        tm = self.font_pequena.render("Menú", True, COLOR_ACENTO)
        superficie.blit(tm, (self.btn_menu.centerx - tm.get_width() // 2, self.btn_menu.centery - tm.get_height() // 2))

        #Boton Salir
        pygame.draw.rect(superficie, COLOR_BOTON_HOVER if self.btn_salir.collidepoint(mouse) else COLOR_BOTON, self.btn_salir, border_radius=12)
        pygame.draw.rect(superficie, (220, 60, 60), self.btn_salir, 2, border_radius=12)
        ts = self.font_pequena.render("Salir", True, (220, 60, 60))
        superficie.blit(ts, (self.btn_salir.centerx - ts.get_width() // 2, self.btn_salir.centery - ts.get_height() // 2))


# Adaptada a la arquitectura del SDK

class Juego:
    def __init__(self, modo, dificultad, ruta_cancion, imagen_fondo=None):
        self.modo = modo
        self.imagen_fondo = imagen_fondo
        
        cfg_dif = DIFICULTADES[dificultad] 
        self.max_circulos = cfg_dif["max_circulos"]
        self.generador = Generador(cfg_dif["intervalo"], cfg_dif["velocidad"], cfg_dif["radio_inicial"])
        
        self.sprites_lista = []
        self.hud = HUD(modo)
        self.ejecutando = True
        
        pygame.mouse.set_visible(False)
        self.estela_raton = [] 

        self.frames_explosion = []
        try:
            game_dir = Path(__file__).resolve().parent
            for i in range(12): 
                ruta_anim = str(game_dir / "assets" / "imagenes" / "animaciones" / f"animacion_{i}.png")
                img = pygame.image.load(ruta_anim).convert_alpha()
                img = pygame.transform.scale(img, (150, 150)) 
                self.frames_explosion.append(img)
        except:
            self.frames_explosion = []

        self.vfx_group = pygame.sprite.Group() 
        
        try:
            ruta_cursor = str(Path(__file__).resolve().parent / "assets" / "imagenes" / "cursor.png")
            img_cursor_raw = pygame.image.load(ruta_cursor).convert_alpha()
            self.img_cursor = pygame.transform.smoothscale(img_cursor_raw, (30, 30))
        except:
            self.img_cursor = None 
        
        pygame.font.init()
        self.font_num = pygame.font.SysFont("Arial", RADIO_OBJETIVO, bold=True)
        try:
            ruta_fuente = str(Path(__file__).resolve().parent / "assets" / "imagenes" / "PixelifySans.ttf")
            self.font_juicio = pygame.font.Font(ruta_fuente, 60)
        except:
            self.font_juicio = pygame.font.SysFont("Arial", 60, bold=True)
            
        self.textos_flotantes = pygame.sprite.Group()

        try:
            ruta_sonido = str(Path(__file__).resolve().parent / "assets" / "sonidos" / "spinnerbonus.wav")
            self.sonido_hit = pygame.mixer.Sound(ruta_sonido)
            self.sonido_hit.set_volume(0.6) 
        except:
            self.sonido_hit = None

        try:
            pygame.mixer.music.load(ruta_cancion)
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)
        except Exception as e:
            print(f"No se encontró la musica del juego: {ruta_cancion} - {e}")    

    def handle_events(self, events):
        for evento in events:
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                self._terminar_juego()
            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                self.verificar_impacto(evento.pos)

    def verificar_impacto(self, pos_mouse):
        obj_correcto = next((s for s in self.sprites_lista if s.activo), None)
        for sprite in self.sprites_lista:
            if sprite.activo and sprite.verificar_click(pos_mouse):
                sprite.tocado = True
                sprite.activo = False
                if sprite is obj_correcto:
                    if self.sonido_hit:
                        self.sonido_hit.play()

                    juicio, color, puntos = sprite.obtener_juicio()
                    self.hud.agregar_puntos(puntos)
                    self.hud.mostrar_juicio(juicio, color)
                    
                    if self.frames_explosion:
                        explosion = EfectoVisual(sprite.rect.center, self.frames_explosion)
                        self.vfx_group.add(explosion)
                        
                    texto_pop = TextoFlotante(sprite.rect.center, juicio, color, self.font_juicio)
                    self.textos_flotantes.add(texto_pop)    
                else:
                    if self.modo == MODO_NORMAL: self.hud.perder_vida()
                    self.hud.mostrar_juicio("Mal", COLOR_MAL)
                    texto_mal = TextoFlotante(sprite.rect.center, "MAL", COLOR_MAL, self.font_juicio)
                    self.textos_flotantes.add(texto_mal)
                break

    def actualizar(self, dt):
        vivos = [s for s in self.sprites_lista if s.activo]
        for i, sprite in enumerate(vivos):
            sprite.numero = i + 1
            
        if len(vivos) < self.max_circulos:
            nuevo = self.generador.actualizar(dt, self.font_num)
            if nuevo: self.sprites_lista.append(nuevo)
            
        mouse_pos = pygame.mouse.get_pos()
        self.estela_raton.append(mouse_pos)
        if len(self.estela_raton) > 15:
            self.estela_raton.pop(0)

        for sprite in self.sprites_lista:
            if sprite.activo:
                sprite.update(dt)
                if not sprite.activo and not sprite.tocado:
                    sprite.tocado = True
                    if self.modo == MODO_NORMAL: self.hud.perder_vida()
                    self.hud.mostrar_juicio("Mal", COLOR_MAL)
                    texto_mal = TextoFlotante(sprite.rect.center, "MAL", COLOR_MAL, self.font_juicio)
                    self.textos_flotantes.add(texto_mal)
                    
        self.sprites_lista = [s for s in self.sprites_lista if s.activo]
        self.hud.actualizar(dt)
        if self.hud.sin_vidas(): 
            self._terminar_juego()
            
        # Actualizar grupos con dt
        self.vfx_group.update(dt) 
        self.textos_flotantes.update(dt) 

    def _terminar_juego(self):
        self.ejecutando = False
        pygame.mouse.set_visible(True)    
        pygame.mixer.music.stop() 

    def _dibujar_follow_points(self, superficie):
        for i in range(len(self.sprites_lista) - 1):
            a = pygame.math.Vector2(self.sprites_lista[i].rect.center)
            b = pygame.math.Vector2(self.sprites_lista[i + 1].rect.center)
            vec = b - a
            if vec.length() < 1: continue
            dir_unit = vec.normalize()
            inicio = a + dir_unit * (RADIO_OBJETIVO + 6)
            fin = b - dir_unit * (RADIO_OBJETIVO + 6)
            tramo = (fin - inicio).length()
            if tramo < 10: continue
            paso = 28
            n_pts = max(1, int(tramo / paso))
            tam = 7
            for j in range(n_pts):
                pos = inicio + (fin - inicio) * ((j + 0.5) / n_pts)
                punta = pos + dir_unit * tam
                izq = pos + pygame.math.Vector2(-dir_unit.y, dir_unit.x) * (tam * 0.6)
                der = pos + pygame.math.Vector2(dir_unit.y, -dir_unit.x) * (tam * 0.6)
                pygame.draw.polygon(superficie, COLOR_ACENTO, [(punta.x, punta.y), (izq.x, izq.y), (der.x, der.y)])

    def dibujar(self, superficie):
        if self.imagen_fondo:
            superficie.blit(self.imagen_fondo, (0, 0))
        else:
            superficie.fill(COLOR_FONDO)
            
        mouse_pos = pygame.mouse.get_pos()
        
        if self.img_cursor:
            for i, pos in enumerate(self.estela_raton):
                factor = i / len(self.estela_raton)
                alpha = int(180 * factor)
                scale_factor = 0.5 + (0.5 * factor)
                
                if alpha < 10: continue

                ancho_nuevo = int(self.img_cursor.get_width() * scale_factor)
                alto_nuevo = int(self.img_cursor.get_height() * scale_factor)
                cursor_fantasma = pygame.transform.smoothscale(self.img_cursor, (ancho_nuevo, alto_nuevo))
                cursor_fantasma.fill((255, 255, 255, alpha), special_flags=pygame.BLEND_RGBA_MULT)
                
                rect_fantasma = cursor_fantasma.get_rect(center=pos)
                superficie.blit(cursor_fantasma, rect_fantasma)

            rect_cursor = self.img_cursor.get_rect(center=mouse_pos)
            superficie.blit(self.img_cursor, rect_cursor)
        else:
            pygame.draw.circle(superficie, COLOR_ACENTO, mouse_pos, 15)
            
        self._dibujar_follow_points(superficie)
        self.vfx_group.draw(superficie) 
        
        for sprite in reversed(self.sprites_lista):
            superficie.blit(sprite.image, sprite.rect)
            sprite.dibujar_anillo(superficie)
            sprite.dibujar_numero(superficie)
            
        self.hud.dibujar(superficie)
        self.textos_flotantes.draw(superficie)



# CLASE NUCLEO DEL JUEGO

class OsuLegacyGame(GameBase):
    def __init__(self, metadata):
        super().__init__(metadata)
        self.estado = "MENU" # Estados posibles: MENU, JUGANDO, GAMEOVER
        
        #variables para las pantallas
        self.menu = None
        self.juego_actual = None
        self.game_over = None
        
        #recursos
        self.fondo_menu = None
        self.fondo_juego = None
        self.img_titulo = None
        self.img_gameover = None

    def start(self, surface: pygame.Surface) -> None:
        super().start(surface)
        
        #cargamos las imagenes al arrancar el juego
        self.fondo_menu, self.fondo_juego, self.img_titulo, self.img_gameover = cargar_recursos()
        
        # Instanciamos el menu inicial
        self.menu = Menu(self.fondo_menu, self.img_titulo)

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        if self.estado == "MENU":
            resultado = self.menu.handle_events(events)
            if resultado: 
                modo, dificultad, ruta_cancion = resultado
                self.juego_actual = Juego(modo, dificultad, ruta_cancion, self.fondo_juego)
                self.estado = "JUGANDO"
                
        elif self.estado == "JUGANDO":
            self.juego_actual.handle_events(events)
            
        elif self.estado == "GAMEOVER":
            accion = self.game_over.handle_events(events)
            if accion == "MENU":
                self.menu = Menu(self.fondo_menu, self.img_titulo)
                self.estado = "MENU"
            elif accion == "SALIR":
                self.stop() # Finaliza el juego devolviendo el control a la MAquina Arcade

    def update(self, dt: float) -> None:
        if self.estado == "MENU":
            self.menu.actualizar(dt)
            
        elif self.estado == "JUGANDO":
            if not self.juego_actual.ejecutando:
                puntos = self.juego_actual.hud.puntos
                # Pasamos al estado Game Over
                self.game_over = PantallaGameOver(puntos, self.fondo_juego, self.img_gameover)
                self.estado = "GAMEOVER"
            else:
                self.juego_actual.actualizar(dt)
                
        elif self.estado == "GAMEOVER":
            self.game_over.actualizar(dt)

    # por si el SDK olvida enviarnos la superficie
    def render(self, surface: pygame.Surface = None) -> None:
        # Si el SDK no envIa la surface tomamos la pantalla principal directamente
        if surface is None:
            surface = pygame.display.get_surface()

        # Dibujamos en la superficie
        if self.estado == "MENU":
            self.menu.dibujar(surface)
        elif self.estado == "JUGANDO":
            self.juego_actual.dibujar(surface)
        elif self.estado == "GAMEOVER":
            self.game_over.dibujar(surface)


# EJECUCION INDEPENDIENTE PARA PRUEBAS
if __name__ == "__main__":
    if not pygame.get_init():
        pygame.init()
        
    # Metadatos obligatorios para el SDK
    metadata = (GameMeta()
        .with_title("Osu! Legacy")
        .with_description("Rhythm Arcade Edition")
        .with_release_date("26/02/2026") 
        .with_group_number(7) 
        .add_tag("Ritmo")
        .add_tag("Arcade")
        .add_author(["Rovel Pérez","Eduardo Díaz","Cesar rodríguez","Hemberth García"])) 

    game = OsuLegacyGame(metadata)
    game.run_independently()