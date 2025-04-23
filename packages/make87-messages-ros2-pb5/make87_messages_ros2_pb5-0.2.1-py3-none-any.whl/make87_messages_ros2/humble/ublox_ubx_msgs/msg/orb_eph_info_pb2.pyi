from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class OrbEphInfo(_message.Message):
    __slots__ = ("header", "eph_usability", "eph_source")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    EPH_USABILITY_FIELD_NUMBER: _ClassVar[int]
    EPH_SOURCE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    eph_usability: int
    eph_source: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., eph_usability: _Optional[int] = ..., eph_source: _Optional[int] = ...) -> None: ...
