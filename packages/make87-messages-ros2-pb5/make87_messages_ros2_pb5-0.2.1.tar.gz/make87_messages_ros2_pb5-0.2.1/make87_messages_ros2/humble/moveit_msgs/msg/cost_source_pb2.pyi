from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import vector3_pb2 as _vector3_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CostSource(_message.Message):
    __slots__ = ("header", "cost_density", "aabb_min", "aabb_max")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    COST_DENSITY_FIELD_NUMBER: _ClassVar[int]
    AABB_MIN_FIELD_NUMBER: _ClassVar[int]
    AABB_MAX_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    cost_density: float
    aabb_min: _vector3_pb2.Vector3
    aabb_max: _vector3_pb2.Vector3
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., cost_density: _Optional[float] = ..., aabb_min: _Optional[_Union[_vector3_pb2.Vector3, _Mapping]] = ..., aabb_max: _Optional[_Union[_vector3_pb2.Vector3, _Mapping]] = ...) -> None: ...
