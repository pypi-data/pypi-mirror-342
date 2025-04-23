from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.ackermann_msgs.msg import ackermann_drive_pb2 as _ackermann_drive_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AckermannDriveStamped(_message.Message):
    __slots__ = ("header", "ros2_header", "drive")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    DRIVE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    drive: _ackermann_drive_pb2.AckermannDrive
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., drive: _Optional[_Union[_ackermann_drive_pb2.AckermannDrive, _Mapping]] = ...) -> None: ...
