from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ObstacleStatus(_message.Message):
    __slots__ = ("header", "ros2_header", "num_obstacles", "timestamp", "application_version", "active_version_number_section", "left_close_range_cut_in", "right_close_range_cut_in", "stop_go", "protocol_version", "close_car", "failsafe")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    NUM_OBSTACLES_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    APPLICATION_VERSION_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_VERSION_NUMBER_SECTION_FIELD_NUMBER: _ClassVar[int]
    LEFT_CLOSE_RANGE_CUT_IN_FIELD_NUMBER: _ClassVar[int]
    RIGHT_CLOSE_RANGE_CUT_IN_FIELD_NUMBER: _ClassVar[int]
    STOP_GO_FIELD_NUMBER: _ClassVar[int]
    PROTOCOL_VERSION_FIELD_NUMBER: _ClassVar[int]
    CLOSE_CAR_FIELD_NUMBER: _ClassVar[int]
    FAILSAFE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    num_obstacles: int
    timestamp: int
    application_version: int
    active_version_number_section: int
    left_close_range_cut_in: bool
    right_close_range_cut_in: bool
    stop_go: int
    protocol_version: int
    close_car: bool
    failsafe: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., num_obstacles: _Optional[int] = ..., timestamp: _Optional[int] = ..., application_version: _Optional[int] = ..., active_version_number_section: _Optional[int] = ..., left_close_range_cut_in: bool = ..., right_close_range_cut_in: bool = ..., stop_go: _Optional[int] = ..., protocol_version: _Optional[int] = ..., close_car: bool = ..., failsafe: _Optional[int] = ...) -> None: ...
