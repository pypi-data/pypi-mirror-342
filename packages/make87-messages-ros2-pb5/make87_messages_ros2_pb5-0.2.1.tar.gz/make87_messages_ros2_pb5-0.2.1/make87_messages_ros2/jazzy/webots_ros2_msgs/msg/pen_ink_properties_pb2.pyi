from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class PenInkProperties(_message.Message):
    __slots__ = ("color", "density")
    COLOR_FIELD_NUMBER: _ClassVar[int]
    DENSITY_FIELD_NUMBER: _ClassVar[int]
    color: int
    density: float
    def __init__(self, color: _Optional[int] = ..., density: _Optional[float] = ...) -> None: ...
