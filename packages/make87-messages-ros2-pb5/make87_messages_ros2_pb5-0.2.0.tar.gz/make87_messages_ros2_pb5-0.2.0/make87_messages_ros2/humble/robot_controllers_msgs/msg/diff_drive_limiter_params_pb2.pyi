from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DiffDriveLimiterParams(_message.Message):
    __slots__ = ("header", "max_linear_velocity", "max_linear_acceleration", "max_angular_velocity", "max_angular_acceleration", "max_wheel_velocity", "track_width", "angular_velocity_limits_linear_velocity", "scale_to_wheel_velocity_limits")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    MAX_LINEAR_VELOCITY_FIELD_NUMBER: _ClassVar[int]
    MAX_LINEAR_ACCELERATION_FIELD_NUMBER: _ClassVar[int]
    MAX_ANGULAR_VELOCITY_FIELD_NUMBER: _ClassVar[int]
    MAX_ANGULAR_ACCELERATION_FIELD_NUMBER: _ClassVar[int]
    MAX_WHEEL_VELOCITY_FIELD_NUMBER: _ClassVar[int]
    TRACK_WIDTH_FIELD_NUMBER: _ClassVar[int]
    ANGULAR_VELOCITY_LIMITS_LINEAR_VELOCITY_FIELD_NUMBER: _ClassVar[int]
    SCALE_TO_WHEEL_VELOCITY_LIMITS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    max_linear_velocity: float
    max_linear_acceleration: float
    max_angular_velocity: float
    max_angular_acceleration: float
    max_wheel_velocity: float
    track_width: float
    angular_velocity_limits_linear_velocity: bool
    scale_to_wheel_velocity_limits: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., max_linear_velocity: _Optional[float] = ..., max_linear_acceleration: _Optional[float] = ..., max_angular_velocity: _Optional[float] = ..., max_angular_acceleration: _Optional[float] = ..., max_wheel_velocity: _Optional[float] = ..., track_width: _Optional[float] = ..., angular_velocity_limits_linear_velocity: bool = ..., scale_to_wheel_velocity_limits: bool = ...) -> None: ...
