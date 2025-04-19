import threading
from typeguard import typechecked


class SimpleThreadLocalState:
    """Clase para manejar el estado específico de cada hilo."""
    __slots__ = ('_thread_local',)

    def __init__(self):
        self._thread_local = threading.local()

    @property
    def acquired(self) -> bool:
        """Obtiene el estado de 'acquired' para el hilo actual."""
        return self._thread_local.acquired

    @property
    def waited(self) -> bool:
        """Retorna True si el Thread tuvo que esperar para bloquear."""
        return self._thread_local.waited

    @waited.setter
    @typechecked
    def waited(self, value: bool):
        """Establece 'waited' para el hilo actual."""
        self._thread_local.waited = value

    @acquired.setter
    @typechecked
    def acquired(self, value: bool):
        """Establece el estado de 'acquired' para el hilo actual."""
        self._thread_local.acquired = value

    def reset(self):
        """Resetea/Inicializa todas las variables para el hilo actual."""
        self._thread_local.acquired = False
        self._thread_local.waited = False
