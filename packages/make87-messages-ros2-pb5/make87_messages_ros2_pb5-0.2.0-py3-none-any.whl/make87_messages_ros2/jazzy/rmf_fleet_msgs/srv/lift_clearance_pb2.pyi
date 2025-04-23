from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class LiftClearanceRequest(_message.Message):
    __slots__ = ("robot_name", "lift_name")
    ROBOT_NAME_FIELD_NUMBER: _ClassVar[int]
    LIFT_NAME_FIELD_NUMBER: _ClassVar[int]
    robot_name: str
    lift_name: str
    def __init__(self, robot_name: _Optional[str] = ..., lift_name: _Optional[str] = ...) -> None: ...

class LiftClearanceResponse(_message.Message):
    __slots__ = ("decision",)
    DECISION_FIELD_NUMBER: _ClassVar[int]
    decision: int
    def __init__(self, decision: _Optional[int] = ...) -> None: ...
