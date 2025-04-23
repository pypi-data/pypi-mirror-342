from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Circle(_message.Message):
    __slots__ = ("header", "radius")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    RADIUS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    radius: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., radius: _Optional[float] = ...) -> None: ...
