from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Circle(_message.Message):
    __slots__ = ("radius",)
    RADIUS_FIELD_NUMBER: _ClassVar[int]
    radius: float
    def __init__(self, radius: _Optional[float] = ...) -> None: ...
