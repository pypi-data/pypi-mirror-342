from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SbgMagStatus(_message.Message):
    __slots__ = ("header", "mag_x", "mag_y", "mag_z", "accel_x", "accel_y", "accel_z", "mags_in_range", "accels_in_range", "calibration")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    MAG_X_FIELD_NUMBER: _ClassVar[int]
    MAG_Y_FIELD_NUMBER: _ClassVar[int]
    MAG_Z_FIELD_NUMBER: _ClassVar[int]
    ACCEL_X_FIELD_NUMBER: _ClassVar[int]
    ACCEL_Y_FIELD_NUMBER: _ClassVar[int]
    ACCEL_Z_FIELD_NUMBER: _ClassVar[int]
    MAGS_IN_RANGE_FIELD_NUMBER: _ClassVar[int]
    ACCELS_IN_RANGE_FIELD_NUMBER: _ClassVar[int]
    CALIBRATION_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    mag_x: bool
    mag_y: bool
    mag_z: bool
    accel_x: bool
    accel_y: bool
    accel_z: bool
    mags_in_range: bool
    accels_in_range: bool
    calibration: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., mag_x: bool = ..., mag_y: bool = ..., mag_z: bool = ..., accel_x: bool = ..., accel_y: bool = ..., accel_z: bool = ..., mags_in_range: bool = ..., accels_in_range: bool = ..., calibration: bool = ...) -> None: ...
