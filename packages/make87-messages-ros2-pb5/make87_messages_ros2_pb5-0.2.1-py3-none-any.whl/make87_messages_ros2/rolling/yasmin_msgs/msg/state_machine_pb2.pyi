from make87_messages_ros2.rolling.yasmin_msgs.msg import state_pb2 as _state_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class StateMachine(_message.Message):
    __slots__ = ("states",)
    STATES_FIELD_NUMBER: _ClassVar[int]
    states: _containers.RepeatedCompositeFieldContainer[_state_pb2.State]
    def __init__(self, states: _Optional[_Iterable[_Union[_state_pb2.State, _Mapping]]] = ...) -> None: ...
