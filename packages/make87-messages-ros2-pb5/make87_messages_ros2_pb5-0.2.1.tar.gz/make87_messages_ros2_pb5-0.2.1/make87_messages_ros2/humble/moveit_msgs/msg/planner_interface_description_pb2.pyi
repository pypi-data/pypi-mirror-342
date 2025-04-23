from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PlannerInterfaceDescription(_message.Message):
    __slots__ = ("header", "name", "pipeline_id", "planner_ids")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PIPELINE_ID_FIELD_NUMBER: _ClassVar[int]
    PLANNER_IDS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    name: str
    pipeline_id: str
    planner_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., name: _Optional[str] = ..., pipeline_id: _Optional[str] = ..., planner_ids: _Optional[_Iterable[str]] = ...) -> None: ...
