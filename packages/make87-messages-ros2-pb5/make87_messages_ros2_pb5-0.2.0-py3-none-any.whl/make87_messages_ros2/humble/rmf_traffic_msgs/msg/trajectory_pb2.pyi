from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.rmf_traffic_msgs.msg import trajectory_waypoint_pb2 as _trajectory_waypoint_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Trajectory(_message.Message):
    __slots__ = ("header", "waypoints")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    WAYPOINTS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    waypoints: _containers.RepeatedCompositeFieldContainer[_trajectory_waypoint_pb2.TrajectoryWaypoint]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., waypoints: _Optional[_Iterable[_Union[_trajectory_waypoint_pb2.TrajectoryWaypoint, _Mapping]]] = ...) -> None: ...
