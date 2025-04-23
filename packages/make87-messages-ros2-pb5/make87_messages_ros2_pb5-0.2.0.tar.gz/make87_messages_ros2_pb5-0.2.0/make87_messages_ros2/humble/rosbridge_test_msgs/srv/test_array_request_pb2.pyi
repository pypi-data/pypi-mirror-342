from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TestArrayRequestRequest(_message.Message):
    __slots__ = ("header", "int_values")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    INT_VALUES_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    int_values: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., int_values: _Optional[_Iterable[int]] = ...) -> None: ...

class TestArrayRequestResponse(_message.Message):
    __slots__ = ("header",)
    HEADER_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ...) -> None: ...
