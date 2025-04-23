from make87_messages_ros2.jazzy.plansys2_msgs.msg import node_pb2 as _node_pb2
from make87_messages_ros2.jazzy.plansys2_msgs.msg import tree_pb2 as _tree_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Derived(_message.Message):
    __slots__ = ("predicate", "preconditions")
    PREDICATE_FIELD_NUMBER: _ClassVar[int]
    PRECONDITIONS_FIELD_NUMBER: _ClassVar[int]
    predicate: _node_pb2.Node
    preconditions: _tree_pb2.Tree
    def __init__(self, predicate: _Optional[_Union[_node_pb2.Node, _Mapping]] = ..., preconditions: _Optional[_Union[_tree_pb2.Tree, _Mapping]] = ...) -> None: ...
