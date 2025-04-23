from make87_messages_ros2.jazzy.geometry_msgs.msg import point_pb2 as _point_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PointWithCovariance(_message.Message):
    __slots__ = ("point", "covariance")
    POINT_FIELD_NUMBER: _ClassVar[int]
    COVARIANCE_FIELD_NUMBER: _ClassVar[int]
    point: _point_pb2.Point
    covariance: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, point: _Optional[_Union[_point_pb2.Point, _Mapping]] = ..., covariance: _Optional[_Iterable[float]] = ...) -> None: ...
