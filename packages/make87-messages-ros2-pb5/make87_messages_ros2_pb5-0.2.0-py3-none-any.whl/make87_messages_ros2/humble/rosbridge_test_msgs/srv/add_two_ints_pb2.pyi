from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AddTwoIntsRequest(_message.Message):
    __slots__ = ("header", "a", "b")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    A_FIELD_NUMBER: _ClassVar[int]
    B_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    a: int
    b: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., a: _Optional[int] = ..., b: _Optional[int] = ...) -> None: ...

class AddTwoIntsResponse(_message.Message):
    __slots__ = ("header", "sum")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUM_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    sum: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., sum: _Optional[int] = ...) -> None: ...
