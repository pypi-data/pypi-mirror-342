from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class MutexGroupManualRelease(_message.Message):
    __slots__ = ("release_mutex_groups", "fleet", "robot")
    RELEASE_MUTEX_GROUPS_FIELD_NUMBER: _ClassVar[int]
    FLEET_FIELD_NUMBER: _ClassVar[int]
    ROBOT_FIELD_NUMBER: _ClassVar[int]
    release_mutex_groups: _containers.RepeatedScalarFieldContainer[str]
    fleet: str
    robot: str
    def __init__(self, release_mutex_groups: _Optional[_Iterable[str]] = ..., fleet: _Optional[str] = ..., robot: _Optional[str] = ...) -> None: ...
