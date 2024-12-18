import pygame as pg
from collections import namedtuple

class Proceso:
    
    def __init__(self, id, nombre, tiempo_ejecucion):
        self.id = id
        self.nombre = nombre
        self.tiempo_ejecucion = tiempo_ejecucion

    def dibujar(self, pantalla, x, y):
        color_azul = (0, 0, 255)
        pg.draw.rect(pantalla, color_azul, (x, y, 40, 40))
        font = pg.font.Font(None, 24)
        text = font.render(self.nombre, True, (255, 255, 255))
        pantalla.blit(text, (x + 5, y + 30))

class Procesador:

    def __init__(self):
        self.procesos = []
        self.ejecutando = None

    def agregar_proceso(self, proceso):
        self.procesos.append(proceso)

    
    def dibujar(self, pantalla, x ,y):
        color_gris = (169, 169, 169)
        pg.draw.rect(pantalla, color_gris, (x, y, 80, 80))
        font = pg.font.Font(None, 24)
        text = font.render("CPU", True, (0, 0, 0))
        pantalla.blit(text, (x + 25, y))

        self.dibujar_procesos(pantalla, x, y + 100)

    def dibujar_procesos(self, pantalla, x, y):
        for i, proceso in enumerate(self.procesos):
            proceso.dibujar(pantalla, x, y + i * 100)

