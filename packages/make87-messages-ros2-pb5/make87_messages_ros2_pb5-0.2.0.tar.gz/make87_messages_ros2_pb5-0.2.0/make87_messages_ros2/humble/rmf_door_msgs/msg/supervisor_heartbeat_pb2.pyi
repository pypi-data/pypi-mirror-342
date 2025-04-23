from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.rmf_door_msgs.msg import door_sessions_pb2 as _door_sessions_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SupervisorHeartbeat(_message.Message):
    __slots__ = ("header", "all_sessions")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ALL_SESSIONS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    all_sessions: _containers.RepeatedCompositeFieldContainer[_door_sessions_pb2.DoorSessions]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., all_sessions: _Optional[_Iterable[_Union[_door_sessions_pb2.DoorSessions, _Mapping]]] = ...) -> None: ...
