from make87_messages_ros2.rolling.builtin_interfaces.msg import time_pb2 as _time_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class StartTimeRange(_message.Message):
    __slots__ = ("earliest_start_time", "has_earliest_start_time", "latest_start_time", "has_latest_start_time")
    EARLIEST_START_TIME_FIELD_NUMBER: _ClassVar[int]
    HAS_EARLIEST_START_TIME_FIELD_NUMBER: _ClassVar[int]
    LATEST_START_TIME_FIELD_NUMBER: _ClassVar[int]
    HAS_LATEST_START_TIME_FIELD_NUMBER: _ClassVar[int]
    earliest_start_time: _time_pb2.Time
    has_earliest_start_time: bool
    latest_start_time: _time_pb2.Time
    has_latest_start_time: bool
    def __init__(self, earliest_start_time: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., has_earliest_start_time: bool = ..., latest_start_time: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., has_latest_start_time: bool = ...) -> None: ...
