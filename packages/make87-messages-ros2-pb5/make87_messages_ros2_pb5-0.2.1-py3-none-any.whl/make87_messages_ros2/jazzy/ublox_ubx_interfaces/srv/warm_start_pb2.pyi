from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class WarmStartRequest(_message.Message):
    __slots__ = ("reset_type",)
    RESET_TYPE_FIELD_NUMBER: _ClassVar[int]
    reset_type: int
    def __init__(self, reset_type: _Optional[int] = ...) -> None: ...

class WarmStartResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
