from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class FRIState(_message.Message):
    __slots__ = ("header", "session_state", "connection_quality", "safety_state", "command_mode", "control_mode", "operation_mode", "drive_state", "overlay_type", "tracking_performance")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SESSION_STATE_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_QUALITY_FIELD_NUMBER: _ClassVar[int]
    SAFETY_STATE_FIELD_NUMBER: _ClassVar[int]
    COMMAND_MODE_FIELD_NUMBER: _ClassVar[int]
    CONTROL_MODE_FIELD_NUMBER: _ClassVar[int]
    OPERATION_MODE_FIELD_NUMBER: _ClassVar[int]
    DRIVE_STATE_FIELD_NUMBER: _ClassVar[int]
    OVERLAY_TYPE_FIELD_NUMBER: _ClassVar[int]
    TRACKING_PERFORMANCE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    session_state: int
    connection_quality: int
    safety_state: int
    command_mode: int
    control_mode: int
    operation_mode: int
    drive_state: int
    overlay_type: int
    tracking_performance: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., session_state: _Optional[int] = ..., connection_quality: _Optional[int] = ..., safety_state: _Optional[int] = ..., command_mode: _Optional[int] = ..., control_mode: _Optional[int] = ..., operation_mode: _Optional[int] = ..., drive_state: _Optional[int] = ..., overlay_type: _Optional[int] = ..., tracking_performance: _Optional[float] = ...) -> None: ...
