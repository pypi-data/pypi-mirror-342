from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class UserDisplay(_message.Message):
    __slots__ = ("header", "ip", "battery", "entries", "selected_entry")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    IP_FIELD_NUMBER: _ClassVar[int]
    BATTERY_FIELD_NUMBER: _ClassVar[int]
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    SELECTED_ENTRY_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ip: str
    battery: str
    entries: _containers.RepeatedScalarFieldContainer[str]
    selected_entry: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ip: _Optional[str] = ..., battery: _Optional[str] = ..., entries: _Optional[_Iterable[str]] = ..., selected_entry: _Optional[int] = ...) -> None: ...
