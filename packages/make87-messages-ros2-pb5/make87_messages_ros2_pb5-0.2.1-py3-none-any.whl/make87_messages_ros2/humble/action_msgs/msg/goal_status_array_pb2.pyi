from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.action_msgs.msg import goal_status_pb2 as _goal_status_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GoalStatusArray(_message.Message):
    __slots__ = ("header", "status_list")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    STATUS_LIST_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    status_list: _containers.RepeatedCompositeFieldContainer[_goal_status_pb2.GoalStatus]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., status_list: _Optional[_Iterable[_Union[_goal_status_pb2.GoalStatus, _Mapping]]] = ...) -> None: ...
