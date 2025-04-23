from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.automotive_platform_msgs.msg import gear_pb2 as _gear_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GearFeedback(_message.Message):
    __slots__ = ("header", "ros2_header", "current_gear")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    CURRENT_GEAR_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    current_gear: _gear_pb2.Gear
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., current_gear: _Optional[_Union[_gear_pb2.Gear, _Mapping]] = ...) -> None: ...
