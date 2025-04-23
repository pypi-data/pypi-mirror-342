from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.sbg_driver.msg import sbg_utc_time_status_pb2 as _sbg_utc_time_status_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SbgUtcTime(_message.Message):
    __slots__ = ("header", "ros2_header", "time_stamp", "clock_status", "year", "month", "day", "hour", "min", "sec", "nanosec", "gps_tow", "clk_bias_std", "clk_sf_error_std", "clk_residual_error")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    TIME_STAMP_FIELD_NUMBER: _ClassVar[int]
    CLOCK_STATUS_FIELD_NUMBER: _ClassVar[int]
    YEAR_FIELD_NUMBER: _ClassVar[int]
    MONTH_FIELD_NUMBER: _ClassVar[int]
    DAY_FIELD_NUMBER: _ClassVar[int]
    HOUR_FIELD_NUMBER: _ClassVar[int]
    MIN_FIELD_NUMBER: _ClassVar[int]
    SEC_FIELD_NUMBER: _ClassVar[int]
    NANOSEC_FIELD_NUMBER: _ClassVar[int]
    GPS_TOW_FIELD_NUMBER: _ClassVar[int]
    CLK_BIAS_STD_FIELD_NUMBER: _ClassVar[int]
    CLK_SF_ERROR_STD_FIELD_NUMBER: _ClassVar[int]
    CLK_RESIDUAL_ERROR_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    time_stamp: int
    clock_status: _sbg_utc_time_status_pb2.SbgUtcTimeStatus
    year: int
    month: int
    day: int
    hour: int
    min: int
    sec: int
    nanosec: int
    gps_tow: int
    clk_bias_std: float
    clk_sf_error_std: float
    clk_residual_error: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., time_stamp: _Optional[int] = ..., clock_status: _Optional[_Union[_sbg_utc_time_status_pb2.SbgUtcTimeStatus, _Mapping]] = ..., year: _Optional[int] = ..., month: _Optional[int] = ..., day: _Optional[int] = ..., hour: _Optional[int] = ..., min: _Optional[int] = ..., sec: _Optional[int] = ..., nanosec: _Optional[int] = ..., gps_tow: _Optional[int] = ..., clk_bias_std: _Optional[float] = ..., clk_sf_error_std: _Optional[float] = ..., clk_residual_error: _Optional[float] = ...) -> None: ...
