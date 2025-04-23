from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MeshTriangle(_message.Message):
    __slots__ = ("header", "vertex_indices")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    VERTEX_INDICES_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    vertex_indices: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., vertex_indices: _Optional[_Iterable[int]] = ...) -> None: ...
