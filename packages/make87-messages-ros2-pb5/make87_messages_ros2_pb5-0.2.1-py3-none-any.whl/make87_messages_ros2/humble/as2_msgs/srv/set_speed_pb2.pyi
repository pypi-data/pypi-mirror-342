from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.as2_msgs.msg import speed_pb2 as _speed_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SetSpeedRequest(_message.Message):
    __slots__ = ("header", "speed")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SPEED_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    speed: _speed_pb2.Speed
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., speed: _Optional[_Union[_speed_pb2.Speed, _Mapping]] = ...) -> None: ...

class SetSpeedResponse(_message.Message):
    __slots__ = ("header", "success")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    success: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., success: bool = ...) -> None: ...
