from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class EStopRequest(_message.Message):
    __slots__ = ("e_stop_on",)
    E_STOP_ON_FIELD_NUMBER: _ClassVar[int]
    e_stop_on: bool
    def __init__(self, e_stop_on: bool = ...) -> None: ...

class EStopResponse(_message.Message):
    __slots__ = ("success", "message")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    def __init__(self, success: bool = ..., message: _Optional[str] = ...) -> None: ...
