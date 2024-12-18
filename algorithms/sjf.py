import time

class ShortestJobFirst:
    def __init__(self):
        """Inicializa la lista de procesos."""
        self.processes = []

    def add_process(self, process):
        """Agrega un proceso a la lista."""
        print(f"Proceso {process.pid} agregado a la lista SJF.")
        self.processes.append(process)

    def run(self):
        """Ejecuta los procesos en orden de menor a mayor tiempo de ráfaga."""
        print("Iniciando planificación SJF...")
        self.processes.sort(key=lambda p: p.burst_time)  # Ordenar por tiempo de ráfaga
        for process in self.processes:
            process.start()
            time.sleep(process.burst_time)  # Simula el tiempo de ejecución
            process.terminate()
            process.display_statistics()
        print("Planificación SJF completada.")
