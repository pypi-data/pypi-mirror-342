from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TestMultipleRequestFieldsRequest(_message.Message):
    __slots__ = ("header", "int_value", "float_value", "string", "bool_value")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    INT_VALUE_FIELD_NUMBER: _ClassVar[int]
    FLOAT_VALUE_FIELD_NUMBER: _ClassVar[int]
    STRING_FIELD_NUMBER: _ClassVar[int]
    BOOL_VALUE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    int_value: int
    float_value: float
    string: str
    bool_value: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., int_value: _Optional[int] = ..., float_value: _Optional[float] = ..., string: _Optional[str] = ..., bool_value: bool = ...) -> None: ...

class TestMultipleRequestFieldsResponse(_message.Message):
    __slots__ = ("header",)
    HEADER_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ...) -> None: ...
