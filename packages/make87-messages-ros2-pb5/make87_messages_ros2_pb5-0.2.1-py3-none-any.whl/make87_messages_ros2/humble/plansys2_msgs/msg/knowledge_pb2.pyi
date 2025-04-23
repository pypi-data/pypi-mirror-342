from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Knowledge(_message.Message):
    __slots__ = ("header", "instances", "predicates", "functions", "goal")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    INSTANCES_FIELD_NUMBER: _ClassVar[int]
    PREDICATES_FIELD_NUMBER: _ClassVar[int]
    FUNCTIONS_FIELD_NUMBER: _ClassVar[int]
    GOAL_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    instances: _containers.RepeatedScalarFieldContainer[str]
    predicates: _containers.RepeatedScalarFieldContainer[str]
    functions: _containers.RepeatedScalarFieldContainer[str]
    goal: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., instances: _Optional[_Iterable[str]] = ..., predicates: _Optional[_Iterable[str]] = ..., functions: _Optional[_Iterable[str]] = ..., goal: _Optional[str] = ...) -> None: ...
