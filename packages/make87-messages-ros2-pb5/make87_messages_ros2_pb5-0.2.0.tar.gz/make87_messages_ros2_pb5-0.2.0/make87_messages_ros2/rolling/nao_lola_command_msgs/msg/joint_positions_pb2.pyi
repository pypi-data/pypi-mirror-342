from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class JointPositions(_message.Message):
    __slots__ = ("indexes", "positions")
    INDEXES_FIELD_NUMBER: _ClassVar[int]
    POSITIONS_FIELD_NUMBER: _ClassVar[int]
    indexes: _containers.RepeatedScalarFieldContainer[int]
    positions: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, indexes: _Optional[_Iterable[int]] = ..., positions: _Optional[_Iterable[float]] = ...) -> None: ...
