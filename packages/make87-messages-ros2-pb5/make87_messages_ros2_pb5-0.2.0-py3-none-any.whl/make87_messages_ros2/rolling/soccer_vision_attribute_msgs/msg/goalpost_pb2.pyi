from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Goalpost(_message.Message):
    __slots__ = ("side", "team")
    SIDE_FIELD_NUMBER: _ClassVar[int]
    TEAM_FIELD_NUMBER: _ClassVar[int]
    side: int
    team: int
    def __init__(self, side: _Optional[int] = ..., team: _Optional[int] = ...) -> None: ...
