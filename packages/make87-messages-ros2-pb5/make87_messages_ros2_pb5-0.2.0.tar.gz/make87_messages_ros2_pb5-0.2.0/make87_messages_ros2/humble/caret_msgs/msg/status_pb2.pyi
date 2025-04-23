from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Status(_message.Message):
    __slots__ = ("header", "caret_node_name", "status", "node_names", "pid")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    CARET_NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    NODE_NAMES_FIELD_NUMBER: _ClassVar[int]
    PID_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    caret_node_name: str
    status: int
    node_names: _containers.RepeatedScalarFieldContainer[str]
    pid: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., caret_node_name: _Optional[str] = ..., status: _Optional[int] = ..., node_names: _Optional[_Iterable[str]] = ..., pid: _Optional[int] = ...) -> None: ...
