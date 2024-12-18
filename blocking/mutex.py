import threading
import time

class Mutex:
    def __init__(self):
        """Inicializa el mutex."""
        self.lock = threading.Lock()
        self.owner = None  # Proceso que actualmente posee el mutex

    def __enter__(self):
        """Entrar en el contexto y adquirir el mutex."""
        print("Adquiriendo Mutex...")
        self.lock.acquire()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Salir del contexto y liberar el mutex."""
        print("Liberando Mutex...")
        self.lock.release()

    def acquire(self, process):
        """
        Intenta adquirir el mutex para un proceso.
        """
        print(f"Proceso {process.pid} ha adquirido el Mutex.")
        self.owner = process

    def release(self, process):
        """
        Libera el mutex si el proceso actual lo posee.
        """
        if self.owner == process:
            self.lock.release()
            print(f"Proceso {process.pid} ha liberado el Mutex.")
            self.owner = None
        else:
            print(f"Proceso {process.pid} no puede liberar el Mutex porque no lo posee.")

    def is_locked(self):
        """
        Verifica si el mutex está bloqueado.
        """
        return self.lock.locked()
