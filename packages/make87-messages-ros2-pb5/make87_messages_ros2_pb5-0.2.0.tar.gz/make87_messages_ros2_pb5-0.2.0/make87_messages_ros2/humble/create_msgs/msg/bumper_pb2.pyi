from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Bumper(_message.Message):
    __slots__ = ("header", "ros2_header", "is_left_pressed", "is_right_pressed", "is_light_left", "is_light_front_left", "is_light_center_left", "is_light_center_right", "is_light_front_right", "is_light_right", "light_signal_left", "light_signal_front_left", "light_signal_center_left", "light_signal_center_right", "light_signal_front_right", "light_signal_right")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    IS_LEFT_PRESSED_FIELD_NUMBER: _ClassVar[int]
    IS_RIGHT_PRESSED_FIELD_NUMBER: _ClassVar[int]
    IS_LIGHT_LEFT_FIELD_NUMBER: _ClassVar[int]
    IS_LIGHT_FRONT_LEFT_FIELD_NUMBER: _ClassVar[int]
    IS_LIGHT_CENTER_LEFT_FIELD_NUMBER: _ClassVar[int]
    IS_LIGHT_CENTER_RIGHT_FIELD_NUMBER: _ClassVar[int]
    IS_LIGHT_FRONT_RIGHT_FIELD_NUMBER: _ClassVar[int]
    IS_LIGHT_RIGHT_FIELD_NUMBER: _ClassVar[int]
    LIGHT_SIGNAL_LEFT_FIELD_NUMBER: _ClassVar[int]
    LIGHT_SIGNAL_FRONT_LEFT_FIELD_NUMBER: _ClassVar[int]
    LIGHT_SIGNAL_CENTER_LEFT_FIELD_NUMBER: _ClassVar[int]
    LIGHT_SIGNAL_CENTER_RIGHT_FIELD_NUMBER: _ClassVar[int]
    LIGHT_SIGNAL_FRONT_RIGHT_FIELD_NUMBER: _ClassVar[int]
    LIGHT_SIGNAL_RIGHT_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    is_left_pressed: bool
    is_right_pressed: bool
    is_light_left: bool
    is_light_front_left: bool
    is_light_center_left: bool
    is_light_center_right: bool
    is_light_front_right: bool
    is_light_right: bool
    light_signal_left: int
    light_signal_front_left: int
    light_signal_center_left: int
    light_signal_center_right: int
    light_signal_front_right: int
    light_signal_right: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., is_left_pressed: bool = ..., is_right_pressed: bool = ..., is_light_left: bool = ..., is_light_front_left: bool = ..., is_light_center_left: bool = ..., is_light_center_right: bool = ..., is_light_front_right: bool = ..., is_light_right: bool = ..., light_signal_left: _Optional[int] = ..., light_signal_front_left: _Optional[int] = ..., light_signal_center_left: _Optional[int] = ..., light_signal_center_right: _Optional[int] = ..., light_signal_front_right: _Optional[int] = ..., light_signal_right: _Optional[int] = ...) -> None: ...
