from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SigLogEvent(_message.Message):
    __slots__ = ("header", "time_elapsed", "detection_type", "event_type")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TIME_ELAPSED_FIELD_NUMBER: _ClassVar[int]
    DETECTION_TYPE_FIELD_NUMBER: _ClassVar[int]
    EVENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    time_elapsed: int
    detection_type: int
    event_type: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., time_elapsed: _Optional[int] = ..., detection_type: _Optional[int] = ..., event_type: _Optional[int] = ...) -> None: ...
