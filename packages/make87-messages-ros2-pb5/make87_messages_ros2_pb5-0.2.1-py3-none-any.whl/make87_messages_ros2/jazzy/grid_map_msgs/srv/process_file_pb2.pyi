from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ProcessFileRequest(_message.Message):
    __slots__ = ("file_path", "topic_name")
    FILE_PATH_FIELD_NUMBER: _ClassVar[int]
    TOPIC_NAME_FIELD_NUMBER: _ClassVar[int]
    file_path: str
    topic_name: str
    def __init__(self, file_path: _Optional[str] = ..., topic_name: _Optional[str] = ...) -> None: ...

class ProcessFileResponse(_message.Message):
    __slots__ = ("success",)
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...
