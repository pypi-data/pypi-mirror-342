from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class RobotMode(_message.Message):
    __slots__ = ("mode", "mode_request_id", "performing_action")
    MODE_FIELD_NUMBER: _ClassVar[int]
    MODE_REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    PERFORMING_ACTION_FIELD_NUMBER: _ClassVar[int]
    mode: int
    mode_request_id: int
    performing_action: str
    def __init__(self, mode: _Optional[int] = ..., mode_request_id: _Optional[int] = ..., performing_action: _Optional[str] = ...) -> None: ...
