from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class NamedCollision(_message.Message):
    __slots__ = ("header", "entity0", "entity1")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ENTITY0_FIELD_NUMBER: _ClassVar[int]
    ENTITY1_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    entity0: str
    entity1: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., entity0: _Optional[str] = ..., entity1: _Optional[str] = ...) -> None: ...
