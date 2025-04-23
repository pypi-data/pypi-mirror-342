from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class LightSensors(_message.Message):
    __slots__ = ("forward_r", "forward_l", "left", "right")
    FORWARD_R_FIELD_NUMBER: _ClassVar[int]
    FORWARD_L_FIELD_NUMBER: _ClassVar[int]
    LEFT_FIELD_NUMBER: _ClassVar[int]
    RIGHT_FIELD_NUMBER: _ClassVar[int]
    forward_r: int
    forward_l: int
    left: int
    right: int
    def __init__(self, forward_r: _Optional[int] = ..., forward_l: _Optional[int] = ..., left: _Optional[int] = ..., right: _Optional[int] = ...) -> None: ...
