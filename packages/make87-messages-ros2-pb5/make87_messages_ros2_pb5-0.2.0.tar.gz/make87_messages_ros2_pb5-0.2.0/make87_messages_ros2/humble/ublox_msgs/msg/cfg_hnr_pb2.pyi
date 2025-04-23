from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CfgHNR(_message.Message):
    __slots__ = ("header", "high_nav_rate", "reserved0")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    HIGH_NAV_RATE_FIELD_NUMBER: _ClassVar[int]
    RESERVED0_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    high_nav_rate: int
    reserved0: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., high_nav_rate: _Optional[int] = ..., reserved0: _Optional[_Iterable[int]] = ...) -> None: ...
