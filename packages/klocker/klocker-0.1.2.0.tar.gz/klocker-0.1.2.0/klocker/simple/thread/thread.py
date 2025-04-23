import threading

from klocker.simple.thread.config import SimpleLocalThreadConfigInterface, SimpleLocalThreadConfigController
from klocker.simple.thread.state import SimpleLocalThreadStateInterface, SimpleLocalThreadStateController


class SimpleLocalThreadInterface:
    def __init__(self, config: SimpleLocalThreadConfigInterface, state: SimpleLocalThreadStateInterface):
        self._config = config
        self._state = state

    @property
    def config(self) -> SimpleLocalThreadConfigInterface:
        return self._config

    @property
    def state(self) -> SimpleLocalThreadStateInterface:
        return self._state

    @property
    def name(self):
        return threading.current_thread().name


class SimpleLocalThreadController:
    def __init__(self, config: SimpleLocalThreadConfigController, state: SimpleLocalThreadStateController):
        self._config = config
        self._state = state

    @property
    def config(self) -> SimpleLocalThreadConfigController:
        return self._config

    @property
    def state(self) -> SimpleLocalThreadStateController:
        return self._state


class SimpleLocalThreadHandler:
    def __init__(self):
        self._local_env = threading.local()

        config_interface = SimpleLocalThreadConfigInterface(self._local_env)
        state_interface = SimpleLocalThreadStateInterface(self._local_env)
        self._interface = SimpleLocalThreadInterface(config_interface, state_interface)

        config_controller = SimpleLocalThreadConfigController(self._local_env)
        state_controller = SimpleLocalThreadStateController(self._local_env)
        self._controller = SimpleLocalThreadController(config_controller, state_controller)

    @property
    def interface(self) -> SimpleLocalThreadInterface:
        """Returns the interface for accessing thread-local data."""
        return self._interface

    @property
    def controller(self) -> SimpleLocalThreadController:
        """Returns the controller for managing thread-local data."""
        return self._controller

    @staticmethod
    def is_main_thread() -> bool:
        return threading.current_thread() is threading.main_thread()

    @classmethod
    def is_thread(cls) -> bool:
        return not cls.is_main_thread()

    def name(self) -> str:
        return self.interface.name
