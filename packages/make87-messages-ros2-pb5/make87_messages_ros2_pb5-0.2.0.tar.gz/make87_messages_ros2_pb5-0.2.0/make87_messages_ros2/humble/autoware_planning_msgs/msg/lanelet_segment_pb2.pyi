from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.autoware_planning_msgs.msg import lanelet_primitive_pb2 as _lanelet_primitive_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LaneletSegment(_message.Message):
    __slots__ = ("header", "preferred_primitive", "primitives")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    PREFERRED_PRIMITIVE_FIELD_NUMBER: _ClassVar[int]
    PRIMITIVES_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    preferred_primitive: _lanelet_primitive_pb2.LaneletPrimitive
    primitives: _containers.RepeatedCompositeFieldContainer[_lanelet_primitive_pb2.LaneletPrimitive]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., preferred_primitive: _Optional[_Union[_lanelet_primitive_pb2.LaneletPrimitive, _Mapping]] = ..., primitives: _Optional[_Iterable[_Union[_lanelet_primitive_pb2.LaneletPrimitive, _Mapping]]] = ...) -> None: ...
