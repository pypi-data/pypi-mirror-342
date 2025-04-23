from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Assignment(_message.Message):
    __slots__ = ("is_assigned", "fleet_name", "expected_robot_name")
    IS_ASSIGNED_FIELD_NUMBER: _ClassVar[int]
    FLEET_NAME_FIELD_NUMBER: _ClassVar[int]
    EXPECTED_ROBOT_NAME_FIELD_NUMBER: _ClassVar[int]
    is_assigned: bool
    fleet_name: str
    expected_robot_name: str
    def __init__(self, is_assigned: bool = ..., fleet_name: _Optional[str] = ..., expected_robot_name: _Optional[str] = ...) -> None: ...
