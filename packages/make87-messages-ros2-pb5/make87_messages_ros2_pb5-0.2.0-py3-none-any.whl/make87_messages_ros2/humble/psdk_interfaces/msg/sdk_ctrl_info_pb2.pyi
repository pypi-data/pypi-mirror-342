from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SDKCtrlInfo(_message.Message):
    __slots__ = ("header", "ros2_header", "control_mode", "device_status", "flight_status", "vrc_status", "reserved")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    CONTROL_MODE_FIELD_NUMBER: _ClassVar[int]
    DEVICE_STATUS_FIELD_NUMBER: _ClassVar[int]
    FLIGHT_STATUS_FIELD_NUMBER: _ClassVar[int]
    VRC_STATUS_FIELD_NUMBER: _ClassVar[int]
    RESERVED_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    control_mode: int
    device_status: int
    flight_status: int
    vrc_status: int
    reserved: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., control_mode: _Optional[int] = ..., device_status: _Optional[int] = ..., flight_status: _Optional[int] = ..., vrc_status: _Optional[int] = ..., reserved: _Optional[int] = ...) -> None: ...
