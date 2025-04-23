from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CollisionMonitorState(_message.Message):
    __slots__ = ("header", "action_type", "polygon_name")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ACTION_TYPE_FIELD_NUMBER: _ClassVar[int]
    POLYGON_NAME_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    action_type: int
    polygon_name: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., action_type: _Optional[int] = ..., polygon_name: _Optional[str] = ...) -> None: ...
