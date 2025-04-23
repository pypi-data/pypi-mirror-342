from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BlockadeCheckpoint(_message.Message):
    __slots__ = ("header", "position", "map_name", "can_hold")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    MAP_NAME_FIELD_NUMBER: _ClassVar[int]
    CAN_HOLD_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    position: _containers.RepeatedScalarFieldContainer[float]
    map_name: str
    can_hold: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., position: _Optional[_Iterable[float]] = ..., map_name: _Optional[str] = ..., can_hold: bool = ...) -> None: ...
