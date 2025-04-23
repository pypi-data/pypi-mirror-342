from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TrafficDependency(_message.Message):
    __slots__ = ("header", "dependent_checkpoint", "on_participant", "on_plan", "on_route", "on_checkpoint")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    DEPENDENT_CHECKPOINT_FIELD_NUMBER: _ClassVar[int]
    ON_PARTICIPANT_FIELD_NUMBER: _ClassVar[int]
    ON_PLAN_FIELD_NUMBER: _ClassVar[int]
    ON_ROUTE_FIELD_NUMBER: _ClassVar[int]
    ON_CHECKPOINT_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    dependent_checkpoint: int
    on_participant: int
    on_plan: int
    on_route: int
    on_checkpoint: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., dependent_checkpoint: _Optional[int] = ..., on_participant: _Optional[int] = ..., on_plan: _Optional[int] = ..., on_route: _Optional[int] = ..., on_checkpoint: _Optional[int] = ...) -> None: ...
