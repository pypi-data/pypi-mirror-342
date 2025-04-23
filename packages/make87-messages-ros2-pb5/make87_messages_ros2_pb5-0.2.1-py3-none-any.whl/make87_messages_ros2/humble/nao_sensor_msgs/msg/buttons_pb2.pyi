from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Buttons(_message.Message):
    __slots__ = ("header", "chest", "l_foot_bumper_left", "l_foot_bumper_right", "r_foot_bumper_left", "r_foot_bumper_right")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    CHEST_FIELD_NUMBER: _ClassVar[int]
    L_FOOT_BUMPER_LEFT_FIELD_NUMBER: _ClassVar[int]
    L_FOOT_BUMPER_RIGHT_FIELD_NUMBER: _ClassVar[int]
    R_FOOT_BUMPER_LEFT_FIELD_NUMBER: _ClassVar[int]
    R_FOOT_BUMPER_RIGHT_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    chest: bool
    l_foot_bumper_left: bool
    l_foot_bumper_right: bool
    r_foot_bumper_left: bool
    r_foot_bumper_right: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., chest: bool = ..., l_foot_bumper_left: bool = ..., l_foot_bumper_right: bool = ..., r_foot_bumper_left: bool = ..., r_foot_bumper_right: bool = ...) -> None: ...
