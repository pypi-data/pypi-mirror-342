from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class GetRobotSoftwareVersionRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetRobotSoftwareVersionResponse(_message.Message):
    __slots__ = ("major", "minor", "bugfix", "build")
    MAJOR_FIELD_NUMBER: _ClassVar[int]
    MINOR_FIELD_NUMBER: _ClassVar[int]
    BUGFIX_FIELD_NUMBER: _ClassVar[int]
    BUILD_FIELD_NUMBER: _ClassVar[int]
    major: int
    minor: int
    bugfix: int
    build: int
    def __init__(self, major: _Optional[int] = ..., minor: _Optional[int] = ..., bugfix: _Optional[int] = ..., build: _Optional[int] = ...) -> None: ...
