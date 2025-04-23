from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ApiResponse(_message.Message):
    __slots__ = ("type", "json_msg", "request_id")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    JSON_MSG_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    type: int
    json_msg: str
    request_id: str
    def __init__(self, type: _Optional[int] = ..., json_msg: _Optional[str] = ..., request_id: _Optional[str] = ...) -> None: ...
