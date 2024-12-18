import time
from algorithms.fifo import FIFO
from algorithms.rr import RoundRobin
from algorithms.sjf import ShortestJobFirst
from algorithms.srtf import ShortestRemainingTimeFirst
from blocking.mutex import Mutex
from blocking.monitor import Monitor
from blocking.semaphore import Semaphore
from process import Process

class Scheduler:
    def __init__(self):
        """Inicializa el planificador con opciones configurables."""
        self.algorithm = None
        self.synchronization = None
        self.processes = []
        self.sync_handler = None

    def select_algorithm(self):
        """Permite al usuario seleccionar un algoritmo de planificación."""
        print("\nSeleccione un algoritmo de planificación:")
        print("1. FIFO")
        print("2. Round-Robin")
        print("3. Shortest Job First (SJF)")
        print("4. Shortest Remaining Time First (SRTF)")
        choice = input("Ingrese el número de su elección: ")

        if choice == "1":
            self.algorithm = FIFO()
        elif choice == "2":
            quantum = int(input("Ingrese el quantum para Round-Robin: "))
            self.algorithm = RoundRobin(quantum)
        elif choice == "3":
            self.algorithm = ShortestJobFirst()
        elif choice == "4":
            self.algorithm = ShortestRemainingTimeFirst()
        else:
            print("Elección no válida. Por defecto se seleccionará FIFO.")
            self.algorithm = FIFO()

    def select_synchronization(self):
        """Permite al usuario seleccionar un método de sincronización."""
        print("\nSeleccione un método de sincronización:")
        print("1. Mutex")
        print("2. Semaphore")
        print("3. Monitor")
        choice = input("Ingrese el número de su elección: ")

        if choice == "1":
            self.sync_handler = Mutex()
        elif choice == "2":
            max_resources = int(input("Ingrese el número máximo de recursos para el Semáforo: "))
            self.sync_handler = Semaphore(max_resources)
        elif choice == "3":
            self.sync_handler = Monitor()
        else:
            print("Elección no válida. Por defecto se seleccionará Mutex.")
            self.sync_handler = Mutex()


    def add_processes(self, num_processes):
        """Crea y agrega procesos simulados al planificador."""
        print(f"Creando {num_processes} procesos simulados...")
        for _ in range(num_processes):
            process = Process()
            self.processes.append(process)
            self.algorithm.add_process(process)

    def execute(self):
        """Ejecuta la planificación y maneja la sincronización."""
        if not self.algorithm:
            print("Error: No se ha seleccionado ningún algoritmo de planificación.")
            return

        if not self.sync_handler:
            print("Error: No se ha seleccionado ningún método de sincronización.")
            return

        print("\n--- Iniciando ejecución del Scheduler ---")
        with self.sync_handler:  # Adquiere el bloqueo
            self.algorithm.run()
            
        print("\n--- Ejecución completada ---")

if __name__ == "__main__":
    scheduler = Scheduler()

    # Paso 1: Seleccionar el algoritmo
    scheduler.select_algorithm()

    # Paso 2: Seleccionar el método de sincronización
    scheduler.select_synchronization()

    # Paso 3: Crear procesos
    num_processes = int(input("\nIngrese el número de procesos a simular: "))
    scheduler.add_processes(num_processes)

    # Paso 4: Ejecutar el planificador
    scheduler.execute()
