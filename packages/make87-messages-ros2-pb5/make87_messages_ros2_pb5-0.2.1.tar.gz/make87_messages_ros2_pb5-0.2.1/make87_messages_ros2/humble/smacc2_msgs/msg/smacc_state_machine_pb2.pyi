from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.smacc2_msgs.msg import smacc_state_pb2 as _smacc_state_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SmaccStateMachine(_message.Message):
    __slots__ = ("header", "states")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    STATES_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    states: _containers.RepeatedCompositeFieldContainer[_smacc_state_pb2.SmaccState]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., states: _Optional[_Iterable[_Union[_smacc_state_pb2.SmaccState, _Mapping]]] = ...) -> None: ...
