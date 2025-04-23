from make87_messages_ros2.rolling.builtin_interfaces.msg import time_pb2 as _time_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Imu(_message.Message):
    __slots__ = ("stamp", "temperature", "gyro_x", "gyro_y", "gyro_z", "accel_x", "accel_y", "accel_z")
    STAMP_FIELD_NUMBER: _ClassVar[int]
    TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    GYRO_X_FIELD_NUMBER: _ClassVar[int]
    GYRO_Y_FIELD_NUMBER: _ClassVar[int]
    GYRO_Z_FIELD_NUMBER: _ClassVar[int]
    ACCEL_X_FIELD_NUMBER: _ClassVar[int]
    ACCEL_Y_FIELD_NUMBER: _ClassVar[int]
    ACCEL_Z_FIELD_NUMBER: _ClassVar[int]
    stamp: _time_pb2.Time
    temperature: float
    gyro_x: float
    gyro_y: float
    gyro_z: float
    accel_x: float
    accel_y: float
    accel_z: float
    def __init__(self, stamp: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., temperature: _Optional[float] = ..., gyro_x: _Optional[float] = ..., gyro_y: _Optional[float] = ..., gyro_z: _Optional[float] = ..., accel_x: _Optional[float] = ..., accel_y: _Optional[float] = ..., accel_z: _Optional[float] = ...) -> None: ...
