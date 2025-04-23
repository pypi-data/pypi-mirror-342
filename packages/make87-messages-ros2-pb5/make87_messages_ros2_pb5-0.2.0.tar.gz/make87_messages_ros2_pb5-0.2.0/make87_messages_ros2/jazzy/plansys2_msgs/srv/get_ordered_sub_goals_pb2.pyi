from make87_messages_ros2.jazzy.plansys2_msgs.msg import tree_pb2 as _tree_pb2
from make87_messages_ros2.jazzy.std_msgs.msg import empty_pb2 as _empty_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetOrderedSubGoalsRequest(_message.Message):
    __slots__ = ("request",)
    REQUEST_FIELD_NUMBER: _ClassVar[int]
    request: _empty_pb2.Empty
    def __init__(self, request: _Optional[_Union[_empty_pb2.Empty, _Mapping]] = ...) -> None: ...

class GetOrderedSubGoalsResponse(_message.Message):
    __slots__ = ("success", "sub_goals", "error_info")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    SUB_GOALS_FIELD_NUMBER: _ClassVar[int]
    ERROR_INFO_FIELD_NUMBER: _ClassVar[int]
    success: bool
    sub_goals: _containers.RepeatedCompositeFieldContainer[_tree_pb2.Tree]
    error_info: str
    def __init__(self, success: bool = ..., sub_goals: _Optional[_Iterable[_Union[_tree_pb2.Tree, _Mapping]]] = ..., error_info: _Optional[str] = ...) -> None: ...
