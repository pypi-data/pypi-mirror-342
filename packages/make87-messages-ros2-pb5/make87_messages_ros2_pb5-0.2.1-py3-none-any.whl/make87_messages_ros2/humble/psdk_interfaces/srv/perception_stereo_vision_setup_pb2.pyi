from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PerceptionStereoVisionSetupRequest(_message.Message):
    __slots__ = ("header", "stereo_cameras_direction", "start_stop")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    STEREO_CAMERAS_DIRECTION_FIELD_NUMBER: _ClassVar[int]
    START_STOP_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    stereo_cameras_direction: str
    start_stop: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., stereo_cameras_direction: _Optional[str] = ..., start_stop: bool = ...) -> None: ...

class PerceptionStereoVisionSetupResponse(_message.Message):
    __slots__ = ("header", "success", "message")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    success: bool
    message: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., success: bool = ..., message: _Optional[str] = ...) -> None: ...
