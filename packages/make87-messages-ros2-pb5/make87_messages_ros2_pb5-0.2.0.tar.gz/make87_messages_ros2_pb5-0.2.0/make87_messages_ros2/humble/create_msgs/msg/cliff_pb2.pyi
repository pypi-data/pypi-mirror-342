from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Cliff(_message.Message):
    __slots__ = ("header", "ros2_header", "is_cliff_left", "is_cliff_front_left", "is_cliff_right", "is_cliff_front_right")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    IS_CLIFF_LEFT_FIELD_NUMBER: _ClassVar[int]
    IS_CLIFF_FRONT_LEFT_FIELD_NUMBER: _ClassVar[int]
    IS_CLIFF_RIGHT_FIELD_NUMBER: _ClassVar[int]
    IS_CLIFF_FRONT_RIGHT_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    is_cliff_left: bool
    is_cliff_front_left: bool
    is_cliff_right: bool
    is_cliff_front_right: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., is_cliff_left: bool = ..., is_cliff_front_left: bool = ..., is_cliff_right: bool = ..., is_cliff_front_right: bool = ...) -> None: ...
