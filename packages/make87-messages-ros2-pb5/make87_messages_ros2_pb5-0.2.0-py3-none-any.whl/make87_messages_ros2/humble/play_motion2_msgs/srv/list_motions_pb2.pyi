from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ListMotionsRequest(_message.Message):
    __slots__ = ("header",)
    HEADER_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ...) -> None: ...

class ListMotionsResponse(_message.Message):
    __slots__ = ("header", "motion_keys")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    MOTION_KEYS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    motion_keys: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., motion_keys: _Optional[_Iterable[str]] = ...) -> None: ...
