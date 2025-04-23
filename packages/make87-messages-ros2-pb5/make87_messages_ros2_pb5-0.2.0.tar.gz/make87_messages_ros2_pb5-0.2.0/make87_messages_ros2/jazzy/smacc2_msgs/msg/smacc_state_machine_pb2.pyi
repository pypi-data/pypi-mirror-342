from make87_messages_ros2.jazzy.smacc2_msgs.msg import smacc_state_pb2 as _smacc_state_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SmaccStateMachine(_message.Message):
    __slots__ = ("states",)
    STATES_FIELD_NUMBER: _ClassVar[int]
    states: _containers.RepeatedCompositeFieldContainer[_smacc_state_pb2.SmaccState]
    def __init__(self, states: _Optional[_Iterable[_Union[_smacc_state_pb2.SmaccState, _Mapping]]] = ...) -> None: ...
