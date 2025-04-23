from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ColorRGBA(_message.Message):
    __slots__ = ("header", "r", "g", "b", "a")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    R_FIELD_NUMBER: _ClassVar[int]
    G_FIELD_NUMBER: _ClassVar[int]
    B_FIELD_NUMBER: _ClassVar[int]
    A_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    r: float
    g: float
    b: float
    a: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., r: _Optional[float] = ..., g: _Optional[float] = ..., b: _Optional[float] = ..., a: _Optional[float] = ...) -> None: ...
