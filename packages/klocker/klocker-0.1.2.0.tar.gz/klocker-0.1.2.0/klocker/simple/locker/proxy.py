from __future__ import annotations

from typing import TYPE_CHECKING, Self

from kmodels.types import Unset, unset

from klocker.simple.constants import ON_LOCKED_T
from klocker.simple.user import SimpleLockerUserInterface

if TYPE_CHECKING:
    from klocker.simple.locker.locker import SimpleLocker


class SimpleLockerProxy:
    def __init__(self, locker: SimpleLocker):
        self._locker = locker
        self._ui = locker.ui

    @property
    def ui(self) -> SimpleLockerUserInterface:
        return self._locker.ui

    def __enter__(self) -> Self:
        self._locker.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._locker.__exit__(exc_type, exc_val, exc_tb)

    def enter(
            self,
            *,
            on_locked: ON_LOCKED_T | Unset = unset,
            timeout: float | None | Unset = unset,
    ) -> Self:
        self._locker.enter(on_locked=on_locked, timeout=timeout)
        return self

    def exit(self):
        self._locker.exit()
