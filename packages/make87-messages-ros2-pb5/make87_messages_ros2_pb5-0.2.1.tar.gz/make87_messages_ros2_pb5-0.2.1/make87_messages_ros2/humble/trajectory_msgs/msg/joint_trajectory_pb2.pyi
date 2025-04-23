from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from make87_messages_ros2.humble.trajectory_msgs.msg import joint_trajectory_point_pb2 as _joint_trajectory_point_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class JointTrajectory(_message.Message):
    __slots__ = ("header", "ros2_header", "joint_names", "points")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    JOINT_NAMES_FIELD_NUMBER: _ClassVar[int]
    POINTS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    joint_names: _containers.RepeatedScalarFieldContainer[str]
    points: _containers.RepeatedCompositeFieldContainer[_joint_trajectory_point_pb2.JointTrajectoryPoint]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., joint_names: _Optional[_Iterable[str]] = ..., points: _Optional[_Iterable[_Union[_joint_trajectory_point_pb2.JointTrajectoryPoint, _Mapping]]] = ...) -> None: ...
