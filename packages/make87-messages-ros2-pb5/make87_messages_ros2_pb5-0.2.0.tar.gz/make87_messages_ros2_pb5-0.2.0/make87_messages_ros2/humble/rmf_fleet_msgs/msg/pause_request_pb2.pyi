from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PauseRequest(_message.Message):
    __slots__ = ("header", "fleet_name", "robot_name", "mode_request_id", "type", "at_checkpoint")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    FLEET_NAME_FIELD_NUMBER: _ClassVar[int]
    ROBOT_NAME_FIELD_NUMBER: _ClassVar[int]
    MODE_REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    AT_CHECKPOINT_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    fleet_name: str
    robot_name: str
    mode_request_id: int
    type: int
    at_checkpoint: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., fleet_name: _Optional[str] = ..., robot_name: _Optional[str] = ..., mode_request_id: _Optional[int] = ..., type: _Optional[int] = ..., at_checkpoint: _Optional[int] = ...) -> None: ...
