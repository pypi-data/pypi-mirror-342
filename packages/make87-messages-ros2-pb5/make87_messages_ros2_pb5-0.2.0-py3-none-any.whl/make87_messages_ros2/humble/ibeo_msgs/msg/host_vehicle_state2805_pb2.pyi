from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.builtin_interfaces.msg import time_pb2 as _time_pb2
from make87_messages_ros2.humble.ibeo_msgs.msg import ibeo_data_header_pb2 as _ibeo_data_header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class HostVehicleState2805(_message.Message):
    __slots__ = ("header", "ros2_header", "ibeo_header", "timestamp", "scan_number", "error_flags", "longitudinal_velocity", "steering_wheel_angle", "front_wheel_angle", "x_position", "y_position", "course_angle", "time_difference", "x_difference", "y_difference", "heading_difference", "current_yaw_rate")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    IBEO_HEADER_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    SCAN_NUMBER_FIELD_NUMBER: _ClassVar[int]
    ERROR_FLAGS_FIELD_NUMBER: _ClassVar[int]
    LONGITUDINAL_VELOCITY_FIELD_NUMBER: _ClassVar[int]
    STEERING_WHEEL_ANGLE_FIELD_NUMBER: _ClassVar[int]
    FRONT_WHEEL_ANGLE_FIELD_NUMBER: _ClassVar[int]
    X_POSITION_FIELD_NUMBER: _ClassVar[int]
    Y_POSITION_FIELD_NUMBER: _ClassVar[int]
    COURSE_ANGLE_FIELD_NUMBER: _ClassVar[int]
    TIME_DIFFERENCE_FIELD_NUMBER: _ClassVar[int]
    X_DIFFERENCE_FIELD_NUMBER: _ClassVar[int]
    Y_DIFFERENCE_FIELD_NUMBER: _ClassVar[int]
    HEADING_DIFFERENCE_FIELD_NUMBER: _ClassVar[int]
    CURRENT_YAW_RATE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    ibeo_header: _ibeo_data_header_pb2.IbeoDataHeader
    timestamp: _time_pb2.Time
    scan_number: int
    error_flags: int
    longitudinal_velocity: float
    steering_wheel_angle: float
    front_wheel_angle: float
    x_position: int
    y_position: int
    course_angle: int
    time_difference: int
    x_difference: int
    y_difference: int
    heading_difference: int
    current_yaw_rate: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., ibeo_header: _Optional[_Union[_ibeo_data_header_pb2.IbeoDataHeader, _Mapping]] = ..., timestamp: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., scan_number: _Optional[int] = ..., error_flags: _Optional[int] = ..., longitudinal_velocity: _Optional[float] = ..., steering_wheel_angle: _Optional[float] = ..., front_wheel_angle: _Optional[float] = ..., x_position: _Optional[int] = ..., y_position: _Optional[int] = ..., course_angle: _Optional[int] = ..., time_difference: _Optional[int] = ..., x_difference: _Optional[int] = ..., y_difference: _Optional[int] = ..., heading_difference: _Optional[int] = ..., current_yaw_rate: _Optional[int] = ...) -> None: ...
