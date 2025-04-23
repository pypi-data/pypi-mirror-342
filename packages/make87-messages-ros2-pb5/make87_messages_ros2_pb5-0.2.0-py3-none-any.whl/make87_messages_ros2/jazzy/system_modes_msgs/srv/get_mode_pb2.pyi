from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class GetModeRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetModeResponse(_message.Message):
    __slots__ = ("current_mode",)
    CURRENT_MODE_FIELD_NUMBER: _ClassVar[int]
    current_mode: str
    def __init__(self, current_mode: _Optional[str] = ...) -> None: ...
