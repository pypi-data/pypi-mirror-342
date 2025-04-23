from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Status(_message.Message):
    __slots__ = ("header", "operating_mode", "area_number", "error_status", "error_code", "lockout_status", "ossd_1", "ossd_2", "warning_1", "warning_2", "ossd_3", "ossd_4", "distance", "angle")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    OPERATING_MODE_FIELD_NUMBER: _ClassVar[int]
    AREA_NUMBER_FIELD_NUMBER: _ClassVar[int]
    ERROR_STATUS_FIELD_NUMBER: _ClassVar[int]
    ERROR_CODE_FIELD_NUMBER: _ClassVar[int]
    LOCKOUT_STATUS_FIELD_NUMBER: _ClassVar[int]
    OSSD_1_FIELD_NUMBER: _ClassVar[int]
    OSSD_2_FIELD_NUMBER: _ClassVar[int]
    WARNING_1_FIELD_NUMBER: _ClassVar[int]
    WARNING_2_FIELD_NUMBER: _ClassVar[int]
    OSSD_3_FIELD_NUMBER: _ClassVar[int]
    OSSD_4_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_FIELD_NUMBER: _ClassVar[int]
    ANGLE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    operating_mode: int
    area_number: int
    error_status: bool
    error_code: int
    lockout_status: bool
    ossd_1: bool
    ossd_2: bool
    warning_1: bool
    warning_2: bool
    ossd_3: bool
    ossd_4: bool
    distance: int
    angle: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., operating_mode: _Optional[int] = ..., area_number: _Optional[int] = ..., error_status: bool = ..., error_code: _Optional[int] = ..., lockout_status: bool = ..., ossd_1: bool = ..., ossd_2: bool = ..., warning_1: bool = ..., warning_2: bool = ..., ossd_3: bool = ..., ossd_4: bool = ..., distance: _Optional[int] = ..., angle: _Optional[float] = ...) -> None: ...
