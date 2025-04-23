from make87_messages_ros2.jazzy.gazebo_msgs.msg import link_state_pb2 as _link_state_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SetLinkStateRequest(_message.Message):
    __slots__ = ("link_state",)
    LINK_STATE_FIELD_NUMBER: _ClassVar[int]
    link_state: _link_state_pb2.LinkState
    def __init__(self, link_state: _Optional[_Union[_link_state_pb2.LinkState, _Mapping]] = ...) -> None: ...

class SetLinkStateResponse(_message.Message):
    __slots__ = ("success", "status_message")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    STATUS_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    status_message: str
    def __init__(self, success: bool = ..., status_message: _Optional[str] = ...) -> None: ...
