from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ListNodesRequest(_message.Message):
    __slots__ = ("header",)
    HEADER_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ...) -> None: ...

class ListNodesResponse(_message.Message):
    __slots__ = ("header", "full_node_names", "unique_ids")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    FULL_NODE_NAMES_FIELD_NUMBER: _ClassVar[int]
    UNIQUE_IDS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    full_node_names: _containers.RepeatedScalarFieldContainer[str]
    unique_ids: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., full_node_names: _Optional[_Iterable[str]] = ..., unique_ids: _Optional[_Iterable[int]] = ...) -> None: ...
