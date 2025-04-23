from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class UBXNavOdo(_message.Message):
    __slots__ = ("header", "ros2_header", "version", "itow", "distance", "total_distance", "distance_std")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    ITOW_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_FIELD_NUMBER: _ClassVar[int]
    TOTAL_DISTANCE_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_STD_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    version: int
    itow: int
    distance: int
    total_distance: int
    distance_std: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., version: _Optional[int] = ..., itow: _Optional[int] = ..., distance: _Optional[int] = ..., total_distance: _Optional[int] = ..., distance_std: _Optional[int] = ...) -> None: ...
