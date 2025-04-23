from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class WaypointSetCurrentRequest(_message.Message):
    __slots__ = ("wp_seq",)
    WP_SEQ_FIELD_NUMBER: _ClassVar[int]
    wp_seq: int
    def __init__(self, wp_seq: _Optional[int] = ...) -> None: ...

class WaypointSetCurrentResponse(_message.Message):
    __slots__ = ("success",)
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...
