from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.rmf_task_msgs.msg import behavior_parameter_pb2 as _behavior_parameter_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Behavior(_message.Message):
    __slots__ = ("header", "name", "parameters")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    name: str
    parameters: _containers.RepeatedCompositeFieldContainer[_behavior_parameter_pb2.BehaviorParameter]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., name: _Optional[str] = ..., parameters: _Optional[_Iterable[_Union[_behavior_parameter_pb2.BehaviorParameter, _Mapping]]] = ...) -> None: ...
