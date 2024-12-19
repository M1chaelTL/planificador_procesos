import scheduler as sc
import process as Proceso
import pygame as pg
import gui.process_viewer as pv


class CPU:
    def __init__(self):
        self.procesos = []
        self.scheduler_cpu1 = sc.Scheduler()
        self.scheduler_cpu2 = sc.Scheduler()
        self.scheduler_cpu3 = sc.Scheduler()
        self.scheduler_cpu4 = sc.Scheduler()

        self.procesador_vista1 = pv.ProcesadorVista("CPU 1")
        self.procesador_vista2 = pv.ProcesadorVista("CPU 2")
        self.procesador_vista3 = pv.ProcesadorVista("CPU 3")
        self.procesador_vista4 = pv.ProcesadorVista("CPU 4")

    def configuracion(self):
        self.scheduler_cpu1.algorithm = sc.FIFO()
        self.scheduler_cpu1.synchronization = sc.Mutex()

        self.scheduler_cpu2.algorithm = sc.RoundRobin(4)
        self.scheduler_cpu2.synchronization = sc.Semaphore(2)

        self.scheduler_cpu3.algorithm = sc.ShortestJobFirst()
        self.scheduler_cpu3.synchronization = sc.Monitor()

        self.scheduler_cpu4.algorithm = sc.ShortestRemainingTimeFirst()
        self.scheduler_cpu4.synchronization = sc.Mutex()

    def agregar_proceso(self, proceso):
        self.procesos.append(proceso)

    def agregar_procesos_so(self, num_procesos):
        for _ in range(num_procesos):
            proceso = Proceso.Process()
            self.agregar_proceso(proceso)

    def simular(self):

        if self.procesos:
            for proceso in self.procesos:
                if proceso.get_priority() == 4 or proceso.get_priority() == 5:
                    self.scheduler_cpu1.add_process(proceso)
                elif proceso.get_priority() == 3:
                    self.scheduler_cpu2.add_process(proceso)
                elif proceso.get_priority() == 2:
                    self.scheduler_cpu3.add_process(proceso)
                else:
                    self.scheduler_cpu4.add_process(proceso)

                self.procesos_asignados = True
        self.procesos.clear()
        
        # Función auxiliar para ejecutar el scheduler y manejar resultados nulos
        def safe_execute(scheduler):
            result = scheduler.execute_per_time()
            if result is not None:
                return result
            return []

        # Ejecutar los schedulers de las CPUs
        procesos1 = safe_execute(self.scheduler_cpu1)
        procesos2 = safe_execute(self.scheduler_cpu2)
        procesos3 = safe_execute(self.scheduler_cpu3)
        procesos4 = safe_execute(self.scheduler_cpu4)

        # Crear vistas para listas de procesos
        procesos_vista1 = [pv.ProcesoVista(proceso) for proceso in procesos1]
        procesos_vista2 = [pv.ProcesoVista(proceso) for proceso in procesos2]
        procesos_vista3 = [pv.ProcesoVista(proceso) for proceso in procesos3]
        procesos_vista4 = [pv.ProcesoVista(proceso) for proceso in procesos4]

        self.procesador_vista1.agregar_procesos(procesos_vista1)
        self.procesador_vista2.agregar_procesos(procesos_vista2)
        self.procesador_vista3.agregar_procesos(procesos_vista3)
        self.procesador_vista4.agregar_procesos(procesos_vista4)

        # Dibujar las vistas de los procesadores
        self.procesador_vista1.dibujar(screen, 100, 100)
        self.procesador_vista2.dibujar(screen, 500, 100)
        self.procesador_vista3.dibujar(screen, 100, 500)
        self.procesador_vista4.dibujar(screen, 500, 500)

            

if __name__ == "__main__":

    cpu = CPU()
    cpu.configuracion()
    cpu.agregar_procesos_so(40)

    pg.init()
    screen = pg.display.set_mode((1100, 1000))
    clock = pg.time.Clock()

    # Colores
    WHITE = (255, 255, 255)
    BLUE = (0, 0, 255)
    DARK_BLUE = (0, 0, 150)


    button_rect = pg.Rect(800, 400, 200, 50) 
    button_color = BLUE
    button_hover_color = DARK_BLUE
    font = pg.font.SysFont(None, 36)
    text = font.render("Crear", True, WHITE)
    text_rect = text.get_rect(center=button_rect.center)

    running = True

    while running:

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    cpu.agregar_procesos_so(10)

        screen.fill((25, 25, 25))

        if button_rect.collidepoint(pg.mouse.get_pos()):
            pg.draw.rect(screen, button_hover_color, button_rect)
        else:
            pg.draw.rect(screen, button_color, button_rect)


        screen.blit(text, text_rect)

        cpu.simular()
        pg.time.wait(100)
        pg.display.flip()
        screen.fill((25, 25, 25))
        clock.tick(60)

    pg.quit() 
    