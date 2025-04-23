from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EnhancedPositionRpt(_message.Message):
    __slots__ = ("header", "shaft_extension", "motor_overload_error", "clutch_overload_error", "motor_open_load_error", "clutch_open_load_error", "position_reach_error", "hardware_warning_1_error", "hardware_warning_2_error", "motor_current")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SHAFT_EXTENSION_FIELD_NUMBER: _ClassVar[int]
    MOTOR_OVERLOAD_ERROR_FIELD_NUMBER: _ClassVar[int]
    CLUTCH_OVERLOAD_ERROR_FIELD_NUMBER: _ClassVar[int]
    MOTOR_OPEN_LOAD_ERROR_FIELD_NUMBER: _ClassVar[int]
    CLUTCH_OPEN_LOAD_ERROR_FIELD_NUMBER: _ClassVar[int]
    POSITION_REACH_ERROR_FIELD_NUMBER: _ClassVar[int]
    HARDWARE_WARNING_1_ERROR_FIELD_NUMBER: _ClassVar[int]
    HARDWARE_WARNING_2_ERROR_FIELD_NUMBER: _ClassVar[int]
    MOTOR_CURRENT_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    shaft_extension: float
    motor_overload_error: bool
    clutch_overload_error: bool
    motor_open_load_error: bool
    clutch_open_load_error: bool
    position_reach_error: bool
    hardware_warning_1_error: bool
    hardware_warning_2_error: bool
    motor_current: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., shaft_extension: _Optional[float] = ..., motor_overload_error: bool = ..., clutch_overload_error: bool = ..., motor_open_load_error: bool = ..., clutch_open_load_error: bool = ..., position_reach_error: bool = ..., hardware_warning_1_error: bool = ..., hardware_warning_2_error: bool = ..., motor_current: _Optional[int] = ...) -> None: ...
