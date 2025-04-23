class LockerException(Exception):
    """Base class for all locker-related exceptions."""
    ...


class LockerLocked(LockerException):
    """Excepción lanzada cuando se intenta adquirir un bloqueo y se decide no esperar."""

    def __init__(self):
        super().__init__("No se pudo adquirir el bloqueo.")


class StoppingLocker(LockerException):
    def __init__(self):
        super().__init__("El locker está en proceso de detención.")
