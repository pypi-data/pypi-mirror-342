from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class VehicleControlData(_message.Message):
    __slots__ = ("header", "ros2_header", "acceleration_pct", "braking_pct", "target_wheel_angle", "target_wheel_angular_rate", "target_gear")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    ACCELERATION_PCT_FIELD_NUMBER: _ClassVar[int]
    BRAKING_PCT_FIELD_NUMBER: _ClassVar[int]
    TARGET_WHEEL_ANGLE_FIELD_NUMBER: _ClassVar[int]
    TARGET_WHEEL_ANGULAR_RATE_FIELD_NUMBER: _ClassVar[int]
    TARGET_GEAR_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    acceleration_pct: float
    braking_pct: float
    target_wheel_angle: float
    target_wheel_angular_rate: float
    target_gear: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., acceleration_pct: _Optional[float] = ..., braking_pct: _Optional[float] = ..., target_wheel_angle: _Optional[float] = ..., target_wheel_angular_rate: _Optional[float] = ..., target_gear: _Optional[int] = ...) -> None: ...
