from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SetImuCalibrationRequest(_message.Message):
    __slots__ = ("header", "gyro_bias_x", "gyro_bias_y", "gyro_bias_z")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    GYRO_BIAS_X_FIELD_NUMBER: _ClassVar[int]
    GYRO_BIAS_Y_FIELD_NUMBER: _ClassVar[int]
    GYRO_BIAS_Z_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    gyro_bias_x: float
    gyro_bias_y: float
    gyro_bias_z: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., gyro_bias_x: _Optional[float] = ..., gyro_bias_y: _Optional[float] = ..., gyro_bias_z: _Optional[float] = ...) -> None: ...

class SetImuCalibrationResponse(_message.Message):
    __slots__ = ("header", "success")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    success: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., success: bool = ...) -> None: ...
