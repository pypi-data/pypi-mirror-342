from make87_messages_ros2.jazzy.plansys2_msgs.msg import node_pb2 as _node_pb2
from make87_messages_ros2.jazzy.std_msgs.msg import empty_pb2 as _empty_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetStatesRequest(_message.Message):
    __slots__ = ("request",)
    REQUEST_FIELD_NUMBER: _ClassVar[int]
    request: _empty_pb2.Empty
    def __init__(self, request: _Optional[_Union[_empty_pb2.Empty, _Mapping]] = ...) -> None: ...

class GetStatesResponse(_message.Message):
    __slots__ = ("success", "states", "error_info")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    STATES_FIELD_NUMBER: _ClassVar[int]
    ERROR_INFO_FIELD_NUMBER: _ClassVar[int]
    success: bool
    states: _containers.RepeatedCompositeFieldContainer[_node_pb2.Node]
    error_info: str
    def __init__(self, success: bool = ..., states: _Optional[_Iterable[_Union[_node_pb2.Node, _Mapping]]] = ..., error_info: _Optional[str] = ...) -> None: ...
