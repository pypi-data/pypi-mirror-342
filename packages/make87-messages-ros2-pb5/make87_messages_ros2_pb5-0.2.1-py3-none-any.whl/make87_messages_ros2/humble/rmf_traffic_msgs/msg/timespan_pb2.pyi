from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Timespan(_message.Message):
    __slots__ = ("header", "maps", "has_lower_bound", "lower_bound", "has_upper_bound", "upper_bound")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    MAPS_FIELD_NUMBER: _ClassVar[int]
    HAS_LOWER_BOUND_FIELD_NUMBER: _ClassVar[int]
    LOWER_BOUND_FIELD_NUMBER: _ClassVar[int]
    HAS_UPPER_BOUND_FIELD_NUMBER: _ClassVar[int]
    UPPER_BOUND_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    maps: _containers.RepeatedScalarFieldContainer[str]
    has_lower_bound: bool
    lower_bound: int
    has_upper_bound: bool
    upper_bound: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., maps: _Optional[_Iterable[str]] = ..., has_lower_bound: bool = ..., lower_bound: _Optional[int] = ..., has_upper_bound: bool = ..., upper_bound: _Optional[int] = ...) -> None: ...
