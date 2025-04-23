from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class FileRenameRequest(_message.Message):
    __slots__ = ("old_path", "new_path")
    OLD_PATH_FIELD_NUMBER: _ClassVar[int]
    NEW_PATH_FIELD_NUMBER: _ClassVar[int]
    old_path: str
    new_path: str
    def __init__(self, old_path: _Optional[str] = ..., new_path: _Optional[str] = ...) -> None: ...

class FileRenameResponse(_message.Message):
    __slots__ = ("success", "r_errno")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    R_ERRNO_FIELD_NUMBER: _ClassVar[int]
    success: bool
    r_errno: int
    def __init__(self, success: bool = ..., r_errno: _Optional[int] = ...) -> None: ...
