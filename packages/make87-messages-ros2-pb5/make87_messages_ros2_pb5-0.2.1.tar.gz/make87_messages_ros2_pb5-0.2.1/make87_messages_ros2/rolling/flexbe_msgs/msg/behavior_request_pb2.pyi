from make87_messages_ros2.rolling.flexbe_msgs.msg import container_pb2 as _container_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BehaviorRequest(_message.Message):
    __slots__ = ("behavior_name", "autonomy_level", "arg_keys", "arg_values", "structure")
    BEHAVIOR_NAME_FIELD_NUMBER: _ClassVar[int]
    AUTONOMY_LEVEL_FIELD_NUMBER: _ClassVar[int]
    ARG_KEYS_FIELD_NUMBER: _ClassVar[int]
    ARG_VALUES_FIELD_NUMBER: _ClassVar[int]
    STRUCTURE_FIELD_NUMBER: _ClassVar[int]
    behavior_name: str
    autonomy_level: int
    arg_keys: _containers.RepeatedScalarFieldContainer[str]
    arg_values: _containers.RepeatedScalarFieldContainer[str]
    structure: _containers.RepeatedCompositeFieldContainer[_container_pb2.Container]
    def __init__(self, behavior_name: _Optional[str] = ..., autonomy_level: _Optional[int] = ..., arg_keys: _Optional[_Iterable[str]] = ..., arg_values: _Optional[_Iterable[str]] = ..., structure: _Optional[_Iterable[_Union[_container_pb2.Container, _Mapping]]] = ...) -> None: ...
