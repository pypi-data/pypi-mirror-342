from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.situational_graphs_reasoning_msgs.msg import attribute_pb2 as _attribute_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Node(_message.Message):
    __slots__ = ("header", "id", "type", "attributes")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    id: int
    type: str
    attributes: _containers.RepeatedCompositeFieldContainer[_attribute_pb2.Attribute]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., id: _Optional[int] = ..., type: _Optional[str] = ..., attributes: _Optional[_Iterable[_Union[_attribute_pb2.Attribute, _Mapping]]] = ...) -> None: ...
