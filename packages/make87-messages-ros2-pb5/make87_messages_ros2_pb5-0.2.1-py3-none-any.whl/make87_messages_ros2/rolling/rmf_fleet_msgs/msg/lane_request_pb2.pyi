from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class LaneRequest(_message.Message):
    __slots__ = ("fleet_name", "open_lanes", "close_lanes")
    FLEET_NAME_FIELD_NUMBER: _ClassVar[int]
    OPEN_LANES_FIELD_NUMBER: _ClassVar[int]
    CLOSE_LANES_FIELD_NUMBER: _ClassVar[int]
    fleet_name: str
    open_lanes: _containers.RepeatedScalarFieldContainer[int]
    close_lanes: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, fleet_name: _Optional[str] = ..., open_lanes: _Optional[_Iterable[int]] = ..., close_lanes: _Optional[_Iterable[int]] = ...) -> None: ...
