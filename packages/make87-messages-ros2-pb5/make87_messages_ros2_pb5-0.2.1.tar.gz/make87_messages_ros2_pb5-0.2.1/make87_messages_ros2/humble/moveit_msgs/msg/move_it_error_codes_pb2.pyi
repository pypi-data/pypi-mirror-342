from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MoveItErrorCodes(_message.Message):
    __slots__ = ("header", "val", "message", "source")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    VAL_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    val: int
    message: str
    source: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., val: _Optional[int] = ..., message: _Optional[str] = ..., source: _Optional[str] = ...) -> None: ...
