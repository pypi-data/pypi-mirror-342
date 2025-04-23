from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ReloadControllerLibrariesRequest(_message.Message):
    __slots__ = ("header", "force_kill")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    FORCE_KILL_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    force_kill: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., force_kill: bool = ...) -> None: ...

class ReloadControllerLibrariesResponse(_message.Message):
    __slots__ = ("header", "ok")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    OK_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ok: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ok: bool = ...) -> None: ...
