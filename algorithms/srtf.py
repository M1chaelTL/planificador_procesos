import time

class ShortestRemainingTimeFirst:
    def __init__(self):
        """Inicializa la lista de procesos."""
        self.processes = []

    def add_process(self, process):
        """Agrega un proceso a la lista."""
        print(f"Proceso {process.pid} agregado a la lista SRTF.")
        self.processes.append(process)
        #print([process.pid for process in self.processes])
    


    def run(self):
        """Ejecuta los procesos seleccionando el que tiene el menor tiempo restante."""
        print("Iniciando planificación SRTF...")
        while self.processes:
            # Ordenar por tiempo restante
            self.processes.sort(key=lambda p: p.burst_time)
            current_process = self.processes[0]
            current_process.start()
            time_slice = 1  # Simula una ejecución de 1 segundo
            time.sleep(min(time_slice, current_process.burst_time))
            current_process.burst_time -= time_slice

            if current_process.burst_time <= 0:
                current_process.terminate()
                current_process.display_statistics()
                self.processes.pop(0)  # Eliminar el proceso completado
        print("Planificación SRTF completada.")

    def run_one_time(self):
        """Ejecuta un tiempo de ejecución de cada proceso en la lista."""
        if self.processes:
            self.processes.sort(key=lambda p: p.burst_time)
            current_process = self.processes[0]
            current_process.burst_time -= 1
            if current_process.burst_time <= 0:
                current_process.terminate()
                self.processes.pop(0)

        return self.processes
