from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class IOOSSDSState(_message.Message):
    __slots__ = ("header", "ossd1a", "ossd1b", "ossd2a", "ossd2b")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    OSSD1A_FIELD_NUMBER: _ClassVar[int]
    OSSD1B_FIELD_NUMBER: _ClassVar[int]
    OSSD2A_FIELD_NUMBER: _ClassVar[int]
    OSSD2B_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ossd1a: int
    ossd1b: int
    ossd2a: int
    ossd2b: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ossd1a: _Optional[int] = ..., ossd1b: _Optional[int] = ..., ossd2a: _Optional[int] = ..., ossd2b: _Optional[int] = ...) -> None: ...
