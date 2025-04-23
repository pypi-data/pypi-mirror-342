from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.builtin_interfaces.msg import duration_pb2 as _duration_pb2
from make87_messages_ros2.humble.builtin_interfaces.msg import time_pb2 as _time_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ClientLocalizationPose(_message.Message):
    __slots__ = ("header", "age", "timestamp", "unique_id", "state", "epoch", "error_flags", "info_flags")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    AGE_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    UNIQUE_ID_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    EPOCH_FIELD_NUMBER: _ClassVar[int]
    ERROR_FLAGS_FIELD_NUMBER: _ClassVar[int]
    INFO_FLAGS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    age: _duration_pb2.Duration
    timestamp: _time_pb2.Time
    unique_id: int
    state: int
    epoch: int
    error_flags: int
    info_flags: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., age: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ..., timestamp: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., unique_id: _Optional[int] = ..., state: _Optional[int] = ..., epoch: _Optional[int] = ..., error_flags: _Optional[int] = ..., info_flags: _Optional[int] = ...) -> None: ...
