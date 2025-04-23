from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.flexbe_msgs.msg import behavior_modification_pb2 as _behavior_modification_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BehaviorSelection(_message.Message):
    __slots__ = ("header", "behavior_key", "behavior_id", "autonomy_level", "arg_keys", "arg_values", "input_keys", "input_values", "modifications")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    BEHAVIOR_KEY_FIELD_NUMBER: _ClassVar[int]
    BEHAVIOR_ID_FIELD_NUMBER: _ClassVar[int]
    AUTONOMY_LEVEL_FIELD_NUMBER: _ClassVar[int]
    ARG_KEYS_FIELD_NUMBER: _ClassVar[int]
    ARG_VALUES_FIELD_NUMBER: _ClassVar[int]
    INPUT_KEYS_FIELD_NUMBER: _ClassVar[int]
    INPUT_VALUES_FIELD_NUMBER: _ClassVar[int]
    MODIFICATIONS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    behavior_key: int
    behavior_id: int
    autonomy_level: int
    arg_keys: _containers.RepeatedScalarFieldContainer[str]
    arg_values: _containers.RepeatedScalarFieldContainer[str]
    input_keys: _containers.RepeatedScalarFieldContainer[str]
    input_values: _containers.RepeatedScalarFieldContainer[str]
    modifications: _containers.RepeatedCompositeFieldContainer[_behavior_modification_pb2.BehaviorModification]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., behavior_key: _Optional[int] = ..., behavior_id: _Optional[int] = ..., autonomy_level: _Optional[int] = ..., arg_keys: _Optional[_Iterable[str]] = ..., arg_values: _Optional[_Iterable[str]] = ..., input_keys: _Optional[_Iterable[str]] = ..., input_values: _Optional[_Iterable[str]] = ..., modifications: _Optional[_Iterable[_Union[_behavior_modification_pb2.BehaviorModification, _Mapping]]] = ...) -> None: ...
