from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class SaveGeometryToFileRequest(_message.Message):
    __slots__ = ("file_path_and_name",)
    FILE_PATH_AND_NAME_FIELD_NUMBER: _ClassVar[int]
    file_path_and_name: str
    def __init__(self, file_path_and_name: _Optional[str] = ...) -> None: ...

class SaveGeometryToFileResponse(_message.Message):
    __slots__ = ("success",)
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...
