from make87_messages_ros2.rolling.sensor_msgs.msg import joy_feedback_pb2 as _joy_feedback_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class JoyFeedbackArray(_message.Message):
    __slots__ = ("array",)
    ARRAY_FIELD_NUMBER: _ClassVar[int]
    array: _containers.RepeatedCompositeFieldContainer[_joy_feedback_pb2.JoyFeedback]
    def __init__(self, array: _Optional[_Iterable[_Union[_joy_feedback_pb2.JoyFeedback, _Mapping]]] = ...) -> None: ...
