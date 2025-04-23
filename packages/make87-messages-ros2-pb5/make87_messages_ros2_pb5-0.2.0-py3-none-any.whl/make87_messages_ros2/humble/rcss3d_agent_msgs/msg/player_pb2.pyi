from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.rcss3d_agent_msgs.msg import spherical_pb2 as _spherical_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Player(_message.Message):
    __slots__ = ("header", "team", "id", "head", "rlowerarm", "llowerarm", "rfoot", "lfoot")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TEAM_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    HEAD_FIELD_NUMBER: _ClassVar[int]
    RLOWERARM_FIELD_NUMBER: _ClassVar[int]
    LLOWERARM_FIELD_NUMBER: _ClassVar[int]
    RFOOT_FIELD_NUMBER: _ClassVar[int]
    LFOOT_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    team: str
    id: int
    head: _containers.RepeatedCompositeFieldContainer[_spherical_pb2.Spherical]
    rlowerarm: _containers.RepeatedCompositeFieldContainer[_spherical_pb2.Spherical]
    llowerarm: _containers.RepeatedCompositeFieldContainer[_spherical_pb2.Spherical]
    rfoot: _containers.RepeatedCompositeFieldContainer[_spherical_pb2.Spherical]
    lfoot: _containers.RepeatedCompositeFieldContainer[_spherical_pb2.Spherical]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., team: _Optional[str] = ..., id: _Optional[int] = ..., head: _Optional[_Iterable[_Union[_spherical_pb2.Spherical, _Mapping]]] = ..., rlowerarm: _Optional[_Iterable[_Union[_spherical_pb2.Spherical, _Mapping]]] = ..., llowerarm: _Optional[_Iterable[_Union[_spherical_pb2.Spherical, _Mapping]]] = ..., rfoot: _Optional[_Iterable[_Union[_spherical_pb2.Spherical, _Mapping]]] = ..., lfoot: _Optional[_Iterable[_Union[_spherical_pb2.Spherical, _Mapping]]] = ...) -> None: ...
