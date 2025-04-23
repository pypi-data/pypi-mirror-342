from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PrimaryControl(_message.Message):
    __slots__ = ("header", "ros2_header", "active", "estop", "steering_command", "throttle_command", "brake_command")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_FIELD_NUMBER: _ClassVar[int]
    ESTOP_FIELD_NUMBER: _ClassVar[int]
    STEERING_COMMAND_FIELD_NUMBER: _ClassVar[int]
    THROTTLE_COMMAND_FIELD_NUMBER: _ClassVar[int]
    BRAKE_COMMAND_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    active: bool
    estop: bool
    steering_command: float
    throttle_command: float
    brake_command: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., active: bool = ..., estop: bool = ..., steering_command: _Optional[float] = ..., throttle_command: _Optional[float] = ..., brake_command: _Optional[float] = ...) -> None: ...
