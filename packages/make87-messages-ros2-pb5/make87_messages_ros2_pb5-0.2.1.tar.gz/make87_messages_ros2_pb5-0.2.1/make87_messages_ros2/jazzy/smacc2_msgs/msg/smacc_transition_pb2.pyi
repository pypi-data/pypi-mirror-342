from make87_messages_ros2.jazzy.smacc2_msgs.msg import smacc_event_pb2 as _smacc_event_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SmaccTransition(_message.Message):
    __slots__ = ("index", "transition_name", "transition_type", "destiny_state_name", "source_state_name", "history_node", "event")
    INDEX_FIELD_NUMBER: _ClassVar[int]
    TRANSITION_NAME_FIELD_NUMBER: _ClassVar[int]
    TRANSITION_TYPE_FIELD_NUMBER: _ClassVar[int]
    DESTINY_STATE_NAME_FIELD_NUMBER: _ClassVar[int]
    SOURCE_STATE_NAME_FIELD_NUMBER: _ClassVar[int]
    HISTORY_NODE_FIELD_NUMBER: _ClassVar[int]
    EVENT_FIELD_NUMBER: _ClassVar[int]
    index: int
    transition_name: str
    transition_type: str
    destiny_state_name: str
    source_state_name: str
    history_node: bool
    event: _smacc_event_pb2.SmaccEvent
    def __init__(self, index: _Optional[int] = ..., transition_name: _Optional[str] = ..., transition_type: _Optional[str] = ..., destiny_state_name: _Optional[str] = ..., source_state_name: _Optional[str] = ..., history_node: bool = ..., event: _Optional[_Union[_smacc_event_pb2.SmaccEvent, _Mapping]] = ...) -> None: ...
