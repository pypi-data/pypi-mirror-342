from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ScheduleState(_message.Message):
    __slots__ = ("header", "name", "last_modified", "last_ran", "next_run", "status")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    LAST_MODIFIED_FIELD_NUMBER: _ClassVar[int]
    LAST_RAN_FIELD_NUMBER: _ClassVar[int]
    NEXT_RUN_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    name: str
    last_modified: int
    last_ran: int
    next_run: int
    status: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., name: _Optional[str] = ..., last_modified: _Optional[int] = ..., last_ran: _Optional[int] = ..., next_run: _Optional[int] = ..., status: _Optional[int] = ...) -> None: ...
