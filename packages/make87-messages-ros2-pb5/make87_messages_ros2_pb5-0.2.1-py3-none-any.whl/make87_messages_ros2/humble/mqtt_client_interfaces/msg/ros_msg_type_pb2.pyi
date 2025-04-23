from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RosMsgType(_message.Message):
    __slots__ = ("header", "md5", "name", "definition", "stamped")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    MD5_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DEFINITION_FIELD_NUMBER: _ClassVar[int]
    STAMPED_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    md5: str
    name: str
    definition: str
    stamped: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., md5: _Optional[str] = ..., name: _Optional[str] = ..., definition: _Optional[str] = ..., stamped: bool = ...) -> None: ...
