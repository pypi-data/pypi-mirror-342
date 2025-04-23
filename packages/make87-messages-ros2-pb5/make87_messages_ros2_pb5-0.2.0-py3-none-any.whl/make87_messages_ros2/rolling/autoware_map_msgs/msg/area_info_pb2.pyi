from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class AreaInfo(_message.Message):
    __slots__ = ("center_x", "center_y", "radius")
    CENTER_X_FIELD_NUMBER: _ClassVar[int]
    CENTER_Y_FIELD_NUMBER: _ClassVar[int]
    RADIUS_FIELD_NUMBER: _ClassVar[int]
    center_x: float
    center_y: float
    radius: float
    def __init__(self, center_x: _Optional[float] = ..., center_y: _Optional[float] = ..., radius: _Optional[float] = ...) -> None: ...
