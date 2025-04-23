from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.action_msgs.msg import goal_info_pb2 as _goal_info_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CancelGoalRequest(_message.Message):
    __slots__ = ("header", "goal_info")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    GOAL_INFO_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    goal_info: _goal_info_pb2.GoalInfo
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., goal_info: _Optional[_Union[_goal_info_pb2.GoalInfo, _Mapping]] = ...) -> None: ...

class CancelGoalResponse(_message.Message):
    __slots__ = ("header", "return_code", "goals_canceling")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    RETURN_CODE_FIELD_NUMBER: _ClassVar[int]
    GOALS_CANCELING_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    return_code: int
    goals_canceling: _containers.RepeatedCompositeFieldContainer[_goal_info_pb2.GoalInfo]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., return_code: _Optional[int] = ..., goals_canceling: _Optional[_Iterable[_Union[_goal_info_pb2.GoalInfo, _Mapping]]] = ...) -> None: ...
