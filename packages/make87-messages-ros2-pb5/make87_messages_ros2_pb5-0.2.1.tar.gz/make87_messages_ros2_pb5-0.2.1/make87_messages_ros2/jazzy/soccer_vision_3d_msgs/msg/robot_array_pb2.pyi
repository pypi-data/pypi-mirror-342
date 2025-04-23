from make87_messages_ros2.jazzy.soccer_vision_3d_msgs.msg import robot_pb2 as _robot_pb2
from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RobotArray(_message.Message):
    __slots__ = ("header", "robots")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROBOTS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    robots: _containers.RepeatedCompositeFieldContainer[_robot_pb2.Robot]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., robots: _Optional[_Iterable[_Union[_robot_pb2.Robot, _Mapping]]] = ...) -> None: ...
