from make87_messages_ros2.jazzy.vision_msgs.msg import point2_d_pb2 as _point2_d_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Pose2D(_message.Message):
    __slots__ = ("position", "theta")
    POSITION_FIELD_NUMBER: _ClassVar[int]
    THETA_FIELD_NUMBER: _ClassVar[int]
    position: _point2_d_pb2.Point2D
    theta: float
    def __init__(self, position: _Optional[_Union[_point2_d_pb2.Point2D, _Mapping]] = ..., theta: _Optional[float] = ...) -> None: ...
