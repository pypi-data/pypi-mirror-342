from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class RadarPreHeaderMeasurementParam1Block(_message.Message):
    __slots__ = ("uicycleduration", "uinoiselevel")
    UICYCLEDURATION_FIELD_NUMBER: _ClassVar[int]
    UINOISELEVEL_FIELD_NUMBER: _ClassVar[int]
    uicycleduration: int
    uinoiselevel: int
    def __init__(self, uicycleduration: _Optional[int] = ..., uinoiselevel: _Optional[int] = ...) -> None: ...
