from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import point_pb2 as _point_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PositionFused(_message.Message):
    __slots__ = ("header", "ros2_header", "position", "x_health", "y_health", "z_health")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    X_HEALTH_FIELD_NUMBER: _ClassVar[int]
    Y_HEALTH_FIELD_NUMBER: _ClassVar[int]
    Z_HEALTH_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    position: _point_pb2.Point
    x_health: int
    y_health: int
    z_health: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., position: _Optional[_Union[_point_pb2.Point, _Mapping]] = ..., x_health: _Optional[int] = ..., y_health: _Optional[int] = ..., z_health: _Optional[int] = ...) -> None: ...
