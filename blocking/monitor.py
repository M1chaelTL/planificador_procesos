import threading
import time

class Monitor:
    def __init__(self):
        """Inicializa el monitor con un candado (Lock)."""
        self.lock = threading.Condition()
        self.is_busy = False  # Estado de la sección crítica

    def __enter__(self):
        """Entrar al contexto y adquirir el monitor."""
        print("Esperando para entrar al Monitor...")
        with self.lock:
            while self.is_busy:
                self.lock.wait()
            self.is_busy = True
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Salir del contexto y liberar el monitor."""
        with self.lock:
            self.is_busy = False
            self.lock.notify_all()
        print("Saliendo del Monitor...")

    def enter(self, process):
        """
        Un proceso intenta entrar a la sección crítica.
        """
        print(f"Proceso {process.pid} ha entrado al Monitor.")

    def exit(self, process):
        """
        El proceso sale de la sección crítica y notifica a otros.
        """
        print(f"Proceso {process.pid} ha salido del Monitor.")
