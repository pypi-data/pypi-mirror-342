from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class GetLoadedProgramRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetLoadedProgramResponse(_message.Message):
    __slots__ = ("answer", "program_name", "success")
    ANSWER_FIELD_NUMBER: _ClassVar[int]
    PROGRAM_NAME_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    answer: str
    program_name: str
    success: bool
    def __init__(self, answer: _Optional[str] = ..., program_name: _Optional[str] = ..., success: bool = ...) -> None: ...
