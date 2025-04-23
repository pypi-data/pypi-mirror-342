from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class RobotMode(_message.Message):
    __slots__ = ("mode", "mode_request_id")
    MODE_FIELD_NUMBER: _ClassVar[int]
    MODE_REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    mode: int
    mode_request_id: int
    def __init__(self, mode: _Optional[int] = ..., mode_request_id: _Optional[int] = ...) -> None: ...
