from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class StartGvmRecordingRequest(_message.Message):
    __slots__ = ("header", "disable_window", "world_as_main_view")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    DISABLE_WINDOW_FIELD_NUMBER: _ClassVar[int]
    WORLD_AS_MAIN_VIEW_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    disable_window: bool
    world_as_main_view: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., disable_window: bool = ..., world_as_main_view: bool = ...) -> None: ...

class StartGvmRecordingResponse(_message.Message):
    __slots__ = ("header",)
    HEADER_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ...) -> None: ...
