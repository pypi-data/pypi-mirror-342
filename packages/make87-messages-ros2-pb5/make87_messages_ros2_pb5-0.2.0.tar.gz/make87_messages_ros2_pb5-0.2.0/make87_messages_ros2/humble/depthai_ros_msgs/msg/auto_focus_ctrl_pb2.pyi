from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AutoFocusCtrl(_message.Message):
    __slots__ = ("header", "auto_focus_mode", "trigger_auto_focus")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    AUTO_FOCUS_MODE_FIELD_NUMBER: _ClassVar[int]
    TRIGGER_AUTO_FOCUS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    auto_focus_mode: int
    trigger_auto_focus: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., auto_focus_mode: _Optional[int] = ..., trigger_auto_focus: bool = ...) -> None: ...
