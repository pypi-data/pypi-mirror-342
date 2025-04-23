from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GPSDetails(_message.Message):
    __slots__ = ("header", "ros2_header", "horizontal_dop", "position_dop", "fix_state", "vertical_accuracy", "horizontal_accuracy", "speed_accuracy", "num_gps_satellites_used", "num_glonass_satellites_used", "num_total_satellites_used", "gps_counter")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    HORIZONTAL_DOP_FIELD_NUMBER: _ClassVar[int]
    POSITION_DOP_FIELD_NUMBER: _ClassVar[int]
    FIX_STATE_FIELD_NUMBER: _ClassVar[int]
    VERTICAL_ACCURACY_FIELD_NUMBER: _ClassVar[int]
    HORIZONTAL_ACCURACY_FIELD_NUMBER: _ClassVar[int]
    SPEED_ACCURACY_FIELD_NUMBER: _ClassVar[int]
    NUM_GPS_SATELLITES_USED_FIELD_NUMBER: _ClassVar[int]
    NUM_GLONASS_SATELLITES_USED_FIELD_NUMBER: _ClassVar[int]
    NUM_TOTAL_SATELLITES_USED_FIELD_NUMBER: _ClassVar[int]
    GPS_COUNTER_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    horizontal_dop: float
    position_dop: float
    fix_state: float
    vertical_accuracy: float
    horizontal_accuracy: float
    speed_accuracy: float
    num_gps_satellites_used: int
    num_glonass_satellites_used: int
    num_total_satellites_used: int
    gps_counter: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., horizontal_dop: _Optional[float] = ..., position_dop: _Optional[float] = ..., fix_state: _Optional[float] = ..., vertical_accuracy: _Optional[float] = ..., horizontal_accuracy: _Optional[float] = ..., speed_accuracy: _Optional[float] = ..., num_gps_satellites_used: _Optional[int] = ..., num_glonass_satellites_used: _Optional[int] = ..., num_total_satellites_used: _Optional[int] = ..., gps_counter: _Optional[int] = ...) -> None: ...
