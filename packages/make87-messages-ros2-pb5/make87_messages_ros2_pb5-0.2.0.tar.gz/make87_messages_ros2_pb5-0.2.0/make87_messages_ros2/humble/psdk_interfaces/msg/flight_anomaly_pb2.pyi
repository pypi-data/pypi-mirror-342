from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class FlightAnomaly(_message.Message):
    __slots__ = ("header", "ros2_header", "impact_in_air", "random_fly", "height_ctrl_fail", "roll_pitch_ctrl_fail", "yaw_ctrl_fail", "aircraft_is_falling", "strong_wind_level1", "strong_wind_level2", "compass_installation_error", "imu_installation_error", "esc_temperature_high", "at_least_one_esc_disconnected", "gps_yaw_error", "reserved")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    IMPACT_IN_AIR_FIELD_NUMBER: _ClassVar[int]
    RANDOM_FLY_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_CTRL_FAIL_FIELD_NUMBER: _ClassVar[int]
    ROLL_PITCH_CTRL_FAIL_FIELD_NUMBER: _ClassVar[int]
    YAW_CTRL_FAIL_FIELD_NUMBER: _ClassVar[int]
    AIRCRAFT_IS_FALLING_FIELD_NUMBER: _ClassVar[int]
    STRONG_WIND_LEVEL1_FIELD_NUMBER: _ClassVar[int]
    STRONG_WIND_LEVEL2_FIELD_NUMBER: _ClassVar[int]
    COMPASS_INSTALLATION_ERROR_FIELD_NUMBER: _ClassVar[int]
    IMU_INSTALLATION_ERROR_FIELD_NUMBER: _ClassVar[int]
    ESC_TEMPERATURE_HIGH_FIELD_NUMBER: _ClassVar[int]
    AT_LEAST_ONE_ESC_DISCONNECTED_FIELD_NUMBER: _ClassVar[int]
    GPS_YAW_ERROR_FIELD_NUMBER: _ClassVar[int]
    RESERVED_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    impact_in_air: int
    random_fly: int
    height_ctrl_fail: int
    roll_pitch_ctrl_fail: int
    yaw_ctrl_fail: int
    aircraft_is_falling: int
    strong_wind_level1: int
    strong_wind_level2: int
    compass_installation_error: int
    imu_installation_error: int
    esc_temperature_high: int
    at_least_one_esc_disconnected: int
    gps_yaw_error: int
    reserved: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., impact_in_air: _Optional[int] = ..., random_fly: _Optional[int] = ..., height_ctrl_fail: _Optional[int] = ..., roll_pitch_ctrl_fail: _Optional[int] = ..., yaw_ctrl_fail: _Optional[int] = ..., aircraft_is_falling: _Optional[int] = ..., strong_wind_level1: _Optional[int] = ..., strong_wind_level2: _Optional[int] = ..., compass_installation_error: _Optional[int] = ..., imu_installation_error: _Optional[int] = ..., esc_temperature_high: _Optional[int] = ..., at_least_one_esc_disconnected: _Optional[int] = ..., gps_yaw_error: _Optional[int] = ..., reserved: _Optional[int] = ...) -> None: ...
