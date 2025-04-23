import threading

from klocker.simple.constants import ON_LOCKED_T
from klocker.simple.shared import SimpleBaseLockerThreadConfig
from klocker.simple.thread.base import SimpleBaseLocalThreadDataInterface, SimpleBaseLocalThreadDataController


class SimpleLocalThreadConfig(SimpleBaseLockerThreadConfig):
    """
    Hereda valores como on_locked y timeout de BaseLockerThreadConfig.
    """
    ...


class SimpleLocalThreadConfigInterface(SimpleBaseLocalThreadDataInterface):
    """
    Clase que contiene la configuración del hilo local. Está pensada para ser accedida directamente por el usuario.
    """

    def __init__(self, local_env: threading.local):
        super().__init__(local_env, 'config')

    @property
    def data(self) -> SimpleLocalThreadConfig:
        self._raise_not_initialized()
        return self._local_env.config

    @property
    def on_locked(self) -> ON_LOCKED_T:
        return self.data.on_locked

    @property
    def timeout(self) -> float | None:
        return self.data.timeout


class SimpleLocalThreadConfigController(SimpleBaseLocalThreadDataController):
    """
    Clase que controla la configuración del hilo local. No debe ser pasada al usuario, se puede considerar que es
    un helper para inicializar la configuración del hilo local, entre otros.
    """

    def __init__(self, local_env: threading.local):
        super().__init__(local_env, 'config')

    def initialize(self, *, on_locked: ON_LOCKED_T, timeout: float | None):
        self._raise_already_initialized()
        self._local_env.config = SimpleLocalThreadConfig(on_locked=on_locked, timeout=timeout)

    def initialize_from_config(self, config: SimpleLocalThreadConfig):
        self.initialize(on_locked=config.on_locked, timeout=config.timeout)
