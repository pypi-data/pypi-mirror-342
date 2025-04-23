from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Scenario(_message.Message):
    __slots__ = ("name", "scenario_file")
    NAME_FIELD_NUMBER: _ClassVar[int]
    SCENARIO_FILE_FIELD_NUMBER: _ClassVar[int]
    name: str
    scenario_file: str
    def __init__(self, name: _Optional[str] = ..., scenario_file: _Optional[str] = ...) -> None: ...
