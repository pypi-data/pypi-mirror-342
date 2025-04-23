from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class RequestHeader(_message.Message):
    __slots__ = ("robot_name", "fleet_name", "request_id")
    ROBOT_NAME_FIELD_NUMBER: _ClassVar[int]
    FLEET_NAME_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    robot_name: str
    fleet_name: str
    request_id: int
    def __init__(self, robot_name: _Optional[str] = ..., fleet_name: _Optional[str] = ..., request_id: _Optional[int] = ...) -> None: ...
