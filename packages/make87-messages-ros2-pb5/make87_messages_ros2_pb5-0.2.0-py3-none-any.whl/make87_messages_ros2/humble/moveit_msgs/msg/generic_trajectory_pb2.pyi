from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.moveit_msgs.msg import cartesian_trajectory_pb2 as _cartesian_trajectory_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from make87_messages_ros2.humble.trajectory_msgs.msg import joint_trajectory_pb2 as _joint_trajectory_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GenericTrajectory(_message.Message):
    __slots__ = ("header", "ros2_header", "joint_trajectory", "cartesian_trajectory")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    JOINT_TRAJECTORY_FIELD_NUMBER: _ClassVar[int]
    CARTESIAN_TRAJECTORY_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    joint_trajectory: _containers.RepeatedCompositeFieldContainer[_joint_trajectory_pb2.JointTrajectory]
    cartesian_trajectory: _containers.RepeatedCompositeFieldContainer[_cartesian_trajectory_pb2.CartesianTrajectory]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., joint_trajectory: _Optional[_Iterable[_Union[_joint_trajectory_pb2.JointTrajectory, _Mapping]]] = ..., cartesian_trajectory: _Optional[_Iterable[_Union[_cartesian_trajectory_pb2.CartesianTrajectory, _Mapping]]] = ...) -> None: ...
