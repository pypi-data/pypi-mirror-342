from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class FileTruncateRequest(_message.Message):
    __slots__ = ("header", "file_path", "length")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    FILE_PATH_FIELD_NUMBER: _ClassVar[int]
    LENGTH_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    file_path: str
    length: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., file_path: _Optional[str] = ..., length: _Optional[int] = ...) -> None: ...

class FileTruncateResponse(_message.Message):
    __slots__ = ("header", "success", "r_errno")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    R_ERRNO_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    success: bool
    r_errno: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., success: bool = ..., r_errno: _Optional[int] = ...) -> None: ...
