from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ClosedLanes(_message.Message):
    __slots__ = ("fleet_name", "closed_lanes")
    FLEET_NAME_FIELD_NUMBER: _ClassVar[int]
    CLOSED_LANES_FIELD_NUMBER: _ClassVar[int]
    fleet_name: str
    closed_lanes: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, fleet_name: _Optional[str] = ..., closed_lanes: _Optional[_Iterable[int]] = ...) -> None: ...
