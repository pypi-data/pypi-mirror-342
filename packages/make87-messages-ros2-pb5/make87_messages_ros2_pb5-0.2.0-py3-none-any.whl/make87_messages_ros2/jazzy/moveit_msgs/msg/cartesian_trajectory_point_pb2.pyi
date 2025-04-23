from make87_messages_ros2.jazzy.builtin_interfaces.msg import duration_pb2 as _duration_pb2
from make87_messages_ros2.jazzy.moveit_msgs.msg import cartesian_point_pb2 as _cartesian_point_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CartesianTrajectoryPoint(_message.Message):
    __slots__ = ("point", "time_from_start")
    POINT_FIELD_NUMBER: _ClassVar[int]
    TIME_FROM_START_FIELD_NUMBER: _ClassVar[int]
    point: _cartesian_point_pb2.CartesianPoint
    time_from_start: _duration_pb2.Duration
    def __init__(self, point: _Optional[_Union[_cartesian_point_pb2.CartesianPoint, _Mapping]] = ..., time_from_start: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...) -> None: ...
