from make87_messages_ros2.jazzy.action_msgs.msg import goal_status_pb2 as _goal_status_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GoalStatusArray(_message.Message):
    __slots__ = ("status_list",)
    STATUS_LIST_FIELD_NUMBER: _ClassVar[int]
    status_list: _containers.RepeatedCompositeFieldContainer[_goal_status_pb2.GoalStatus]
    def __init__(self, status_list: _Optional[_Iterable[_Union[_goal_status_pb2.GoalStatus, _Mapping]]] = ...) -> None: ...
