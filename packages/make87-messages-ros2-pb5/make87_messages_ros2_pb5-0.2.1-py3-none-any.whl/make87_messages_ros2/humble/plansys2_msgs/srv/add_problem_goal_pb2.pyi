from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.plansys2_msgs.msg import tree_pb2 as _tree_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AddProblemGoalRequest(_message.Message):
    __slots__ = ("header", "tree")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TREE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    tree: _tree_pb2.Tree
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., tree: _Optional[_Union[_tree_pb2.Tree, _Mapping]] = ...) -> None: ...

class AddProblemGoalResponse(_message.Message):
    __slots__ = ("header", "success", "error_info")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_INFO_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    success: bool
    error_info: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., success: bool = ..., error_info: _Optional[str] = ...) -> None: ...
