from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetParamRequest(_message.Message):
    __slots__ = ("header", "name", "default_value")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_VALUE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    name: str
    default_value: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., name: _Optional[str] = ..., default_value: _Optional[str] = ...) -> None: ...

class GetParamResponse(_message.Message):
    __slots__ = ("header", "value")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    value: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., value: _Optional[str] = ...) -> None: ...
