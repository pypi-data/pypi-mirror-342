from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class TrafficLightElement(_message.Message):
    __slots__ = ("color", "shape", "status", "confidence")
    COLOR_FIELD_NUMBER: _ClassVar[int]
    SHAPE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    CONFIDENCE_FIELD_NUMBER: _ClassVar[int]
    color: int
    shape: int
    status: int
    confidence: float
    def __init__(self, color: _Optional[int] = ..., shape: _Optional[int] = ..., status: _Optional[int] = ..., confidence: _Optional[float] = ...) -> None: ...
