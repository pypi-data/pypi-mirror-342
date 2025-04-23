from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class StopStatus(_message.Message):
    __slots__ = ("header", "ros2_header", "stop_power_status", "external_stop_present", "needs_reset")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    STOP_POWER_STATUS_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_STOP_PRESENT_FIELD_NUMBER: _ClassVar[int]
    NEEDS_RESET_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    stop_power_status: bool
    external_stop_present: bool
    needs_reset: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., stop_power_status: bool = ..., external_stop_present: bool = ..., needs_reset: bool = ...) -> None: ...
