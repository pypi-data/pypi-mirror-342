from kmodels.types import Unset, unset
from pydantic import Field, ConfigDict
from klocker.simple.constants import ON_LOCKED_T, CALLBACK_T
from klocker.simple.shared import SimpleBaseLockerThreadConfig


class SimpleLockerConfig(SimpleBaseLockerThreadConfig):
    """
    Configuration class for the locker thread.

    Attributes:
        stop_event_delay (float): Delay before stopping the event, must be greater than 0.
        stop_timeout (float | None): Timeout for stopping, must be greater than 0 or None.
        callback (CALLBACK_T): Callback function to execute.
        warnings (bool): Flag to enable or disable warnings.
        stop_event_warnings (bool): Flag to enable or disable stop event warnings.
    """
    model_config = ConfigDict(frozen=True, extra='forbid')

    stop_event_delay: float = Field(default=0.1, gt=0.0)
    stop_timeout: float | None = Field(default=None, gt=0.0)
    callback: CALLBACK_T = Field(default=None)
    allow_stop_from_threads: bool = Field(default=False)
    warnings: bool = True
    stop_event_warnings: bool = True


class BaseSimpleLockerConfig:
    """
    Base class for locker configuration management.

    Attributes:
        _config (SimpleLockerConfig): The locker configuration instance.
    """

    def __init__(self, config: SimpleLockerConfig):
        """
        Initialize the base locker configuration.

        Args:
            config (SimpleLockerConfig): The locker configuration instance.
        """
        self._config = config

    def get_config(self) -> SimpleLockerConfig:
        """
        Retrieve the current locker configuration.

        Returns:
            SimpleLockerConfig: The current locker configuration.
        """
        return self._config


class SimpleLockerConfigInterface(BaseSimpleLockerConfig):
    """
    Interface class for accessing locker configuration properties.
    """

    @property
    def on_locked(self) -> ON_LOCKED_T:
        """
        Returns the current on_locked configuration.

        Returns:
            ON_LOCKED_T: The on_locked configuration.
        """
        return self._config.on_locked

    @property
    def timeout(self) -> float | None:
        """
        Returns the current timeout configuration.

        Returns:
            float | None: The timeout value or None.
        """
        return self._config.timeout

    @property
    def stop_event_delay(self) -> float:
        """
        Returns the stop event delay configuration.

        Returns:
            float: The stop event delay value.
        """
        return self._config.stop_event_delay

    @property
    def stop_timeout(self) -> float | None:
        """
        Returns the stop timeout configuration.

        Returns:
            float | None: The stop timeout value or None.
        """
        return self._config.stop_timeout

    @property
    def callback(self) -> CALLBACK_T:
        """
        Returns the callback configuration.

        Returns:
            CALLBACK_T: The callback function.
        """
        return self._config.callback

    @property
    def allow_stop_from_threads(self) -> bool:
        """
        Returns the allow stop from threads configuration.

        Returns:
            bool: True if stopping from threads is allowed, False otherwise.
        """
        return self._config.allow_stop_from_threads

    @property
    def warnings(self) -> bool:
        """
        Returns the warnings configuration.

        Returns:
            bool: True if warnings are enabled, False otherwise.
        """
        return self._config.warnings

    @property
    def stop_event_warnings(self) -> bool:
        """
        Returns the stop event warnings configuration.

        Returns:
            bool: True if stop event warnings are enabled, False otherwise.
        """
        return self._config.stop_event_warnings


class SimpleLockerConfigController(BaseSimpleLockerConfig):
    """
    Controller class for modifying locker configuration.
    """

    def set_config(self, config: SimpleLockerConfig):
        """
        Set a new locker configuration.

        Args:
            config (SimpleLockerConfig): The new locker configuration instance.
        """
        self.update_config(on_locked=config.on_locked, timeout=config.timeout)

    def update_config(self, *, on_locked: ON_LOCKED_T | None = None, timeout: float | None = None):
        """
        Update specific fields in the locker configuration.

        Args:
            on_locked (ON_LOCKED_T | None): The new on_locked configuration.
            timeout (float | None): The new timeout value.
        """
        self._config = self._config.update(on_locked=on_locked, timeout=timeout)


class SimpleLockerConfigHandler:
    """
    Handler class for managing locker configuration, providing both interface and controller.

    Attributes:
        _config (SimpleLockerConfig): The locker configuration instance.
        _interface (SimpleLockerConfigInterface): The interface for accessing configuration properties.
        _controller (SimpleLockerConfigController): The controller for modifying configuration properties.
    """

    def __init__(self, *, config: SimpleLockerConfig | Unset = unset):
        """
        Initialize the locker configuration handler.

        Args:
            config (SimpleLockerConfig | Unset): The locker configuration instance or unset.
        """
        self._config = config if config is not unset else SimpleLockerConfig()
        self._interface = SimpleLockerConfigInterface(self._config)
        self._controller = SimpleLockerConfigController(self._config)

    @property
    def interface(self) -> SimpleLockerConfigInterface:
        """
        Access the configuration interface.

        Returns:
            SimpleLockerConfigInterface: The interface for accessing configuration properties.
        """
        return self._interface

    @property
    def controller(self) -> SimpleLockerConfigController:
        """
        Access the configuration controller.

        Returns:
            SimpleLockerConfigController: The controller for modifying configuration properties.
        """
        return self._controller
