import threading


class SimpleBaseThreadHandler:
    def __init__(self, local_env: threading.local, varname: str):
        self._local_env: threading.local = local_env
        self._varname: str = varname

    def is_initialized(self) -> bool:
        return hasattr(self._local_env, self._varname)

    def _raise_already_initialized(self):
        if self.is_initialized():
            raise RuntimeError("Thread-local state already initialized.")

    def _raise_not_initialized(self):
        if not self.is_initialized():
            raise RuntimeError("Thread-local state not initialized. Call init() first.")


class SimpleBaseLocalThreadDataInterface(SimpleBaseThreadHandler):
    ...


class SimpleBaseLocalThreadDataController(SimpleBaseThreadHandler):
    ...


class SimpleBaseLocalThreadDataGrouper(SimpleBaseThreadHandler):
    ...
