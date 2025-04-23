from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.sensor_msgs.msg import joy_feedback_pb2 as _joy_feedback_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class JoyFeedbackArray(_message.Message):
    __slots__ = ("header", "array")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ARRAY_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    array: _containers.RepeatedCompositeFieldContainer[_joy_feedback_pb2.JoyFeedback]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., array: _Optional[_Iterable[_Union[_joy_feedback_pb2.JoyFeedback, _Mapping]]] = ...) -> None: ...
