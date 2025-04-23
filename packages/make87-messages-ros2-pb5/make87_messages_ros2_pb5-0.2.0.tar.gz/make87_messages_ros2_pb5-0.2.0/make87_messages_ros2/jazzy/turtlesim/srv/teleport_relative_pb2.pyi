from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class TeleportRelativeRequest(_message.Message):
    __slots__ = ("linear", "angular")
    LINEAR_FIELD_NUMBER: _ClassVar[int]
    ANGULAR_FIELD_NUMBER: _ClassVar[int]
    linear: float
    angular: float
    def __init__(self, linear: _Optional[float] = ..., angular: _Optional[float] = ...) -> None: ...

class TeleportRelativeResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
