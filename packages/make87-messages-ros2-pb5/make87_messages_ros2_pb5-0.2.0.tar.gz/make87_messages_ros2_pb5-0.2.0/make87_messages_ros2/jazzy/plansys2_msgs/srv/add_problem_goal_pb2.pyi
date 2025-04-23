from make87_messages_ros2.jazzy.plansys2_msgs.msg import tree_pb2 as _tree_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AddProblemGoalRequest(_message.Message):
    __slots__ = ("tree",)
    TREE_FIELD_NUMBER: _ClassVar[int]
    tree: _tree_pb2.Tree
    def __init__(self, tree: _Optional[_Union[_tree_pb2.Tree, _Mapping]] = ...) -> None: ...

class AddProblemGoalResponse(_message.Message):
    __slots__ = ("success", "error_info")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_INFO_FIELD_NUMBER: _ClassVar[int]
    success: bool
    error_info: str
    def __init__(self, success: bool = ..., error_info: _Optional[str] = ...) -> None: ...
