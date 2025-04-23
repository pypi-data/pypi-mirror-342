from make87_messages_ros2.rolling.rcl_interfaces.msg import floating_point_range_pb2 as _floating_point_range_pb2
from make87_messages_ros2.rolling.rcl_interfaces.msg import integer_range_pb2 as _integer_range_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ParameterDescriptor(_message.Message):
    __slots__ = ("name", "type", "description", "additional_constraints", "read_only", "dynamic_typing", "floating_point_range", "integer_range")
    NAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    ADDITIONAL_CONSTRAINTS_FIELD_NUMBER: _ClassVar[int]
    READ_ONLY_FIELD_NUMBER: _ClassVar[int]
    DYNAMIC_TYPING_FIELD_NUMBER: _ClassVar[int]
    FLOATING_POINT_RANGE_FIELD_NUMBER: _ClassVar[int]
    INTEGER_RANGE_FIELD_NUMBER: _ClassVar[int]
    name: str
    type: int
    description: str
    additional_constraints: str
    read_only: bool
    dynamic_typing: bool
    floating_point_range: _containers.RepeatedCompositeFieldContainer[_floating_point_range_pb2.FloatingPointRange]
    integer_range: _containers.RepeatedCompositeFieldContainer[_integer_range_pb2.IntegerRange]
    def __init__(self, name: _Optional[str] = ..., type: _Optional[int] = ..., description: _Optional[str] = ..., additional_constraints: _Optional[str] = ..., read_only: bool = ..., dynamic_typing: bool = ..., floating_point_range: _Optional[_Iterable[_Union[_floating_point_range_pb2.FloatingPointRange, _Mapping]]] = ..., integer_range: _Optional[_Iterable[_Union[_integer_range_pb2.IntegerRange, _Mapping]]] = ...) -> None: ...
