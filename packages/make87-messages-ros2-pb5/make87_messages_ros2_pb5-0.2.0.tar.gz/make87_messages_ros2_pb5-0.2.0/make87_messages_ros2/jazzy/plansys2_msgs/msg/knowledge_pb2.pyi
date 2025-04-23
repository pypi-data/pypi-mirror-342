from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Knowledge(_message.Message):
    __slots__ = ("instances", "predicates", "functions", "goal")
    INSTANCES_FIELD_NUMBER: _ClassVar[int]
    PREDICATES_FIELD_NUMBER: _ClassVar[int]
    FUNCTIONS_FIELD_NUMBER: _ClassVar[int]
    GOAL_FIELD_NUMBER: _ClassVar[int]
    instances: _containers.RepeatedScalarFieldContainer[str]
    predicates: _containers.RepeatedScalarFieldContainer[str]
    functions: _containers.RepeatedScalarFieldContainer[str]
    goal: str
    def __init__(self, instances: _Optional[_Iterable[str]] = ..., predicates: _Optional[_Iterable[str]] = ..., functions: _Optional[_Iterable[str]] = ..., goal: _Optional[str] = ...) -> None: ...
