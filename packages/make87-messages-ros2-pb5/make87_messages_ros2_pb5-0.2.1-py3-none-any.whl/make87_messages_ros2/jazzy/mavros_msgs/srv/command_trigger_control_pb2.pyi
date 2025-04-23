from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class CommandTriggerControlRequest(_message.Message):
    __slots__ = ("trigger_enable", "sequence_reset", "trigger_pause")
    TRIGGER_ENABLE_FIELD_NUMBER: _ClassVar[int]
    SEQUENCE_RESET_FIELD_NUMBER: _ClassVar[int]
    TRIGGER_PAUSE_FIELD_NUMBER: _ClassVar[int]
    trigger_enable: bool
    sequence_reset: bool
    trigger_pause: bool
    def __init__(self, trigger_enable: bool = ..., sequence_reset: bool = ..., trigger_pause: bool = ...) -> None: ...

class CommandTriggerControlResponse(_message.Message):
    __slots__ = ("success", "result")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    success: bool
    result: int
    def __init__(self, success: bool = ..., result: _Optional[int] = ...) -> None: ...
