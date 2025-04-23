from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LIDoutputstateMsg(_message.Message):
    __slots__ = ("header", "version_number", "system_counter", "output_state", "output_count", "time_state", "year", "month", "day", "hour", "minute", "second", "microsecond")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    VERSION_NUMBER_FIELD_NUMBER: _ClassVar[int]
    SYSTEM_COUNTER_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_STATE_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_COUNT_FIELD_NUMBER: _ClassVar[int]
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
    system_counter: int
    output_state: _containers.RepeatedScalarFieldContainer[int]
    output_count: _containers.RepeatedScalarFieldContainer[int]
    time_state: int
    year: int
    month: int
    day: int
    hour: int
    minute: int
    second: int
    microsecond: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., version_number: _Optional[int] = ..., system_counter: _Optional[int] = ..., output_state: _Optional[_Iterable[int]] = ..., output_count: _Optional[_Iterable[int]] = ..., time_state: _Optional[int] = ..., year: _Optional[int] = ..., month: _Optional[int] = ..., day: _Optional[int] = ..., hour: _Optional[int] = ..., minute: _Optional[int] = ..., second: _Optional[int] = ..., microsecond: _Optional[int] = ...) -> None: ...
