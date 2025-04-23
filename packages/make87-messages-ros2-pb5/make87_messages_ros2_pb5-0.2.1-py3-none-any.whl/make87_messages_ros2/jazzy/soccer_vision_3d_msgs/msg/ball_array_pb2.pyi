from make87_messages_ros2.jazzy.soccer_vision_3d_msgs.msg import ball_pb2 as _ball_pb2
from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BallArray(_message.Message):
    __slots__ = ("header", "balls")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    BALLS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    balls: _containers.RepeatedCompositeFieldContainer[_ball_pb2.Ball]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., balls: _Optional[_Iterable[_Union[_ball_pb2.Ball, _Mapping]]] = ...) -> None: ...
