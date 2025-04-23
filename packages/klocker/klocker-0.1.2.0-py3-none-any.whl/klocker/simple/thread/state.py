import threading
from kmodels.models import CoreModel
from kmodels.types import OmitIfUnset, Unset, unset
from pydantic import ConfigDict, model_validator

from klocker.simple.constants import LOCK_FAILURE_T
from klocker.simple.thread.base import SimpleBaseLocalThreadDataInterface, SimpleBaseLocalThreadDataController


class SimpleThreadLockFailureDetails(CoreModel):
    model_config = ConfigDict(frozen=True, extra='forbid', arbitrary_types_allowed=True)
    reason: LOCK_FAILURE_T
    exception: OmitIfUnset[BaseException | Unset] = unset

    @model_validator(mode='after')
    def reason_consistency(self):
        if self.reason == 'exception' and self.exception is unset:
            raise ValueError(f'If exception happened you have to set `exception` to the exception that happened.')
        return self


class SimpleLocalThreadState(CoreModel):
    model_config = ConfigDict(frozen=True, extra='forbid')
    acquired: bool = False
    waited: bool = False
    failure_details: OmitIfUnset[SimpleThreadLockFailureDetails | Unset] = unset


class SimpleLocalThreadStateInterface(SimpleBaseLocalThreadDataInterface):
    def __init__(self, local_env: threading.local):
        super().__init__(local_env, 'state')

    @property
    def data(self) -> SimpleLocalThreadState:
        self._raise_not_initialized()
        return self._local_env.state

    @property
    def acquired(self) -> bool:
        return self.data.acquired

    @property
    def waited(self) -> bool:
        return self.data.waited

    @property
    def failure_details(self) -> SimpleThreadLockFailureDetails | None:
        return self.data.failure_details


class SimpleLocalThreadStateController(SimpleBaseLocalThreadDataController):
    def __init__(self, local_env: threading.local):
        super().__init__(local_env, 'state')

    def initialize(
            self,
            *,
            acquired: bool = False,
            waited: bool = False,
            failure_details: SimpleThreadLockFailureDetails | Unset = unset
    ):
        self._raise_already_initialized()
        self._local_env.state = SimpleLocalThreadState(acquired=acquired, waited=waited, failure_details=failure_details)

    def initialize_from_state(self, state: SimpleLocalThreadState):
        return self.initialize(acquired=state.acquired, waited=state.waited, failure_details=state.failure_details)
