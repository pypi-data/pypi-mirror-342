from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.rmf_fleet_msgs.msg import robot_state_pb2 as _robot_state_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class FleetState(_message.Message):
    __slots__ = ("header", "name", "robots")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ROBOTS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    name: str
    robots: _containers.RepeatedCompositeFieldContainer[_robot_state_pb2.RobotState]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., name: _Optional[str] = ..., robots: _Optional[_Iterable[_Union[_robot_state_pb2.RobotState, _Mapping]]] = ...) -> None: ...
