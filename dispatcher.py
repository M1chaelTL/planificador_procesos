import psutil
import time
import threading
import random

class Proceso:
    def __init__(self, pid=None):
        if pid is None:
            raise ValueError("Debes proporcionar un PID de un proceso existente en el sistema.")

        try:
            self.proceso = psutil.Process(pid)
            self.PID = pid
            self.nombre = self.proceso.name()
            self.estado = self.proceso.status()
            self.cpu_porcentaje = 0.0
            self.memoria_porcentaje = 0.0
            self.tiempo_inicio = self.proceso.create_time()
            self.hijos = self.proceso.children(recursive=True)
            self.finalizado = False
        except psutil.NoSuchProcess:
            raise ValueError(f"No se encontró ningún proceso con PID {pid}.")

    def actualizar_estadisticas(self):
        """Actualiza las estadísticas del proceso."""
        try:
            self.cpu_porcentaje = self.proceso.cpu_percent(interval=0.1)
            self.memoria_porcentaje = self.proceso.memory_percent()
            self.estado = self.proceso.status()
        except psutil.NoSuchProcess:
            self.finalizado = True

    def terminar(self):
        """Termina el proceso de manera segura."""
        try:
            self.proceso.terminate()
            self.proceso.wait(timeout=3)
            print(f"Proceso {self.PID} terminado correctamente.")
        except psutil.NoSuchProcess:
            print(f"El proceso {self.PID} ya no existe.")
        except psutil.AccessDenied:
            print(f"No tienes permisos para terminar el proceso {self.PID}.")
        except psutil.TimeoutExpired:
            print(f"El proceso {self.PID} no pudo ser terminado a tiempo.")

    def print(self):
        print(f"PID: {self.PID}\n"
              f"Nombre: {self.nombre}\n"
              f"Estado: {self.estado}\n"
              f"CPU (%): {self.cpu_porcentaje}\n"
              f"Memoria (%): {self.memoria_porcentaje}\n"
              f"Tiempo de inicio: {self.tiempo_inicio}\n"
              f"Número de hijos: {len(self.hijos)}")

class ProcesoBloqueado(threading.Thread):
    def __init__(self, proceso, delay, cola_listos):
        super().__init__()
        self.proceso = proceso
        self.delay = delay  # Tiempo en milisegundos
        self.cola_listos = cola_listos

    def run(self):
        try:
            while True:
                time.sleep(self.delay / 1000.0)  # Convertir delay a segundos
                if self.proceso.finalizado:
                    break
                self.proceso.actualizar_estadisticas()
                if self.proceso.estado not in ("stopped", "sleeping"):
                    self.cola_listos.append(self.proceso)
                    break
        except Exception as e:
            print(f"Error en ProcesoBloqueado: {e}")

class PlanificadorCPU:
    FCFS = 1
    SRT = 2
    PSJF = 3
    ROUNDROBIN = 4

    def __init__(self, algoritmo=FCFS, quantum=10, num_procesos_aleatorios=5):
        self.algoritmo = algoritmo
        self.quantum = quantum
        self.procesos = []
        self.cola_listos = []
        self.proceso_activo = None
        self.tiempo_actual = 0
        self.quantum_counter = quantum

        # Crear procesos aleatorios al inicio
        self.crear_procesos_aleatorios(num_procesos_aleatorios)

    def crear_procesos_aleatorios(self, num_procesos):
        """Genera un número específico de procesos aleatorios."""
        pids = random.sample([p.info['pid'] for p in psutil.process_iter(['pid'])], min(num_procesos, len(psutil.pids())))
        self.procesos = [Proceso(pid) for pid in pids]

    def cargar_cola_listos(self):
        """Carga procesos reales listos para ejecutarse en la cola de listos."""
        for proceso in self.procesos:
            if proceso.estado in ("running", "ready"):
                if proceso not in self.cola_listos:
                    self.cola_listos.append(proceso)

    def planificar(self):
        if self.algoritmo == self.FCFS:
            self.proceso_activo = min(self.cola_listos, key=lambda p: p.tiempo_inicio, default=None)
        elif self.algoritmo == self.ROUNDROBIN:
            if self.proceso_activo in self.cola_listos:
                idx = (self.cola_listos.index(self.proceso_activo) + 1) % len(self.cola_listos)
                self.proceso_activo = self.cola_listos[idx]

    def ejecutar_ciclo(self):
        """Ejecuta un ciclo de CPU para el proceso activo."""
        if not self.cola_listos:
            print("No hay procesos listos para ejecutar.")
            return

        self.planificar()

        if self.proceso_activo:
            print(f"Ejecutando proceso: {self.proceso_activo.PID} ({self.proceso_activo.nombre})")
            time.sleep(1)  # Simular tiempo de CPU
            self.proceso_activo.actualizar_estadisticas()

            if self.proceso_activo.finalizado:
                self.cola_listos.remove(self.proceso_activo)

    def simular(self):
        """Simula la ejecución de procesos reales."""
        while True:
            self.cargar_cola_listos()
            self.ejecutar_ciclo()
            time.sleep(0.5)  # Esperar antes del próximo ciclo

    def menu(self):
        while True:
            print("\n--- Menú Interactivo ---")
            print("1. Cargar procesos del sistema")
            print("2. Mostrar cola de listos")
            print("3. Ejecutar ciclo")
            print("4. Simular planificación")
            print("5. Salir")

            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                self.cargar_cola_listos()
                print("Cola de listos cargada.")
            elif opcion == "2":
                print("Procesos en la cola de listos:")
                for proceso in self.cola_listos:
                    proceso.print()
            elif opcion == "3":
                self.ejecutar_ciclo()
            elif opcion == "4":
                self.simular()
            elif opcion == "5":
                print("Saliendo...")
                break
            else:
                print("Opción no válida.")

# Ejemplo de uso
if __name__ == "__main__":
    planificador = PlanificadorCPU(algoritmo=PlanificadorCPU.FCFS, num_procesos_aleatorios=10)
    planificador.menu()
