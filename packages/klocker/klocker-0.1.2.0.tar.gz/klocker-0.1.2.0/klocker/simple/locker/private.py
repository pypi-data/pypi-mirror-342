import threading
import time
import warnings
from abc import abstractmethod
from collections.abc import Callable
from typing import Concatenate

from kmodels.types import Unset, unset
from klocker.simple.constants import ON_LOCKED_T, LOCK_FAILURE_T, CALLBACK_T, P, R
from klocker.simple.locker.config import SimpleLockerConfigHandler, SimpleLockerConfigController
from klocker.simple.locker.proxy import SimpleLockerProxy
from klocker.simple.user import SimpleLockerUserInterface
from klocker.simple.thread.state import SimpleThreadLockFailureDetails
from klocker.simple.thread.thread import SimpleLocalThreadController, SimpleLocalThreadHandler


class SimpleLockerPrivate:
    __slots__ = ('_lock', '_stop_event', '_thread', '_config', '_ui', '_proxy')

    _thread: SimpleLocalThreadHandler
    _config: SimpleLockerConfigHandler
    _lock: threading.Lock
    _stop_event: threading.Event
    _ui: SimpleLockerUserInterface
    _proxy: SimpleLockerProxy

    @abstractmethod
    def is_stopping(self) -> bool:
        ...

    @property
    @abstractmethod
    def ui(self):
        ...

    @property
    @abstractmethod
    def _thread_controller(self) -> SimpleLocalThreadController:
        ...

    @property
    @abstractmethod
    def _config_controller(self) -> SimpleLockerConfigController:
        ...

    """------------------------------------------------------"""

    def _handle_stopping_from_thread(self, wait: bool):
        if not self._thread.is_main_thread():
            if not self.ui.config.allow_stop_from_threads:
                raise ValueError(
                    "stop() can only be called from the main thread unless LockerConfig.allow_stop_from_threads == "
                    "True. This is totally fine but, it's disabled by default to prevent unexpected things."
                )
            if wait and not self._thread.is_main_thread():
                raise ValueError(
                    "stop() have to be called with stop(wait=False, ...) if you are not in the main thread. You "
                    "shouldn't send the locker directly to the threads, instead of that, it's safer to send "
                    "locker.proxy or to use locker.with_locker(...) to call the thread functions with the "
                    "restricted ui."
                )

    def _handle_stop_event_warnings(self) -> None:
        """
        Handles warnings related to the stop event.

        If the locker is in the process of stopping and warnings are enabled, this method
        emits a warning to notify the user that the locker is being used after calling `stop()`.
        """
        if self.is_stopping() and self.ui.config.warnings and self.ui.config.stop_event_warnings:
            warnings.warn(
                "Se ha intentado usar el locker tras usar stop() (usa clear() o desactiva "
                "stop_event_warnings según convenga para evitar este warning una vez sepas que tu código funciona "
                "correctamente).",
                RuntimeWarning
            )

    def _try_to_acquire_lock(
            self,
            *,
            remaining_timeout: float | None,
            on_locked: ON_LOCKED_T,
    ) -> tuple[bool, bool]:
        """
        Attempts to acquire the lock with the specified behavior and timeout.

        :param remaining_timeout: The remaining time to wait for the lock, in seconds.
        :param on_locked: Specifies the behavior when the lock is already in use ('wait' or 'leave').

        :return: A tuple where the first value indicates if the lock was acquired, and the second
                 value indicates if the thread waited to acquire the lock.
        """
        if self.is_stopping():
            return False, False

        _acquired = self._lock.acquire(blocking=False)
        _waited = False

        if not _acquired and on_locked == 'wait':
            _waited = True
            if remaining_timeout is None:
                # If no timeout is specified, wait indefinitely (in a safe way)
                _safe_timeout = self.ui.config.stop_event_delay
                while not self.is_stopping() and not _acquired:
                    _acquired = self._lock.acquire(timeout=_safe_timeout)
            else:
                #  If a timeout is specified, just for the stop_event_delay or remaining time (whichever is smaller)
                #  at any rate, this function is going to be called multiple times.
                _safe_timeout = min(self.ui.config.stop_event_delay, remaining_timeout)
                _acquired = self._lock.acquire(timeout=_safe_timeout)

        return _acquired, _waited

    def _stop_timeout_validator(self, stop_timeout) -> float | None:
        _stop_timeout = stop_timeout if not isinstance(stop_timeout, Unset) else self.ui.config.stop_timeout
        if isinstance(_stop_timeout, float) and _stop_timeout <= 0.0:
            raise ValueError("stop_timeout must be greater than 0.0. Use None to wait indefinitely.")
        return _stop_timeout

    @staticmethod
    def _calculate_remaining_timeout(start_time: float, timeout: float | None) -> float | None:
        """
        Calculates the remaining timeout based on the elapsed time.

        :param start_time: The time when the operation started.
        :param timeout: The total timeout duration.

        :return: The remaining timeout, or `None` if no time is left.
        """

        if timeout is None:
            return None

        elapsed = max(0.0, time.monotonic() - start_time)
        remaining_timeout = timeout - elapsed
        remaining_timeout = remaining_timeout if remaining_timeout > 0.0 else None
        return remaining_timeout

    @staticmethod
    def _handle_failure(
            failure_reason: LOCK_FAILURE_T | Unset,
            exception: BaseException
    ) -> SimpleThreadLockFailureDetails | Unset:
        """
        Handles failure details when the lock cannot be acquired.

        :param failure_reason: The reason for the failure ('leave', 'timeout', 'stop_event', or 'exception').
        :param exception: The exception raised during the failure, if any.

        :return: A `ThreadLockFailureDetails` object with the failure details, or `Unset` if no failure occurred.
        """
        if isinstance(failure_reason, Unset):
            return unset
        else:
            if failure_reason == 'exception':
                failure_details = SimpleThreadLockFailureDetails(reason=failure_reason, exception=exception)
            else:
                failure_details = SimpleThreadLockFailureDetails(reason=failure_reason)
        return failure_details

    def _callback_handler(
            self,
            *args,
            func: Callable[[Concatenate[SimpleLockerUserInterface, P]], R],
            callback: CALLBACK_T | Unset,
            **kwargs,
    ):
        """
        Handles the execution of the callback function when the lock is not acquired.

        :param func: The original function passed to `with_locker`.
        :param callback: The callback function to execute. Can be 'func', a callable, or `None`.
        """
        _callback = self.ui.config.callback if isinstance(callback, Unset) else callback
        if _callback is None:
            return

        elif isinstance(_callback, str) and _callback == 'func':
            func(self.ui, *args, **kwargs)
            return

        elif isinstance(_callback, Callable):
            # Si no obtenemos el bloqueo delegamos a
            _callback(self.ui, *args, **kwargs)
            return
        else:
            raise TypeError('callback must be a Callable, "func" or None.')
