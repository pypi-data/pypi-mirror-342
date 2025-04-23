from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import accel_pb2 as _accel_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import pose_pb2 as _pose_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import twist_pb2 as _twist_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CartesianPoint(_message.Message):
    __slots__ = ("header", "pose", "velocity", "acceleration")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    POSE_FIELD_NUMBER: _ClassVar[int]
    VELOCITY_FIELD_NUMBER: _ClassVar[int]
    ACCELERATION_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    pose: _pose_pb2.Pose
    velocity: _twist_pb2.Twist
    acceleration: _accel_pb2.Accel
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., pose: _Optional[_Union[_pose_pb2.Pose, _Mapping]] = ..., velocity: _Optional[_Union[_twist_pb2.Twist, _Mapping]] = ..., acceleration: _Optional[_Union[_accel_pb2.Accel, _Mapping]] = ...) -> None: ...
