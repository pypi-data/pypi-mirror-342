from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class PlannerInterfaceDescription(_message.Message):
    __slots__ = ("name", "pipeline_id", "planner_ids")
    NAME_FIELD_NUMBER: _ClassVar[int]
    PIPELINE_ID_FIELD_NUMBER: _ClassVar[int]
    PLANNER_IDS_FIELD_NUMBER: _ClassVar[int]
    name: str
    pipeline_id: str
    planner_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, name: _Optional[str] = ..., pipeline_id: _Optional[str] = ..., planner_ids: _Optional[_Iterable[str]] = ...) -> None: ...
