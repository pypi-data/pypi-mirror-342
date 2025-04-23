from make87_messages_ros2.jazzy.geometry_msgs.msg import vector3_pb2 as _vector3_pb2
from make87_messages_ros2.jazzy.geometry_msgs.msg import wrench_pb2 as _wrench_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ContactState(_message.Message):
    __slots__ = ("info", "collision1_name", "collision2_name", "wrenches", "total_wrench", "contact_positions", "contact_normals", "depths")
    INFO_FIELD_NUMBER: _ClassVar[int]
    COLLISION1_NAME_FIELD_NUMBER: _ClassVar[int]
    COLLISION2_NAME_FIELD_NUMBER: _ClassVar[int]
    WRENCHES_FIELD_NUMBER: _ClassVar[int]
    TOTAL_WRENCH_FIELD_NUMBER: _ClassVar[int]
    CONTACT_POSITIONS_FIELD_NUMBER: _ClassVar[int]
    CONTACT_NORMALS_FIELD_NUMBER: _ClassVar[int]
    DEPTHS_FIELD_NUMBER: _ClassVar[int]
    info: str
    collision1_name: str
    collision2_name: str
    wrenches: _containers.RepeatedCompositeFieldContainer[_wrench_pb2.Wrench]
    total_wrench: _wrench_pb2.Wrench
    contact_positions: _containers.RepeatedCompositeFieldContainer[_vector3_pb2.Vector3]
    contact_normals: _containers.RepeatedCompositeFieldContainer[_vector3_pb2.Vector3]
    depths: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, info: _Optional[str] = ..., collision1_name: _Optional[str] = ..., collision2_name: _Optional[str] = ..., wrenches: _Optional[_Iterable[_Union[_wrench_pb2.Wrench, _Mapping]]] = ..., total_wrench: _Optional[_Union[_wrench_pb2.Wrench, _Mapping]] = ..., contact_positions: _Optional[_Iterable[_Union[_vector3_pb2.Vector3, _Mapping]]] = ..., contact_normals: _Optional[_Iterable[_Union[_vector3_pb2.Vector3, _Mapping]]] = ..., depths: _Optional[_Iterable[float]] = ...) -> None: ...
