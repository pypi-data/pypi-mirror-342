from typing import Literal, get_args, ParamSpec, TypeVar

ON_BLOCKED_T = Literal['wait', 'leave', 'raise']
ON_BLOCKED: tuple[ON_BLOCKED_T, ...] = get_args(ON_BLOCKED_T)

P = ParamSpec("P")
R = TypeVar("R")
