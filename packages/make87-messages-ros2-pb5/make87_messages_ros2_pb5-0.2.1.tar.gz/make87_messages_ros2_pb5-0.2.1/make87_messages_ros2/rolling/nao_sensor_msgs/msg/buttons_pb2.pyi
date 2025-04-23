from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Buttons(_message.Message):
    __slots__ = ("chest", "l_foot_bumper_left", "l_foot_bumper_right", "r_foot_bumper_left", "r_foot_bumper_right")
    CHEST_FIELD_NUMBER: _ClassVar[int]
    L_FOOT_BUMPER_LEFT_FIELD_NUMBER: _ClassVar[int]
    L_FOOT_BUMPER_RIGHT_FIELD_NUMBER: _ClassVar[int]
    R_FOOT_BUMPER_LEFT_FIELD_NUMBER: _ClassVar[int]
    R_FOOT_BUMPER_RIGHT_FIELD_NUMBER: _ClassVar[int]
    chest: bool
    l_foot_bumper_left: bool
    l_foot_bumper_right: bool
    r_foot_bumper_left: bool
    r_foot_bumper_right: bool
    def __init__(self, chest: bool = ..., l_foot_bumper_left: bool = ..., l_foot_bumper_right: bool = ..., r_foot_bumper_left: bool = ..., r_foot_bumper_right: bool = ...) -> None: ...
