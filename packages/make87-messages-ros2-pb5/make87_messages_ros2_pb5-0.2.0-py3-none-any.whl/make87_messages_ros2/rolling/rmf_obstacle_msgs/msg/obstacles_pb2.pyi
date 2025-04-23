from make87_messages_ros2.rolling.rmf_obstacle_msgs.msg import obstacle_pb2 as _obstacle_pb2
from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Obstacles(_message.Message):
    __slots__ = ("header", "obstacles")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    OBSTACLES_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    obstacles: _containers.RepeatedCompositeFieldContainer[_obstacle_pb2.Obstacle]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., obstacles: _Optional[_Iterable[_Union[_obstacle_pb2.Obstacle, _Mapping]]] = ...) -> None: ...
