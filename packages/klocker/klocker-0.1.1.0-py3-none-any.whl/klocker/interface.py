from abc import ABC, abstractmethod
from typing import Literal, get_args, ParamSpec, TypeVar


class LockerInterface(ABC):
    """Interfaz para un locker."""

    @abstractmethod
    def __enter__(self):
        ...

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        ...

    @property
    @abstractmethod
    def acquired(self) -> bool:
        ...
