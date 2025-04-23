from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Motion(_message.Message):
    __slots__ = ("header", "key", "name", "usage", "description", "joints", "positions", "times_from_start")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    USAGE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    JOINTS_FIELD_NUMBER: _ClassVar[int]
    POSITIONS_FIELD_NUMBER: _ClassVar[int]
    TIMES_FROM_START_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    key: str
    name: str
    usage: str
    description: str
    joints: _containers.RepeatedScalarFieldContainer[str]
    positions: _containers.RepeatedScalarFieldContainer[float]
    times_from_start: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., key: _Optional[str] = ..., name: _Optional[str] = ..., usage: _Optional[str] = ..., description: _Optional[str] = ..., joints: _Optional[_Iterable[str]] = ..., positions: _Optional[_Iterable[float]] = ..., times_from_start: _Optional[_Iterable[float]] = ...) -> None: ...
