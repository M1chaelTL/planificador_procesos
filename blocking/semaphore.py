import threading
import time

class Semaphore:
    def __init__(self, max_resources):
        """
        Inicializa el semáforo con un número máximo de recursos.
        """
        self.semaphore = threading.Semaphore(max_resources)
        self.max_resources = max_resources
        self.current_resources = max_resources

    def __enter__(self):
        """Entrar en el contexto y adquirir el semáforo."""
        print("Adquiriendo recurso del Semáforo...")
        self.semaphore.acquire()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Salir del contexto y liberar el semáforo."""
        print("Saliendo del Semáforo...")
        self.semaphore.release()

    def acquire(self, process):
        """
        Intenta adquirir un recurso del semáforo.
        """
        print(f"Proceso {process.pid} ha adquirido un recurso del semáforo.")

    def release(self, process):
        """
        Libera un recurso del semáforo.
        """
        self.semaphore.release()
        print(f"Proceso {process.pid} ha liberado un recurso del semáforo.")

    def get_available_resources(self):
        """
        Devuelve el número de recursos disponibles.
        """
        return self.current_resources
