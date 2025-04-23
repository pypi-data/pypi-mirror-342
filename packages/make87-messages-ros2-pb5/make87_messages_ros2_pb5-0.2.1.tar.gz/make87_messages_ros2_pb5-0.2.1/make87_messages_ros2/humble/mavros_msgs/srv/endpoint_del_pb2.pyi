from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EndpointDelRequest(_message.Message):
    __slots__ = ("header", "id", "url", "type")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    id: int
    url: str
    type: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., id: _Optional[int] = ..., url: _Optional[str] = ..., type: _Optional[int] = ...) -> None: ...

class EndpointDelResponse(_message.Message):
    __slots__ = ("header", "successful")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUCCESSFUL_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    successful: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., successful: bool = ...) -> None: ...
