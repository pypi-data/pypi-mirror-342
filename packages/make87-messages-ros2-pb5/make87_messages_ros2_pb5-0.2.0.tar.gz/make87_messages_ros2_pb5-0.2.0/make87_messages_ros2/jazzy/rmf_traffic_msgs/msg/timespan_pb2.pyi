from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Timespan(_message.Message):
    __slots__ = ("maps", "has_lower_bound", "lower_bound", "has_upper_bound", "upper_bound")
    MAPS_FIELD_NUMBER: _ClassVar[int]
    HAS_LOWER_BOUND_FIELD_NUMBER: _ClassVar[int]
    LOWER_BOUND_FIELD_NUMBER: _ClassVar[int]
    HAS_UPPER_BOUND_FIELD_NUMBER: _ClassVar[int]
    UPPER_BOUND_FIELD_NUMBER: _ClassVar[int]
    maps: _containers.RepeatedScalarFieldContainer[str]
    has_lower_bound: bool
    lower_bound: int
    has_upper_bound: bool
    upper_bound: int
    def __init__(self, maps: _Optional[_Iterable[str]] = ..., has_lower_bound: bool = ..., lower_bound: _Optional[int] = ..., has_upper_bound: bool = ..., upper_bound: _Optional[int] = ...) -> None: ...
