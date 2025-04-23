from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class SensorData(_message.Message):
    __slots__ = ("distance", "warn", "alarm", "active")
    DISTANCE_FIELD_NUMBER: _ClassVar[int]
    WARN_FIELD_NUMBER: _ClassVar[int]
    ALARM_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_FIELD_NUMBER: _ClassVar[int]
    distance: int
    warn: bool
    alarm: bool
    active: bool
    def __init__(self, distance: _Optional[int] = ..., warn: bool = ..., alarm: bool = ..., active: bool = ...) -> None: ...
