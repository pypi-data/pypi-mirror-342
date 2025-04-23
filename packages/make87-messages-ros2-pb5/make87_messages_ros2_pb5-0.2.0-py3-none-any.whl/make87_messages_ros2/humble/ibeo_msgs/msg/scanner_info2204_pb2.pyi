from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ScannerInfo2204(_message.Message):
    __slots__ = ("header", "device_id", "scanner_type", "scan_number", "start_angle", "end_angle", "yaw_angle", "pitch_angle", "roll_angle", "offset_x", "offset_y", "offset_z")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    DEVICE_ID_FIELD_NUMBER: _ClassVar[int]
    SCANNER_TYPE_FIELD_NUMBER: _ClassVar[int]
    SCAN_NUMBER_FIELD_NUMBER: _ClassVar[int]
    START_ANGLE_FIELD_NUMBER: _ClassVar[int]
    END_ANGLE_FIELD_NUMBER: _ClassVar[int]
    YAW_ANGLE_FIELD_NUMBER: _ClassVar[int]
    PITCH_ANGLE_FIELD_NUMBER: _ClassVar[int]
    ROLL_ANGLE_FIELD_NUMBER: _ClassVar[int]
    OFFSET_X_FIELD_NUMBER: _ClassVar[int]
    OFFSET_Y_FIELD_NUMBER: _ClassVar[int]
    OFFSET_Z_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    device_id: int
    scanner_type: int
    scan_number: int
    start_angle: float
    end_angle: float
    yaw_angle: float
    pitch_angle: float
    roll_angle: float
    offset_x: float
    offset_y: float
    offset_z: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., device_id: _Optional[int] = ..., scanner_type: _Optional[int] = ..., scan_number: _Optional[int] = ..., start_angle: _Optional[float] = ..., end_angle: _Optional[float] = ..., yaw_angle: _Optional[float] = ..., pitch_angle: _Optional[float] = ..., roll_angle: _Optional[float] = ..., offset_x: _Optional[float] = ..., offset_y: _Optional[float] = ..., offset_z: _Optional[float] = ...) -> None: ...
