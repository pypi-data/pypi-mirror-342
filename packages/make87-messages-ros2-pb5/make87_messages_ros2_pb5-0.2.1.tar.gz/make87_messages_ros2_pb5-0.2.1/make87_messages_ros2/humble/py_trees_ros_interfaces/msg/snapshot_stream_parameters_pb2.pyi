from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SnapshotStreamParameters(_message.Message):
    __slots__ = ("header", "snapshot_period", "blackboard_data", "blackboard_activity")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SNAPSHOT_PERIOD_FIELD_NUMBER: _ClassVar[int]
    BLACKBOARD_DATA_FIELD_NUMBER: _ClassVar[int]
    BLACKBOARD_ACTIVITY_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    snapshot_period: float
    blackboard_data: bool
    blackboard_activity: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., snapshot_period: _Optional[float] = ..., blackboard_data: bool = ..., blackboard_activity: bool = ...) -> None: ...
