from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SpeedMode(_message.Message):
    __slots__ = ("header", "ros2_header", "mode", "speed", "acceleration_limit", "deceleration_limit")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    SPEED_FIELD_NUMBER: _ClassVar[int]
    ACCELERATION_LIMIT_FIELD_NUMBER: _ClassVar[int]
    DECELERATION_LIMIT_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    mode: int
    speed: float
    acceleration_limit: float
    deceleration_limit: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., mode: _Optional[int] = ..., speed: _Optional[float] = ..., acceleration_limit: _Optional[float] = ..., deceleration_limit: _Optional[float] = ...) -> None: ...
