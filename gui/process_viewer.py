import pygame as pg
from collections import namedtuple
from process import Process

class ProcesoVista:
    
    def __init__(self, proceso):
        self.pid = proceso.pid
        self.tiempo_ejecucion = proceso.burst_time

    def dibujar(self, pantalla, x, y):
        color_azul = (0, 0, 255)
        pg.draw.rect(pantalla, color_azul, (x, y, 40, 40))
        font = pg.font.Font(None, 24)
        text = font.render(str(self.pid), True, (255, 255, 255))
        tiempo_text = font.render(str(self.tiempo_ejecucion), True, (255, 255, 255))
        pantalla.blit(tiempo_text, (x + 5, y + 5))

        pantalla.blit(text, (x + 5, y + 30))

class ProcesadorVista:

    def __init__(self, nombre):
        self.procesos = []
        self.ejecutando = None
        self.nombre = nombre

    def agregar_proceso(self, proceso):
        self.procesos.append(proceso)

    def agregar_procesos(self, procesos):
        self.procesos.clear()
        self.procesos.extend(procesos)
    
    def dibujar(self, pantalla, x ,y):
        color_gris = (169, 169, 169)
        pg.draw.rect(pantalla, color_gris, (x, y, 80, 80))
        font = pg.font.Font(None, 24)
        text = font.render(self.nombre, True, (0, 0, 0))
        pantalla.blit(text, (x + 25, y))

        self.dibujar_procesos(pantalla, x, y + 100)

    def dibujar_procesos(self, pantalla, x, y):
        for i, proceso in enumerate(self.procesos[:4]):
            proceso.dibujar(pantalla, x, y + i * 100)

