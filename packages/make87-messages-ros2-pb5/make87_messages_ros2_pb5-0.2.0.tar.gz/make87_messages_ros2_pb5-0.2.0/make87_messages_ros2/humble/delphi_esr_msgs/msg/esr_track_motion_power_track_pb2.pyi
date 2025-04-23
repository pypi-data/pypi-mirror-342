from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EsrTrackMotionPowerTrack(_message.Message):
    __slots__ = ("header", "id", "movable_fast", "movable_slow", "moving", "power")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    MOVABLE_FAST_FIELD_NUMBER: _ClassVar[int]
    MOVABLE_SLOW_FIELD_NUMBER: _ClassVar[int]
    MOVING_FIELD_NUMBER: _ClassVar[int]
    POWER_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    id: int
    movable_fast: bool
    movable_slow: bool
    moving: bool
    power: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., id: _Optional[int] = ..., movable_fast: bool = ..., movable_slow: bool = ..., moving: bool = ..., power: _Optional[int] = ...) -> None: ...
