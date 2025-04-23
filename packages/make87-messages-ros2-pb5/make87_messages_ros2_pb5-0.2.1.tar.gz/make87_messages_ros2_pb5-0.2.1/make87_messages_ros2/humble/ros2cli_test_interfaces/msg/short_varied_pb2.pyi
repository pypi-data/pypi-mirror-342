from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ShortVaried(_message.Message):
    __slots__ = ("header", "bool_value", "bool_values")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    BOOL_VALUE_FIELD_NUMBER: _ClassVar[int]
    BOOL_VALUES_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    bool_value: bool
    bool_values: _containers.RepeatedScalarFieldContainer[bool]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., bool_value: bool = ..., bool_values: _Optional[_Iterable[bool]] = ...) -> None: ...
