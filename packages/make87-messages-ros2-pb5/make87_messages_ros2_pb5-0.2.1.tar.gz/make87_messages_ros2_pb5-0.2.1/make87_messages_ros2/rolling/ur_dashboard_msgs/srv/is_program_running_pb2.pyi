from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class IsProgramRunningRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class IsProgramRunningResponse(_message.Message):
    __slots__ = ("answer", "program_running", "success")
    ANSWER_FIELD_NUMBER: _ClassVar[int]
    PROGRAM_RUNNING_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    answer: str
    program_running: bool
    success: bool
    def __init__(self, answer: _Optional[str] = ..., program_running: bool = ..., success: bool = ...) -> None: ...
