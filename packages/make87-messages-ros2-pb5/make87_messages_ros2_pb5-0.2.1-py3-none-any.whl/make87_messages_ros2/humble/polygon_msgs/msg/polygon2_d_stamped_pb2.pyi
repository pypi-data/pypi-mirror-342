from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.polygon_msgs.msg import polygon2_d_pb2 as _polygon2_d_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Polygon2DStamped(_message.Message):
    __slots__ = ("header", "ros2_header", "polygon")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    POLYGON_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    polygon: _polygon2_d_pb2.Polygon2D
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., polygon: _Optional[_Union[_polygon2_d_pb2.Polygon2D, _Mapping]] = ...) -> None: ...
