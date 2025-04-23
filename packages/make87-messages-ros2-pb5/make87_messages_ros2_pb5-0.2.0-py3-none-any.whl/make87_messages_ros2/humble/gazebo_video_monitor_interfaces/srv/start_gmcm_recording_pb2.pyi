from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.gazebo_video_monitor_interfaces.msg import strings_pb2 as _strings_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class StartGmcmRecordingRequest(_message.Message):
    __slots__ = ("header", "cameras")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    CAMERAS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    cameras: _strings_pb2.Strings
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., cameras: _Optional[_Union[_strings_pb2.Strings, _Mapping]] = ...) -> None: ...

class StartGmcmRecordingResponse(_message.Message):
    __slots__ = ("header",)
    HEADER_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ...) -> None: ...
