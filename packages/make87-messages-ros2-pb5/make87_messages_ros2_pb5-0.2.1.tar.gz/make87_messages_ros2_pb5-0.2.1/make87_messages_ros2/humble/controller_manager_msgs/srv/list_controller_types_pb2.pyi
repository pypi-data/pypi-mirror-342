from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ListControllerTypesRequest(_message.Message):
    __slots__ = ("header",)
    HEADER_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ...) -> None: ...

class ListControllerTypesResponse(_message.Message):
    __slots__ = ("header", "types", "base_classes")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TYPES_FIELD_NUMBER: _ClassVar[int]
    BASE_CLASSES_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    types: _containers.RepeatedScalarFieldContainer[str]
    base_classes: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., types: _Optional[_Iterable[str]] = ..., base_classes: _Optional[_Iterable[str]] = ...) -> None: ...
