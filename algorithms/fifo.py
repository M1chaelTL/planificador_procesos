import time
from queue import Queue

class FIFO:
    def __init__(self):
        """Inicializa la cola de procesos."""
        self.queue = Queue()

    def add_process(self, process):
        """Agrega un proceso a la cola."""
        print(f"Proceso {process.pid} agregado a la cola FIFO.")
        self.queue.put(process)

    def display_queue(self):
        """Muestra el estado actual de la cola de procesos."""
        processes = list(self.queue.queue)
        if processes:
            print("Cola actual de procesos:", [p.pid for p in processes])
        else:
            print("La cola de procesos está vacía.")
    
    def run(self):
        """Ejecuta los procesos en el orden en que llegaron."""
        print("Iniciando planificación FIFO...")
        while not self.queue.empty():
            self.display_queue()  # Mostrar el estado actual de la cola
            process = self.queue.get()
            process.start()
            time.sleep(process.burst_time)  # Simula el tiempo de ejecución
            process.terminate()
            process.display_statistics()
        print("Planificación FIFO completada.")
