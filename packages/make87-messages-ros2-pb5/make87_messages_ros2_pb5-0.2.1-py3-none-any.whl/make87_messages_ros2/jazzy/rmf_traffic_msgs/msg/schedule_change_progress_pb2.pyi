from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ScheduleChangeProgress(_message.Message):
    __slots__ = ("has_progress", "version", "checkpoints")
    HAS_PROGRESS_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    CHECKPOINTS_FIELD_NUMBER: _ClassVar[int]
    has_progress: bool
    version: int
    checkpoints: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, has_progress: bool = ..., version: _Optional[int] = ..., checkpoints: _Optional[_Iterable[int]] = ...) -> None: ...
