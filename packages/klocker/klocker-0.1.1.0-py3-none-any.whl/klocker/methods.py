import inspect
from functools import wraps
from typing import Literal, get_args, Callable, ParamSpec, TypeVar, Concatenate
from klocker.interface import LockerInterface

ON_BLOCKED_T = Literal['wait', 'leave', 'raise']
ON_BLOCKED: tuple[ON_BLOCKED_T, ...] = get_args(ON_BLOCKED_T)

P = ParamSpec("P")
R = TypeVar("R")


def execute_with_locker(
        locker: LockerInterface, func: Callable[Concatenate[LockerInterface, P], R],
        pass_locker: bool,
        *args: P.args,
        **kwargs: P.kwargs
) -> R:
    """
    Helper function to execute a function with or without passing the locker.

    :param locker: The locker instance.
    :param func: The function to execute.
    :param pass_locker: Whether to pass the locker as the first argument.
    :param args: Positional arguments for the function.
    :param kwargs: Keyword arguments for the function.
    :return: The result of the function execution.
    """
    if pass_locker:
        sig = inspect.signature(func)
        params = list(sig.parameters.values())
        if not params or not isinstance(locker, params[0].annotation):
            raise TypeError(f"The first parameter of {func.__name__} must be of type {type(locker).__name__}.")

    with locker:
        return func(locker, *args, **kwargs) if pass_locker else func(*args, **kwargs)


def create_locker_wrapper(
        locker: LockerInterface, func: Callable[Concatenate[LockerInterface, P], R],
        pass_locker: bool
) -> Callable[Concatenate[LockerInterface, P], R]:
    """
    Helper function to create a wrapper for a function to execute it with or without passing the locker.

    :param locker: The locker instance.
    :param func: The function to wrap.
    :param pass_locker: Whether to pass the locker as the first argument.
    :return: The wrapped function.
    """

    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        return execute_with_locker(locker, func, pass_locker, *args, **kwargs)

    return wrapper
