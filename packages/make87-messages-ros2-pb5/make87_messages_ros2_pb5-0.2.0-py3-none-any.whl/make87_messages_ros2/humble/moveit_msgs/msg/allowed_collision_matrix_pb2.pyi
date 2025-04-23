from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.moveit_msgs.msg import allowed_collision_entry_pb2 as _allowed_collision_entry_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AllowedCollisionMatrix(_message.Message):
    __slots__ = ("header", "entry_names", "entry_values", "default_entry_names", "default_entry_values")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ENTRY_NAMES_FIELD_NUMBER: _ClassVar[int]
    ENTRY_VALUES_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_ENTRY_NAMES_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_ENTRY_VALUES_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    entry_names: _containers.RepeatedScalarFieldContainer[str]
    entry_values: _containers.RepeatedCompositeFieldContainer[_allowed_collision_entry_pb2.AllowedCollisionEntry]
    default_entry_names: _containers.RepeatedScalarFieldContainer[str]
    default_entry_values: _containers.RepeatedScalarFieldContainer[bool]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., entry_names: _Optional[_Iterable[str]] = ..., entry_values: _Optional[_Iterable[_Union[_allowed_collision_entry_pb2.AllowedCollisionEntry, _Mapping]]] = ..., default_entry_names: _Optional[_Iterable[str]] = ..., default_entry_values: _Optional[_Iterable[bool]] = ...) -> None: ...
