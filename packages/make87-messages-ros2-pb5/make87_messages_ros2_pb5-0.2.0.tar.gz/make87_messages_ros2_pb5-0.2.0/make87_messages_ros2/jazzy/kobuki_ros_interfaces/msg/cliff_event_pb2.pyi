from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class CliffEvent(_message.Message):
    __slots__ = ("sensor", "state", "bottom")
    SENSOR_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    BOTTOM_FIELD_NUMBER: _ClassVar[int]
    sensor: int
    state: int
    bottom: int
    def __init__(self, sensor: _Optional[int] = ..., state: _Optional[int] = ..., bottom: _Optional[int] = ...) -> None: ...
