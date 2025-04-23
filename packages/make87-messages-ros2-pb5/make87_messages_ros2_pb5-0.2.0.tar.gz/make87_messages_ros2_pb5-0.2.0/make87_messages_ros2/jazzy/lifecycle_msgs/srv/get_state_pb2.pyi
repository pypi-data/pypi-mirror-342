from make87_messages_ros2.jazzy.lifecycle_msgs.msg import state_pb2 as _state_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetStateRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetStateResponse(_message.Message):
    __slots__ = ("current_state",)
    CURRENT_STATE_FIELD_NUMBER: _ClassVar[int]
    current_state: _state_pb2.State
    def __init__(self, current_state: _Optional[_Union[_state_pb2.State, _Mapping]] = ...) -> None: ...
