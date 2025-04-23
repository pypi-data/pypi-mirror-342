from make87_messages_ros2.jazzy.geometry_msgs.msg import accel_pb2 as _accel_pb2
from make87_messages_ros2.jazzy.geometry_msgs.msg import pose_pb2 as _pose_pb2
from make87_messages_ros2.jazzy.geometry_msgs.msg import twist_pb2 as _twist_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CartesianPoint(_message.Message):
    __slots__ = ("pose", "velocity", "acceleration")
    POSE_FIELD_NUMBER: _ClassVar[int]
    VELOCITY_FIELD_NUMBER: _ClassVar[int]
    ACCELERATION_FIELD_NUMBER: _ClassVar[int]
    pose: _pose_pb2.Pose
    velocity: _twist_pb2.Twist
    acceleration: _accel_pb2.Accel
    def __init__(self, pose: _Optional[_Union[_pose_pb2.Pose, _Mapping]] = ..., velocity: _Optional[_Union[_twist_pb2.Twist, _Mapping]] = ..., acceleration: _Optional[_Union[_accel_pb2.Accel, _Mapping]] = ...) -> None: ...
