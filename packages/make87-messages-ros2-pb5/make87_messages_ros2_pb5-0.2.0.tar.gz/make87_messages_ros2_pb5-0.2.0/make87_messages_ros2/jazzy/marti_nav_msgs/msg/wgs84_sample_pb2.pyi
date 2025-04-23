from make87_messages_ros2.jazzy.geometry_msgs.msg import point_pb2 as _point_pb2
from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Wgs84Sample(_message.Message):
    __slots__ = ("header", "odom", "wgs84", "wgs84_covariance")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ODOM_FIELD_NUMBER: _ClassVar[int]
    WGS84_FIELD_NUMBER: _ClassVar[int]
    WGS84_COVARIANCE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    odom: _point_pb2.Point
    wgs84: _point_pb2.Point
    wgs84_covariance: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., odom: _Optional[_Union[_point_pb2.Point, _Mapping]] = ..., wgs84: _Optional[_Union[_point_pb2.Point, _Mapping]] = ..., wgs84_covariance: _Optional[_Iterable[float]] = ...) -> None: ...
