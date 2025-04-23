from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class CommandTriggerIntervalRequest(_message.Message):
    __slots__ = ("cycle_time", "integration_time")
    CYCLE_TIME_FIELD_NUMBER: _ClassVar[int]
    INTEGRATION_TIME_FIELD_NUMBER: _ClassVar[int]
    cycle_time: float
    integration_time: float
    def __init__(self, cycle_time: _Optional[float] = ..., integration_time: _Optional[float] = ...) -> None: ...

class CommandTriggerIntervalResponse(_message.Message):
    __slots__ = ("success", "result")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    success: bool
    result: int
    def __init__(self, success: bool = ..., result: _Optional[int] = ...) -> None: ...
