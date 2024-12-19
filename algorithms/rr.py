import time
from process import Process
from queue import Queue

class RoundRobin:
    def __init__(self, quantum):
        """Inicializa la cola de procesos y el quantum."""
        self.queue = Queue()
        self.quantum = quantum
        self.quantum_actual = quantum

    def add_process(self, process):
        """Agrega un proceso a la cola."""
        print(f"\nProceso {process.pid} agregado a la cola Round-Robin.")
        self.queue.put(process)

    def display_queue(self):
        """Muestra el estado actual de la cola de procesos."""
        processes = list(self.queue.queue)
        if processes:
            print("Cola actual de procesos:", [p.pid for p in processes])
        else:
            print("La cola de procesos está vacía.")

    def run(self):
        """Ejecuta los procesos con la política Round-Robin."""
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

    def run_one_time(self):
        if not self.queue.empty():
            current_process = self.queue.queue[0]  # Obtener el primer proceso sin sacarlo de la cola
            current_process.burst_time -= 1
            self.quantum_actual -= 1

            if current_process.burst_time <= 0:
                self.queue.get()  
                current_process.terminate()
 
            if self.quantum_actual == 0:
                self.quantum_actual = self.quantum
                self.queue.get()  
                self.queue.put(current_process)  
        
        return self.queue
    
    def delete_process(self, pid):
        """Elimina un proceso de la cola."""
        processes = list(self.queue.queue)
        for process in processes:
            if process.pid == pid:
                self.queue.queue.remove(process)
                print(f"Proceso {pid} eliminado de la cola Round-Robin.")
                return
        print(f"Error: Proceso {pid} no encontrado en la cola Round-Robin.")

# Ejemplo de uso
if __name__ == "__main__":
    rr = RoundRobin(quantum=2)
    rr.add_process(Process(pid=1, burst_time=5))
    rr.add_process(Process(pid=2, burst_time=3))
    rr.add_process(Process(pid=3, burst_time=6))
    rr.run()
