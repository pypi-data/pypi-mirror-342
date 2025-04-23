from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class UlcCmd(_message.Message):
    __slots__ = ("header", "cmd", "limit_accel", "limit_decel", "limit_jerk_throttle", "limit_jerk_brake", "cmd_type", "enable", "clear", "enable_shift", "enable_shift_park", "coast_decel")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    CMD_FIELD_NUMBER: _ClassVar[int]
    LIMIT_ACCEL_FIELD_NUMBER: _ClassVar[int]
    LIMIT_DECEL_FIELD_NUMBER: _ClassVar[int]
    LIMIT_JERK_THROTTLE_FIELD_NUMBER: _ClassVar[int]
    LIMIT_JERK_BRAKE_FIELD_NUMBER: _ClassVar[int]
    CMD_TYPE_FIELD_NUMBER: _ClassVar[int]
    ENABLE_FIELD_NUMBER: _ClassVar[int]
    CLEAR_FIELD_NUMBER: _ClassVar[int]
    ENABLE_SHIFT_FIELD_NUMBER: _ClassVar[int]
    ENABLE_SHIFT_PARK_FIELD_NUMBER: _ClassVar[int]
    COAST_DECEL_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    cmd: float
    limit_accel: float
    limit_decel: float
    limit_jerk_throttle: float
    limit_jerk_brake: float
    cmd_type: int
    enable: bool
    clear: bool
    enable_shift: bool
    enable_shift_park: bool
    coast_decel: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., cmd: _Optional[float] = ..., limit_accel: _Optional[float] = ..., limit_decel: _Optional[float] = ..., limit_jerk_throttle: _Optional[float] = ..., limit_jerk_brake: _Optional[float] = ..., cmd_type: _Optional[int] = ..., enable: bool = ..., clear: bool = ..., enable_shift: bool = ..., enable_shift_park: bool = ..., coast_decel: bool = ...) -> None: ...
