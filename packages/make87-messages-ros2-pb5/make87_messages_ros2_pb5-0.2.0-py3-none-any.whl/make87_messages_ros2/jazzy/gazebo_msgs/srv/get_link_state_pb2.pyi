from make87_messages_ros2.jazzy.gazebo_msgs.msg import link_state_pb2 as _link_state_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetLinkStateRequest(_message.Message):
    __slots__ = ("link_name", "reference_frame")
    LINK_NAME_FIELD_NUMBER: _ClassVar[int]
    REFERENCE_FRAME_FIELD_NUMBER: _ClassVar[int]
    link_name: str
    reference_frame: str
    def __init__(self, link_name: _Optional[str] = ..., reference_frame: _Optional[str] = ...) -> None: ...

class GetLinkStateResponse(_message.Message):
    __slots__ = ("link_state", "success", "status_message")
    LINK_STATE_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    STATUS_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    link_state: _link_state_pb2.LinkState
    success: bool
    status_message: str
    def __init__(self, link_state: _Optional[_Union[_link_state_pb2.LinkState, _Mapping]] = ..., success: bool = ..., status_message: _Optional[str] = ...) -> None: ...
