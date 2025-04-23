from make87_messages_ros2.jazzy.type_description_interfaces.msg import individual_type_description_pb2 as _individual_type_description_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TypeDescription(_message.Message):
    __slots__ = ("type_description", "referenced_type_descriptions")
    TYPE_DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    REFERENCED_TYPE_DESCRIPTIONS_FIELD_NUMBER: _ClassVar[int]
    type_description: _individual_type_description_pb2.IndividualTypeDescription
    referenced_type_descriptions: _containers.RepeatedCompositeFieldContainer[_individual_type_description_pb2.IndividualTypeDescription]
    def __init__(self, type_description: _Optional[_Union[_individual_type_description_pb2.IndividualTypeDescription, _Mapping]] = ..., referenced_type_descriptions: _Optional[_Iterable[_Union[_individual_type_description_pb2.IndividualTypeDescription, _Mapping]]] = ...) -> None: ...
