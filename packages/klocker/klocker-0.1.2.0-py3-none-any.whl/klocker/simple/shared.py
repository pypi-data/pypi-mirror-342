from typing import Self

from kmodels.models import CoreModel
from pydantic import ConfigDict, Field, model_validator

from klocker.simple.constants import ON_LOCKED_T


class SimpleBaseLockerThreadConfig(CoreModel):
    model_config = ConfigDict(frozen=True, extra='forbid')

    on_locked: ON_LOCKED_T = 'wait'
    timeout: float | None = Field(default=None, ge=0.0)

    @model_validator(mode='after')
    def _post_init(self) -> Self:
        if self.timeout == 0.0:
            self.timeout = None
        return self
