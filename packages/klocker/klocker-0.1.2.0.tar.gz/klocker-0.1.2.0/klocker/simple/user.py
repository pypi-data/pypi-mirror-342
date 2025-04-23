from __future__ import annotations

from typing import TYPE_CHECKING

from kmodels.types import unset

from klocker.simple.locker.config import SimpleLockerConfigInterface
from klocker.simple.thread.thread import SimpleLocalThreadInterface

if TYPE_CHECKING:
    from klocker.simple.locker.locker import SimpleLocker


class SimpleLockerUserInterface:
    """
    Interface for interacting with a Locker instance, providing access to its configuration
    and threading interface, as well as methods to check and control its stopping state.
    """

    def __init__(self, locker: SimpleLocker, *, config_interface: SimpleLockerConfigInterface,
                 thread_interface: SimpleLocalThreadInterface):
        """
        Initialize the LockerUserInterface.

        :param locker: The Locker instance to interact with.
        :param config_interface: Interface for accessing locker configuration.
        :param thread_interface: Interface for managing threads related to the locker.
        """
        self._locker = locker
        self._config = config_interface
        self._thread = thread_interface

    @property
    def config(self) -> SimpleLockerConfigInterface:
        """
        Get the configuration interface for the locker.

        :return: An instance of LockerConfigInterface.
        """
        return self._config

    @property
    def thread(self) -> SimpleLocalThreadInterface:
        """
        Get the threading interface for the locker.

        :return: An instance of LocalThreadInterface.
        """
        return self._thread

    def is_stopping(self) -> bool:
        """
        Check if the locker is in the process of stopping.

        :return: True if the locker is stopping, False otherwise.
        """
        return self._locker.is_stopping()

    def stop(self):
        """
        Stop the locker without waiting and using the default stop timeout.

        This method signals the locker to stop its operations.
        """
        self._locker.stop(wait=False, stop_timeout=unset)

    def sleep(self, duration: float = 2.0, *, sleep_time: float = 0.1) -> bool:
        """
        Simulates work while respecting the stop signal of the locker.

        :param duration: Total duration to simulate work, in seconds.
        :param sleep_time: Interval to check for stop signals, in seconds.

        :return: True if the locker is not stopping, False otherwise. (In other words, return True if the duration
            was completed without interruption)
        """
        return self._locker.sleep(duration, sleep_time=sleep_time)
