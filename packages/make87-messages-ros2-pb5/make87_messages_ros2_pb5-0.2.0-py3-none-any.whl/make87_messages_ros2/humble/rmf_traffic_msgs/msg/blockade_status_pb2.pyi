from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BlockadeStatus(_message.Message):
    __slots__ = ("header", "participant", "reservation", "any_ready", "last_ready", "last_reached", "assignment_begin", "assignment_end")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    PARTICIPANT_FIELD_NUMBER: _ClassVar[int]
    RESERVATION_FIELD_NUMBER: _ClassVar[int]
    ANY_READY_FIELD_NUMBER: _ClassVar[int]
    LAST_READY_FIELD_NUMBER: _ClassVar[int]
    LAST_REACHED_FIELD_NUMBER: _ClassVar[int]
    ASSIGNMENT_BEGIN_FIELD_NUMBER: _ClassVar[int]
    ASSIGNMENT_END_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    participant: int
    reservation: int
    any_ready: bool
    last_ready: int
    last_reached: int
    assignment_begin: int
    assignment_end: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., participant: _Optional[int] = ..., reservation: _Optional[int] = ..., any_ready: bool = ..., last_ready: _Optional[int] = ..., last_reached: _Optional[int] = ..., assignment_begin: _Optional[int] = ..., assignment_end: _Optional[int] = ...) -> None: ...
