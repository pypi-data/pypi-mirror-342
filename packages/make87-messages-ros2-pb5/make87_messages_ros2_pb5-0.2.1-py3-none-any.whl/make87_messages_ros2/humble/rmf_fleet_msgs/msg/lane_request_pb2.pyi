from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LaneRequest(_message.Message):
    __slots__ = ("header", "fleet_name", "open_lanes", "close_lanes")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    FLEET_NAME_FIELD_NUMBER: _ClassVar[int]
    OPEN_LANES_FIELD_NUMBER: _ClassVar[int]
    CLOSE_LANES_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    fleet_name: str
    open_lanes: _containers.RepeatedScalarFieldContainer[int]
    close_lanes: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., fleet_name: _Optional[str] = ..., open_lanes: _Optional[_Iterable[int]] = ..., close_lanes: _Optional[_Iterable[int]] = ...) -> None: ...
