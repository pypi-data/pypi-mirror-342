from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MutexGroupManualRelease(_message.Message):
    __slots__ = ("header", "release_mutex_groups", "fleet", "robot")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    RELEASE_MUTEX_GROUPS_FIELD_NUMBER: _ClassVar[int]
    FLEET_FIELD_NUMBER: _ClassVar[int]
    ROBOT_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    release_mutex_groups: _containers.RepeatedScalarFieldContainer[str]
    fleet: str
    robot: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., release_mutex_groups: _Optional[_Iterable[str]] = ..., fleet: _Optional[str] = ..., robot: _Optional[str] = ...) -> None: ...
