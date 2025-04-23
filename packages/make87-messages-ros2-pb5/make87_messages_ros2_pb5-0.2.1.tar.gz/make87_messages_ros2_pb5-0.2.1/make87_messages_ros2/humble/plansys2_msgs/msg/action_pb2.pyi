from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.plansys2_msgs.msg import param_pb2 as _param_pb2
from make87_messages_ros2.humble.plansys2_msgs.msg import tree_pb2 as _tree_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Action(_message.Message):
    __slots__ = ("header", "name", "parameters", "preconditions", "effects")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    PRECONDITIONS_FIELD_NUMBER: _ClassVar[int]
    EFFECTS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    name: str
    parameters: _containers.RepeatedCompositeFieldContainer[_param_pb2.Param]
    preconditions: _tree_pb2.Tree
    effects: _tree_pb2.Tree
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., name: _Optional[str] = ..., parameters: _Optional[_Iterable[_Union[_param_pb2.Param, _Mapping]]] = ..., preconditions: _Optional[_Union[_tree_pb2.Tree, _Mapping]] = ..., effects: _Optional[_Union[_tree_pb2.Tree, _Mapping]] = ...) -> None: ...
