import psutil
import os
import random
import time

class Process:
    def __init__(self, pid=None, burst_time=None, priority=None):
        # Atributos básicos del proceso
        self.pid = pid if pid is not None else None  # ID del proceso real o simulado
        self.priority = priority if priority is not None else random.randint(1, 5)  # Prioridad aleatoria (1 = alta, 5 = baja)
        self.burst_time = burst_time if burst_time is not None else random.randint(1, 10)  # Tiempo de ejecución
        self.arrival_time = time.time()  # Momento en que el proceso fue creado

        # Atributos adicionales para estadísticas
        self.blocked_time = random.randint(1, 5)  # Tiempo bloqueado simulado
        self.remaining_blocked_time = self.blocked_time
        self.delay_time = None
        self.start_time = None
        self.end_time = None
        self.total_wait_time = None
        self.response_time = None

        if pid is None:
            # Crear proceso real si no se pasa un PID manualmente
            self._create_real_process()

    def _create_real_process(self):
        """
        Crea un proceso real usando psutil y un comando simulado.
        """
        try:
            # Inicia un proceso real (en este caso, un sleep)
            self.process = psutil.Popen(["sleep", str(self.burst_time)])
            self.pid = self.process.pid  # Obtener el PID del proceso real
            print(f"Proceso creado con PID: {self.pid}")
        except Exception as e:
            print(f"Error al crear el proceso: {e}")

    def start(self):
        """
        Simula el inicio del proceso.
        """
        self.start_time = time.time()
        print(f"Proceso {self.pid} iniciado a las {time.strftime('%H:%M:%S', time.localtime(self.start_time))}")

    def terminate(self):
        """
        Termina el proceso real.
        """
        if self.process.is_running():
            self.process.terminate()
            print(f"Proceso {self.pid} terminado.")
        else:
            print(f"Proceso {self.pid} ya estaba terminado.")

    def get_priority(self):

        return self.priority

    # Setters para actualizar atributos desde otras clases
    def set_end_time(self, end_time):
        self.end_time = end_time

    def set_total_wait_time(self, wait_time):
        self.total_wait_time = wait_time

    def set_response_time(self, response_time):
        self.response_time = response_time

    def set_delay_time(self, delay_time):
        self.delay_time = delay_time

    def set_blocked_time(self, blocked_time):
        self.blocked_time = blocked_time
        self.remaining_blocked_time = blocked_time

    def display_statistics(self):
        """
        Muestra las estadísticas del proceso.
        """
        tInitBurst = f"{self.burst_time:.2f}s"
        tBloqueadoReferencia = f"{self.blocked_time:.2f}s" if self.blocked_time else "N/A"
        tBloqueadoIO = f"{self.remaining_blocked_time:.2f}s" if self.remaining_blocked_time else "N/A"
        tRetraso = f"{self.delay_time:.2f}s" if self.delay_time else "N/A"
        tLlegada = time.strftime('%H:%M:%S', time.localtime(self.arrival_time))
        tInicio = time.strftime('%H:%M:%S', time.localtime(self.start_time)) if self.start_time else "N/A"
        tTermina = time.strftime('%H:%M:%S', time.localtime(self.end_time)) if self.end_time else "N/A"
        tTotalEspera = f"{self.total_wait_time:.2f}s" if self.total_wait_time else "N/A"
        tRespuesta = f"{self.response_time:.2f}s" if self.response_time else "N/A"

        stats = (
            f"--- Estadísticas del Proceso {self.pid} ---\n"
            f"Tiempo inicial Burst     : {tInitBurst}\n"
            f"Tiempo bloqueado         : {tBloqueadoReferencia}\n"
            f"Tiempo bloqueado restante: {tBloqueadoIO}\n"
            f"Tiempo Retraso           : {tRetraso}\n"
            f"Tiempo Llegada           : {tLlegada}\n"
            f"Tiempo Inicio            : {tInicio}\n"
            f"Tiempo Final             : {tTermina}\n"
            f"Tiempo Espera            : {tTotalEspera}\n"
            f"Tiempo Respuesta         : {tRespuesta}\n"
        )
        print(stats)

# Ejemplo de uso
if __name__ == "__main__":
    # Crear un proceso y mostrar sus estadísticas
    proceso = Process()
    time.sleep(1)  # Simula algún retraso antes de que el proceso comience
    proceso.start()
    
    # Simulando métricas desde otra clase
    proceso.set_delay_time(2.5)
    proceso.set_end_time(time.time() + proceso.burst_time)
    proceso.set_total_wait_time(3.0)
    proceso.set_response_time(1.0)
    proceso.set_blocked_time(4)

    proceso.terminate()
    proceso.display_statistics()
