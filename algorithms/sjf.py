import time

class ShortestJobFirst:
    def __init__(self):
        """Inicializa la lista de procesos."""
        self.processes = []

    def add_process(self, process):
        """Agrega un proceso a la lista."""
        print(f"Proceso {process.pid} agregado a la lista SJF.")
        self.processes.append(process)
        self.processes.sort(key=lambda p: p.burst_time)
        #print([process.pid for process in self.processes])

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

    def run_one_time(self):
        """Ejecuta un tiempo de ejecución de cada proceso en la lista."""
        if self.processes:
            
            current_process = self.processes[0]
            current_process.burst_time -= 1
            if current_process.burst_time <= 0:
                current_process.terminate()
                self.processes.pop(0)
        
        return self.processes
    
    def delete_process(self, pid):
        """Elimina un proceso de la lista."""
        for process in self.processes:
            if process.pid == pid:
                self.processes.remove(process)
                print(f"Proceso {pid} eliminado de la lista SJF.")
                return
        print(f"Error: Proceso {pid} no encontrado en la lista SJF.")