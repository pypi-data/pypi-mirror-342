from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.ds_dbw_msgs.msg import quality_pb2 as _quality_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BrakeInfo(_message.Message):
    __slots__ = ("header", "ros2_header", "brake_torque_pedal", "brake_torque_request", "brake_torque_actual", "brake_pedal_qf", "brake_vacuum", "abs_active", "abs_enabled", "esc_active", "esc_enabled", "trac_active", "trac_enabled")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    BRAKE_TORQUE_PEDAL_FIELD_NUMBER: _ClassVar[int]
    BRAKE_TORQUE_REQUEST_FIELD_NUMBER: _ClassVar[int]
    BRAKE_TORQUE_ACTUAL_FIELD_NUMBER: _ClassVar[int]
    BRAKE_PEDAL_QF_FIELD_NUMBER: _ClassVar[int]
    BRAKE_VACUUM_FIELD_NUMBER: _ClassVar[int]
    ABS_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    ABS_ENABLED_FIELD_NUMBER: _ClassVar[int]
    ESC_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    ESC_ENABLED_FIELD_NUMBER: _ClassVar[int]
    TRAC_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    TRAC_ENABLED_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    brake_torque_pedal: float
    brake_torque_request: float
    brake_torque_actual: float
    brake_pedal_qf: _quality_pb2.Quality
    brake_vacuum: float
    abs_active: bool
    abs_enabled: bool
    esc_active: bool
    esc_enabled: bool
    trac_active: bool
    trac_enabled: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., brake_torque_pedal: _Optional[float] = ..., brake_torque_request: _Optional[float] = ..., brake_torque_actual: _Optional[float] = ..., brake_pedal_qf: _Optional[_Union[_quality_pb2.Quality, _Mapping]] = ..., brake_vacuum: _Optional[float] = ..., abs_active: bool = ..., abs_enabled: bool = ..., esc_active: bool = ..., esc_enabled: bool = ..., trac_active: bool = ..., trac_enabled: bool = ...) -> None: ...
