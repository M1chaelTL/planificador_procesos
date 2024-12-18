import time
from planificador_procesos.process import Process
from queue import Queue

class RoundRobin:
    def __init__(self, quantum):
        """Inicializa la cola de procesos y el quantum."""
        self.queue = Queue()
        self.quantum = quantum

    def add_process(self, process):
        """Agrega un proceso a la cola."""
        print(f"\nProceso {process.pid} agregado a la cola Round-Robin.")
        self.queue.put(process)
        self.display_queue()

        def display_queue(self):
            """Muestra el estado actual de la cola de procesos."""
            processes = list(self.queue.queue)
            if processes:
                print("Cola actual de procesos:", [p.pid for p in processes])
            else:
                print("La cola de procesos está vacía.")

    def run(self):
        """Ejecuta los procesos con la política Round-Robin."""
        print("\nIniciando planificación Round-Robin...")
        while not self.queue.empty():
            self.display_queue()  # Mostrar el estado actual de la cola
            process = self.queue.get()
            if process.burst_time > 0:
                process.start()
                execution_time = min(self.quantum, process.burst_time)
                time.sleep(execution_time)  # Simula el tiempo de ejecución
                process.burst_time -= execution_time
                print(f"Proceso {process.pid} ejecutado por {execution_time} segundos. Tiempo restante: {process.burst_time} segundos.")
                if process.burst_time > 0:
                    self.queue.put(process)  # Reinsertar en la cola si no ha terminado
                else:
                    process.terminate()
                    process.display_statistics()
        print("\nPlanificación Round-Robin completada.")

# Ejemplo de uso
if __name__ == "__main__":
    rr = RoundRobin(quantum=2)
    rr.add_process(Process(pid=1, burst_time=5))
    rr.add_process(Process(pid=2, burst_time=3))
    rr.add_process(Process(pid=3, burst_time=6))
    rr.run()