import pygame as pg
import process_viewer as pl

pg.init()
screen = pg.display.set_mode((800, 1000))
clock = pg.time.Clock()

running = True

procesador = pl.ProcesadorVista()
procesador2 = pl.ProcesadorVista()

proceso1 = pl.ProcesoVista(1, "Proceso 1", 10)
proceso2 = pl.ProcesoVista(2, "Proceso 2", 20)
#proceso3 = pl.ProcesoVista(3, "Proceso 3", 30)

procesador.agregar_proceso(proceso1)
procesador.agregar_proceso(proceso2)
#procesador.agregar_proceso(proceso3)

procesador2.agregar_proceso(proceso1)
procesador2.agregar_proceso(proceso2)
#procesador2.agregar_proceso(proceso3)

while running:

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    screen.fill((30, 30, 30))

    # Dibujar el planificador
    procesador.dibujar(screen, 100, 100)
    procesador2.dibujar(screen, 500, 100)

    pg.display.flip()
    clock.tick(60)

pg.quit()