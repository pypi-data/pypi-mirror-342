from make87_messages_ros2.jazzy.type_description_interfaces.msg import key_value_pb2 as _key_value_pb2
from make87_messages_ros2.jazzy.type_description_interfaces.msg import type_description_pb2 as _type_description_pb2
from make87_messages_ros2.jazzy.type_description_interfaces.msg import type_source_pb2 as _type_source_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetTypeDescriptionRequest(_message.Message):
    __slots__ = ("type_name", "type_hash", "include_type_sources")
    TYPE_NAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_HASH_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_TYPE_SOURCES_FIELD_NUMBER: _ClassVar[int]
    type_name: str
    type_hash: str
    include_type_sources: bool
    def __init__(self, type_name: _Optional[str] = ..., type_hash: _Optional[str] = ..., include_type_sources: bool = ...) -> None: ...

class GetTypeDescriptionResponse(_message.Message):
    __slots__ = ("successful", "failure_reason", "type_description", "type_sources", "extra_information")
    SUCCESSFUL_FIELD_NUMBER: _ClassVar[int]
    FAILURE_REASON_FIELD_NUMBER: _ClassVar[int]
    TYPE_DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    TYPE_SOURCES_FIELD_NUMBER: _ClassVar[int]
    EXTRA_INFORMATION_FIELD_NUMBER: _ClassVar[int]
    successful: bool
    failure_reason: str
    type_description: _type_description_pb2.TypeDescription
    type_sources: _containers.RepeatedCompositeFieldContainer[_type_source_pb2.TypeSource]
    extra_information: _containers.RepeatedCompositeFieldContainer[_key_value_pb2.KeyValue]
    def __init__(self, successful: bool = ..., failure_reason: _Optional[str] = ..., type_description: _Optional[_Union[_type_description_pb2.TypeDescription, _Mapping]] = ..., type_sources: _Optional[_Iterable[_Union[_type_source_pb2.TypeSource, _Mapping]]] = ..., extra_information: _Optional[_Iterable[_Union[_key_value_pb2.KeyValue, _Mapping]]] = ...) -> None: ...
