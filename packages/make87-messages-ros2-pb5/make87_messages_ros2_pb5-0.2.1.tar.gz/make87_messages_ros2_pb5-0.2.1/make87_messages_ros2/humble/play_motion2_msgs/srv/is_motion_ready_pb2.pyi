from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class IsMotionReadyRequest(_message.Message):
    __slots__ = ("header", "motion_key")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    MOTION_KEY_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    motion_key: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., motion_key: _Optional[str] = ...) -> None: ...

class IsMotionReadyResponse(_message.Message):
    __slots__ = ("header", "is_ready")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    IS_READY_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    is_ready: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., is_ready: bool = ...) -> None: ...
