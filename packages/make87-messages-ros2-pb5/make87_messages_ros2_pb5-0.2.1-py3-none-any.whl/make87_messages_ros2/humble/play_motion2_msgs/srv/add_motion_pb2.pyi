from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.play_motion2_msgs.msg import motion_pb2 as _motion_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AddMotionRequest(_message.Message):
    __slots__ = ("header", "motion", "overwrite")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    MOTION_FIELD_NUMBER: _ClassVar[int]
    OVERWRITE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    motion: _motion_pb2.Motion
    overwrite: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., motion: _Optional[_Union[_motion_pb2.Motion, _Mapping]] = ..., overwrite: bool = ...) -> None: ...

class AddMotionResponse(_message.Message):
    __slots__ = ("header", "success")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    success: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., success: bool = ...) -> None: ...
