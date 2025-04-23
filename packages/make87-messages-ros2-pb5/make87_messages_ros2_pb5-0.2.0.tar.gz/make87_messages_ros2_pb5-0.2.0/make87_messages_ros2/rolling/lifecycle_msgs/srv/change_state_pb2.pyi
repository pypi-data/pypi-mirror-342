from make87_messages_ros2.rolling.lifecycle_msgs.msg import transition_pb2 as _transition_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ChangeStateRequest(_message.Message):
    __slots__ = ("transition",)
    TRANSITION_FIELD_NUMBER: _ClassVar[int]
    transition: _transition_pb2.Transition
    def __init__(self, transition: _Optional[_Union[_transition_pb2.Transition, _Mapping]] = ...) -> None: ...

class ChangeStateResponse(_message.Message):
    __slots__ = ("success",)
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...
