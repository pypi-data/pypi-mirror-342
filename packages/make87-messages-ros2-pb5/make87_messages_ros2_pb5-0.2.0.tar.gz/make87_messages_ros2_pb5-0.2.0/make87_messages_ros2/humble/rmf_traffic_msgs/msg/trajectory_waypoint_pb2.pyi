from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TrajectoryWaypoint(_message.Message):
    __slots__ = ("header", "time", "position", "velocity")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    VELOCITY_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    time: int
    position: _containers.RepeatedScalarFieldContainer[float]
    velocity: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., time: _Optional[int] = ..., position: _Optional[_Iterable[float]] = ..., velocity: _Optional[_Iterable[float]] = ...) -> None: ...
