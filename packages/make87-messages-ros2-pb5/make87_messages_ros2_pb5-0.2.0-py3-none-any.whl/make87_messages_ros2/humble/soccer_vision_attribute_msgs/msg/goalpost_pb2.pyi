from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Goalpost(_message.Message):
    __slots__ = ("header", "side", "team")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SIDE_FIELD_NUMBER: _ClassVar[int]
    TEAM_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    side: int
    team: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., side: _Optional[int] = ..., team: _Optional[int] = ...) -> None: ...
