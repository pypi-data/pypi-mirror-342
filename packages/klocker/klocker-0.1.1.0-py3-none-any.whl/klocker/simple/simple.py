import threading
import time
from typing import Literal, get_args, Callable, Concatenate, Self
from typeguard import typechecked

from klocker.exception import LockerLocked
from klocker.interface import LockerInterface
from klocker.methods import execute_with_locker, create_locker_wrapper, P, R
from klocker.simple.localstate import SimpleThreadLocalState

ON_BLOCKED_T = Literal['wait', 'leave', 'raise']
ON_BLOCKED: tuple[ON_BLOCKED_T, ...] = get_args(ON_BLOCKED_T)


class SimpleLocker(LockerInterface):
    """
    A simple locker class to manage shared resources.
    """
    __slots__ = ('_lock', '_state', '_on_locked')

    @typechecked
    def __init__(self, *, on_blocked: ON_BLOCKED_T = 'wait'):
        """
        Initializes the locker with a blocking behavior.

        :param on_blocked: Defines the behavior when the lock is already acquired.
                           Options are 'wait', 'leave', or 'raise'.
        """
        self._lock = threading.Lock()
        self._on_locked = on_blocked
        self._state = SimpleThreadLocalState()

    def __enter__(self):
        """
        Acquires the lock based on the blocking behavior.

        :return: The locker instance.
        """
        self._state.reset()
        if not self._lock.acquire(blocking=False):
            if self._on_locked == 'wait':
                self._state.waited = True
                self._lock.acquire()
            elif self._on_locked == 'leave':
                return self
            elif self._on_locked == 'raise':
                raise LockerLocked()

        self._state.acquired = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Releases the lock if it was acquired.

        :param exc_type: Exception type if an exception occurred.
        :param exc_val: Exception value if an exception occurred.
        :param exc_tb: Traceback object if an exception occurred.
        """
        if self.acquired:
            self._lock.release()

    @property
    def acquired(self):
        """
        Checks if the lock is currently acquired.

        :return: True if the lock is acquired, False otherwise.
        """
        return self._state.acquired

    @property
    def waited(self):
        """
        Returns True if the thread had to wait for its own turn because the lock was already acquired.

        :return: True if the thread waited, False otherwise.
        """
        return self._state.waited

    @typechecked
    def with_locker_pass(self, func: Callable[Concatenate[Self, P], R], *args: P.args, **kwargs: P.kwargs) -> R:
        return execute_with_locker(self, func, pass_locker=True, *args, **kwargs)

    @typechecked
    def locker_wrapper_pass(self, func: Callable[Concatenate[Self, P], R]) -> Callable[Concatenate[Self, P], R]:
        return create_locker_wrapper(self, func, pass_locker=True)

    @typechecked
    def with_locker_nonpass(self, func: Callable[[P], R], *args: P.args, **kwargs: P.kwargs) -> R:
        return execute_with_locker(self, func, pass_locker=False, *args, **kwargs)

    @typechecked
    def locker_wrapper_nonpass(self, func: Callable[[P], R]) -> Callable[[P], R]:
        return create_locker_wrapper(self, func, pass_locker=False)


class Test:
    """
    A class containing test methods for the SimpleLocker.
    """

    @staticmethod
    def start_threads(worker_func: Callable, _last_idx: int = 0, _n_threads: int = 10) -> int:
        """
        Starts multiple threads to execute a worker function.

        :param worker_func: The function to execute in each thread.
        :param _last_idx: The starting index for thread naming.
        :param _n_threads: The number of threads to start.
        :return: The next starting index for thread naming.
        """
        threads = [
            threading.Thread(target=worker_func, name=f"Thread-{idx}") for idx in
            range(_last_idx, _last_idx + _n_threads)
        ]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        return _last_idx + _n_threads

    @classmethod
    def test_passing(cls):
        """
        Tests the locker with functions that require the locker to be passed as an argument.
        """
        locker = SimpleLocker(on_blocked='leave')
        last_idx = 0
        n_threads = 10

        @locker.locker_wrapper_pass
        def locker_wrapper_pass(_locker: SimpleLocker):
            """
            A test function wrapped with locker_wrapper_pass.
            """
            if _locker.acquired:  # Only needed if on_blocked is 'wait'
                print(f"[{threading.current_thread().name}] Acquired the lock. Waited: {_locker.waited}")
                time.sleep(0.05)
            else:
                print(f"[{threading.current_thread().name}] Could not acquire the lock.")

        def with_locker_pass(_locker: SimpleLocker):
            """
            A test function executed with with_locker_pass.
            """
            if _locker.acquired:  # Only needed if on_blocked is 'wait'
                print(f"[{threading.current_thread().name}] Acquired the lock. Waited: {_locker.waited}")
                time.sleep(0.05)  # Simulates work inside the lock
            else:
                print(f"[{threading.current_thread().name}] Could not acquire the lock.")

        def direct_use_pass(_locker: SimpleLocker):
            """
            A test function using the locker directly.
            """
            with _locker:
                if _locker.acquired:  # Only needed if on_blocked is 'wait'
                    print(f"[{threading.current_thread().name}] Acquired the lock. Waited: {_locker.waited}")
                    time.sleep(0.05)  # Simulates work inside the lock
                else:
                    print(f"[{threading.current_thread().name}] Could not acquire the lock.")

        # Uncomment one of the following to test different scenarios:
        cls.start_threads(locker_wrapper_pass, last_idx, n_threads)
        print('--' * 20)
        cls.start_threads(lambda: locker.with_locker_pass(with_locker_pass), last_idx, n_threads)
        print('--' * 20)
        cls.start_threads(lambda: direct_use_pass(locker), last_idx, n_threads)

    @classmethod
    def test_not_passing(cls):
        """
        Tests the locker with functions that do not require the locker to be passed as an argument.
        """
        locker = SimpleLocker(on_blocked='leave')
        last_idx = 0
        n_threads = 10

        @locker.locker_wrapper_nonpass
        def locker_wrapper_nonpass():
            """
            A test function wrapped with locker_wrapper_nonpass.
            """
            if locker.acquired:  # Only needed if on_blocked is 'wait'
                print(f"[{threading.current_thread().name}] Acquired the lock. Waited: {locker.waited}")
                time.sleep(0.05)
            else:
                print(f"[{threading.current_thread().name}] Could not acquire the lock.")

        def with_locker_nonpass():
            """
            A test function executed with with_locker_nonpass.
            """
            if locker.acquired:  # Only needed if on_blocked is 'wait'
                print(f"[{threading.current_thread().name}] Acquired the lock. Waited: {locker.waited}")
                time.sleep(0.05)  # Simulates work inside the lock
            else:
                print(f"[{threading.current_thread().name}] Could not acquire the lock.")

        def direct_use_nonpass():
            """
            A test function using the locker directly.
            """
            with locker:
                if locker.acquired:  # Only needed if on_blocked is 'wait'
                    print(f"[{threading.current_thread().name}] Acquired the lock. Waited: {locker.waited}")
                    time.sleep(0.05)  # Simulates work inside the lock
                else:
                    print(f"[{threading.current_thread().name}] Could not acquire the lock.")

        # Uncomment one of the following to test different scenarios:
        cls.start_threads(locker_wrapper_nonpass, last_idx, n_threads)
        print('--' * 20)
        cls.start_threads(lambda: locker.with_locker_nonpass(with_locker_nonpass), last_idx, n_threads)
        print('--' * 20)
        cls.start_threads(direct_use_nonpass, last_idx, n_threads)


if __name__ == "__main__":
    Test.test_passing()
    Test.test_not_passing()
