from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LFErecFieldMsg(_message.Message):
    __slots__ = ("header", "version_number", "field_index", "sys_count", "dist_scale_factor", "dist_scale_offset", "angle_scale_factor", "angle_scale_offset", "field_result_mrs", "time_state", "year", "month", "day", "hour", "minute", "second", "microsecond")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    VERSION_NUMBER_FIELD_NUMBER: _ClassVar[int]
    FIELD_INDEX_FIELD_NUMBER: _ClassVar[int]
    SYS_COUNT_FIELD_NUMBER: _ClassVar[int]
    DIST_SCALE_FACTOR_FIELD_NUMBER: _ClassVar[int]
    DIST_SCALE_OFFSET_FIELD_NUMBER: _ClassVar[int]
    ANGLE_SCALE_FACTOR_FIELD_NUMBER: _ClassVar[int]
    ANGLE_SCALE_OFFSET_FIELD_NUMBER: _ClassVar[int]
    FIELD_RESULT_MRS_FIELD_NUMBER: _ClassVar[int]
    TIME_STATE_FIELD_NUMBER: _ClassVar[int]
    YEAR_FIELD_NUMBER: _ClassVar[int]
    MONTH_FIELD_NUMBER: _ClassVar[int]
    DAY_FIELD_NUMBER: _ClassVar[int]
    HOUR_FIELD_NUMBER: _ClassVar[int]
    MINUTE_FIELD_NUMBER: _ClassVar[int]
    SECOND_FIELD_NUMBER: _ClassVar[int]
    MICROSECOND_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    version_number: int
    field_index: int
    sys_count: int
    dist_scale_factor: float
    dist_scale_offset: float
    angle_scale_factor: int
    angle_scale_offset: int
    field_result_mrs: int
    time_state: int
    year: int
    month: int
    day: int
    hour: int
    minute: int
    second: int
    microsecond: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., version_number: _Optional[int] = ..., field_index: _Optional[int] = ..., sys_count: _Optional[int] = ..., dist_scale_factor: _Optional[float] = ..., dist_scale_offset: _Optional[float] = ..., angle_scale_factor: _Optional[int] = ..., angle_scale_offset: _Optional[int] = ..., field_result_mrs: _Optional[int] = ..., time_state: _Optional[int] = ..., year: _Optional[int] = ..., month: _Optional[int] = ..., day: _Optional[int] = ..., hour: _Optional[int] = ..., minute: _Optional[int] = ..., second: _Optional[int] = ..., microsecond: _Optional[int] = ...) -> None: ...
