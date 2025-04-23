from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.builtin_interfaces.msg import time_pb2 as _time_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetMeasurementsRequest(_message.Message):
    __slots__ = ("header", "max_repeats", "get_position", "get_current", "get_velocity")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    MAX_REPEATS_FIELD_NUMBER: _ClassVar[int]
    GET_POSITION_FIELD_NUMBER: _ClassVar[int]
    GET_CURRENT_FIELD_NUMBER: _ClassVar[int]
    GET_VELOCITY_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    max_repeats: int
    get_position: bool
    get_current: bool
    get_velocity: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., max_repeats: _Optional[int] = ..., get_position: bool = ..., get_current: bool = ..., get_velocity: bool = ...) -> None: ...

class GetMeasurementsResponse(_message.Message):
    __slots__ = ("header", "success", "position", "current", "velocity", "stamp")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    CURRENT_FIELD_NUMBER: _ClassVar[int]
    VELOCITY_FIELD_NUMBER: _ClassVar[int]
    STAMP_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    success: bool
    position: int
    current: int
    velocity: int
    stamp: _time_pb2.Time
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., success: bool = ..., position: _Optional[int] = ..., current: _Optional[int] = ..., velocity: _Optional[int] = ..., stamp: _Optional[_Union[_time_pb2.Time, _Mapping]] = ...) -> None: ...
