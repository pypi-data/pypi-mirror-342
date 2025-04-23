from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ScheduleQueryParticipants(_message.Message):
    __slots__ = ("type", "ids")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    IDS_FIELD_NUMBER: _ClassVar[int]
    type: int
    ids: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, type: _Optional[int] = ..., ids: _Optional[_Iterable[int]] = ...) -> None: ...
