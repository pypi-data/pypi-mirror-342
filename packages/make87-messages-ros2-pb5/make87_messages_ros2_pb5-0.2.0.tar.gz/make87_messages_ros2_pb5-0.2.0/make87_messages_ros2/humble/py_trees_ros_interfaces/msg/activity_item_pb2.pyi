from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ActivityItem(_message.Message):
    __slots__ = ("header", "key", "client_name", "activity_type", "previous_value", "current_value")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    CLIENT_NAME_FIELD_NUMBER: _ClassVar[int]
    ACTIVITY_TYPE_FIELD_NUMBER: _ClassVar[int]
    PREVIOUS_VALUE_FIELD_NUMBER: _ClassVar[int]
    CURRENT_VALUE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    key: str
    client_name: str
    activity_type: str
    previous_value: str
    current_value: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., key: _Optional[str] = ..., client_name: _Optional[str] = ..., activity_type: _Optional[str] = ..., previous_value: _Optional[str] = ..., current_value: _Optional[str] = ...) -> None: ...
