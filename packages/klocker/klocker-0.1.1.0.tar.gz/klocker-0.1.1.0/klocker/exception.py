class LockerLocked(Exception):
    """Excepción lanzada cuando se intenta adquirir un bloqueo y se decide no esperar."""

    def __init__(self):
        super().__init__("No se pudo adquirir el bloqueo.")
