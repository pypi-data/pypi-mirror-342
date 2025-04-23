from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.situational_graphs_reasoning_msgs.msg import keyframe_pb2 as _keyframe_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GraphKeyframes(_message.Message):
    __slots__ = ("header", "type", "robot", "keyframes")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    ROBOT_FIELD_NUMBER: _ClassVar[int]
    KEYFRAMES_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    type: str
    robot: str
    keyframes: _containers.RepeatedCompositeFieldContainer[_keyframe_pb2.Keyframe]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., type: _Optional[str] = ..., robot: _Optional[str] = ..., keyframes: _Optional[_Iterable[_Union[_keyframe_pb2.Keyframe, _Mapping]]] = ...) -> None: ...
