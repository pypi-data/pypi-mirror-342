from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SbgGpsHdt(_message.Message):
    __slots__ = ("header", "ros2_header", "time_stamp", "status", "tow", "true_heading", "true_heading_acc", "pitch", "pitch_acc", "baseline", "num_sv_tracked", "num_sv_used")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    TIME_STAMP_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    TOW_FIELD_NUMBER: _ClassVar[int]
    TRUE_HEADING_FIELD_NUMBER: _ClassVar[int]
    TRUE_HEADING_ACC_FIELD_NUMBER: _ClassVar[int]
    PITCH_FIELD_NUMBER: _ClassVar[int]
    PITCH_ACC_FIELD_NUMBER: _ClassVar[int]
    BASELINE_FIELD_NUMBER: _ClassVar[int]
    NUM_SV_TRACKED_FIELD_NUMBER: _ClassVar[int]
    NUM_SV_USED_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    time_stamp: int
    status: int
    tow: int
    true_heading: float
    true_heading_acc: float
    pitch: float
    pitch_acc: float
    baseline: float
    num_sv_tracked: int
    num_sv_used: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., time_stamp: _Optional[int] = ..., status: _Optional[int] = ..., tow: _Optional[int] = ..., true_heading: _Optional[float] = ..., true_heading_acc: _Optional[float] = ..., pitch: _Optional[float] = ..., pitch_acc: _Optional[float] = ..., baseline: _Optional[float] = ..., num_sv_tracked: _Optional[int] = ..., num_sv_used: _Optional[int] = ...) -> None: ...
