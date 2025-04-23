import threading
import time

from collections.abc import Callable
from typing import Self, Concatenate
from typeguard import typechecked

from kmodels.types import Unset, unset
from klocker.simple.constants import ON_LOCKED_T, LOCK_FAILURE_T, CALLBACK_T, P, R
from klocker.simple.locker.config import SimpleLockerConfig, SimpleLockerConfigHandler, SimpleLockerConfigController
from klocker.simple.locker.private import SimpleLockerPrivate
from klocker.simple.locker.proxy import SimpleLockerProxy
from klocker.simple.user import SimpleLockerUserInterface
from klocker.simple.thread.state import SimpleThreadLockFailureDetails
from klocker.simple.thread.thread import SimpleLocalThreadController, SimpleLocalThreadHandler


class SimpleLocker(SimpleLockerPrivate):
    @typechecked
    def __init__(self, *, config: SimpleLockerConfig | Unset = unset):
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._thread = SimpleLocalThreadHandler()
        self._config = SimpleLockerConfigHandler(config=config)
        self._ui: SimpleLockerUserInterface = SimpleLockerUserInterface(
            self,
            config_interface=self._config.interface,
            thread_interface=self._thread.interface
        )
        self._proxy = SimpleLockerProxy(self)

    @property
    def _thread_controller(self) -> SimpleLocalThreadController:
        """Manejador de datos del hilo local (para uso privado)."""
        return self._thread.controller

    @property
    def _config_controller(self) -> SimpleLockerConfigController:
        """Manejador de datos de la configuración general del locker (para uso privado)."""
        return self._config.controller

    @property
    def proxy(self) -> SimpleLockerProxy:
        return self._proxy

    @property
    def ui(self):
        return self._ui

    def is_stopping(self) -> bool:
        """
        Checks if the locker is in the process of stopping.

        :return: True if the locker is stopping, False otherwise.
        """
        return self._stop_event.is_set()

    @typechecked
    def stop(self, *, wait: bool = True, stop_timeout: float | None | Unset = unset) -> None:
        """
        Stops the threads associated with the locker by signaling them to exit, waiting
        for them to leave within the specified timeout if applicable. Ensures that all
        threads are properly synchronized before considering the stop operation complete.

        :param wait: If True, waits for the threads to exit the locker before returning. If False,
            returns immediately without waiting for threads to exit.

        :param stop_timeout: Specifies the maximum time, in seconds, to wait for threads
            to exit the locker. If set to None, waits indefinitely. If the value is less
            than or equal to 0.0 and not None, a ValueError is raised. Use `Unset` to
            designate that the configured default timeout should be used.
        :type stop_timeout: float | None | Unset


        :return: None

        :raises ValueError: If `stop_timeout` is less than or equal to 0.0 when not None (if stop_time is invalid).
        :raises TimeoutError: If the waiting period exceeds the specified `stop_timeout`
            and threads have not exited the locker.
        """

        self._handle_stopping_from_thread(wait)

        _stop_timeout = self._stop_timeout_validator(stop_timeout)

        # Espera a que todos los hilos abandonen el locker para considerarlo detenido.
        self._stop_event.set()

        if not wait:
            return

        if _stop_timeout is None:
            self._lock.acquire(blocking=True)
        else:
            acquired = self._lock.acquire(blocking=True, timeout=_stop_timeout)
            if not acquired:
                raise TimeoutError("Timeout while waiting for threads to exit the locker.")

        # Finalmente, liberamos el lock.
        self._lock.release()

    def clear(self):
        """
        Clears the internal stop event.

        This method is intended to reset the flag indicating a stopping event. It ensures that the stop event is
        cleared only if the object's stopping condition is active. It does not perform any action if the stopping
        condition is not met.

        """
        if not self.is_stopping():
            return
        self._stop_event.clear()

    def _handle_stop_event(self) -> bool:
        ...

    @typechecked
    def enter(
            self,
            *,
            on_locked: ON_LOCKED_T | Unset = unset,
            timeout: float | None | Unset = unset,
    ) -> Self:
        """
        Attempts to acquire a lock and manage its lifecycle within a specified timeout period.
        This method is designed to handle scenarios where the lock cannot be immediately
        acquired and includes customizable behavior for handling contention with other
        threads or processes. The method also respects stopping signals to ensure that
        resources are properly managed and no deadlocks occur.

        :param on_locked:
            Specifies the behavior to be used when the lock is already in use. This can
            determine how contention is handled, such as waiting for the lock to become
            available, or exiting immediately based on the value provided. Uses the
            global configuration value `self.config.on_locked` if omitted or unset.

        :param timeout:
            The maximum time to wait to acquire the lock, in seconds. If `None`, waits
            indefinitely. If omitted or unset, defaults to the value configured globally
            in `self.config.timeout`. Takes precedence over global settings when specified.

        :return:
            Returns the current instance (`self`) after attempting to acquire the lock,
            initializing the proper thread-local state and configuration. This ensures
            that the acquired or waited state is properly synchronized with the caller's
            expectations.
        """

        _on_locked = on_locked if not isinstance(on_locked, Unset) else self.ui.config.on_locked
        _timeout = timeout if not isinstance(timeout, Unset) else self.ui.config.timeout

        _waited, _acquired = False, False
        _remaining_timeout = _timeout
        _start_time = time.monotonic()

        _failure_reason: LOCK_FAILURE_T | Unset = unset
        _exception: BaseException | Unset = unset
        _failure_details: SimpleThreadLockFailureDetails | Unset = unset
        try:
            while True:
                # Stopping at the beginning of the loop to avoid unnecessary lapses
                if self.is_stopping():
                    _failure_reason = 'stop_event'
                    break

                # Try to acquire the lock
                _acquired, _this_waited = self._try_to_acquire_lock(
                    remaining_timeout=_remaining_timeout,
                    on_locked=_on_locked
                )
                _waited = any((_this_waited, _waited))

                # Check if timeout is reached
                if _remaining_timeout is not None:
                    _remaining_timeout = self._calculate_remaining_timeout(_start_time, _timeout)
                    if _remaining_timeout is None:
                        _failure_reason = 'timeout'
                        break

                # Check if the lock was acquired
                if _acquired:
                    break
                elif _on_locked == 'leave':
                    _failure_reason = 'leave'
                    break

        except BaseException as e:
            _failure_reason = 'exception'
            _exception = e

        # FIX: self.is_stopping() puede haber sucedido tras self._try_to_acquire_lock().
        if self.is_stopping():
            _failure_reason = 'stop_event'
            if _acquired:
                _acquired = False
                self._lock.release()

        # We handle the failure reason and details
        _failure_details = self._handle_failure(_failure_reason, _exception)

        # We initialize the thread-local state and config
        self._thread_controller.config.initialize(on_locked=_on_locked, timeout=_timeout)
        self._thread_controller.state.initialize(acquired=_acquired, waited=_waited, failure_details=_failure_details)

        # Finally, we return the locker instance
        return self

    def exit(self):
        """
        Releases the lock if it was acquired and resets the thread-local state.

        This method is intended to be called when the lock is no longer needed. It ensures
        that the lock is released properly and resets the thread-local state to its initial
        configuration. This is important for maintaining the integrity of the locking mechanism
        and ensuring that resources are properly managed.

        """
        if self.ui.thread.state.acquired:
            self._lock.release()

    def __enter__(self) -> Self:
        """
        Enters the lock context manager, acquiring the lock if possible.

        :return: The current instance of the locker.
        """
        return self.enter()

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Exits the lock context manager, releasing the lock if it was acquired.

        :param exc_type: The type of exception raised, if any.
        :param exc_val: The value of the exception raised, if any.
        :param exc_tb: The traceback object, if any.
        """
        self.exit()

    def with_locker(
            self,
            func: Callable[[Concatenate[SimpleLockerUserInterface, P]], R],
            callback: CALLBACK_T | Unset = unset,
            *args,
            on_locked: ON_LOCKED_T | Unset = unset,
            timeout: float | None | Unset = unset,
            **kwargs,
    ):
        """
        Executes a function within the context of the locker.

        This method handles acquiring and releasing the lock automatically. If the lock
        cannot be acquired, a callback function can be executed instead.

        :param func: The function to execute if the lock is acquired.
        :param callback: The function to execute if the lock is not acquired. Can be 'func',
                         a callable, or `None`.
        :param on_locked: Specifies the behavior when the lock is already in use ('wait' or 'leave').
                          Defaults to the global configuration if `Unset`.
        :param timeout: The maximum time to wait for the lock, in seconds. Defaults to the global
                        configuration if `Unset`.
        """

        # We enter the locker (custom config for this call is allowed)
        self.enter(on_locked=on_locked, timeout=timeout)
        # We separate the callback from the function to be executed (or not if callback is 'func')
        if not self.ui.thread.state.acquired:
            # Si sinos hemos obtenido el bloqueo delegamos al _callback_handler
            self._callback_handler(func=func, callback=callback)
            return

        # Llamamos a la función si hemos obtenido el bloqueo
        func(self.ui, *args, **kwargs)
        self.exit()

    def sleep(self, duration: float = 2.0, *, sleep_time: float = 0.1) -> bool:
        """
        Simulates work while respecting the stop signal of the locker.

        :param duration: Total duration to simulate work, in seconds.
        :param sleep_time: Interval to check for stop signals, in seconds.

        :return: True if the locker is not stopping, False otherwise. (In other words, return True if the duration
            was completed without interruption)
        """
        remaining = duration
        condition = threading.Condition()

        while not self.is_stopping() and remaining > 0.0:
            start_time = time.monotonic()
            with condition:
                condition.wait(timeout=min(remaining, sleep_time))  # Efficient wait
            elapsed = time.monotonic() - start_time
            remaining = max(0.0, remaining - elapsed)

        return not self.is_stopping()


SimpleLockerConfig.model_rebuild()
