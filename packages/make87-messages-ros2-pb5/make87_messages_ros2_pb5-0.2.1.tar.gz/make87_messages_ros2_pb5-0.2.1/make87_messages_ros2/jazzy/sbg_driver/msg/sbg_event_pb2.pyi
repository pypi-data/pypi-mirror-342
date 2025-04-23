from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SbgEvent(_message.Message):
    __slots__ = ("header", "time_stamp", "overflow", "offset_0_valid", "offset_1_valid", "offset_2_valid", "offset_3_valid", "time_offset_0", "time_offset_1", "time_offset_2", "time_offset_3")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TIME_STAMP_FIELD_NUMBER: _ClassVar[int]
    OVERFLOW_FIELD_NUMBER: _ClassVar[int]
    OFFSET_0_VALID_FIELD_NUMBER: _ClassVar[int]
    OFFSET_1_VALID_FIELD_NUMBER: _ClassVar[int]
    OFFSET_2_VALID_FIELD_NUMBER: _ClassVar[int]
    OFFSET_3_VALID_FIELD_NUMBER: _ClassVar[int]
    TIME_OFFSET_0_FIELD_NUMBER: _ClassVar[int]
    TIME_OFFSET_1_FIELD_NUMBER: _ClassVar[int]
    TIME_OFFSET_2_FIELD_NUMBER: _ClassVar[int]
    TIME_OFFSET_3_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    time_stamp: int
    overflow: bool
    offset_0_valid: bool
    offset_1_valid: bool
    offset_2_valid: bool
    offset_3_valid: bool
    time_offset_0: int
    time_offset_1: int
    time_offset_2: int
    time_offset_3: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., time_stamp: _Optional[int] = ..., overflow: bool = ..., offset_0_valid: bool = ..., offset_1_valid: bool = ..., offset_2_valid: bool = ..., offset_3_valid: bool = ..., time_offset_0: _Optional[int] = ..., time_offset_1: _Optional[int] = ..., time_offset_2: _Optional[int] = ..., time_offset_3: _Optional[int] = ...) -> None: ...
