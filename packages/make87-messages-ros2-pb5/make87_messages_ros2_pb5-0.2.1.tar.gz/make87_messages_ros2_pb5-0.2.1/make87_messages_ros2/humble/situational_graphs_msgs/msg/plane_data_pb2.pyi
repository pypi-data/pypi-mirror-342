from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import vector3_pb2 as _vector3_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PlaneData(_message.Message):
    __slots__ = ("header", "ros2_header", "id", "nx", "ny", "nz", "d", "plane_orientation", "plane_points", "data_source")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    NX_FIELD_NUMBER: _ClassVar[int]
    NY_FIELD_NUMBER: _ClassVar[int]
    NZ_FIELD_NUMBER: _ClassVar[int]
    D_FIELD_NUMBER: _ClassVar[int]
    PLANE_ORIENTATION_FIELD_NUMBER: _ClassVar[int]
    PLANE_POINTS_FIELD_NUMBER: _ClassVar[int]
    DATA_SOURCE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    id: int
    nx: float
    ny: float
    nz: float
    d: float
    plane_orientation: _vector3_pb2.Vector3
    plane_points: _containers.RepeatedCompositeFieldContainer[_vector3_pb2.Vector3]
    data_source: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., id: _Optional[int] = ..., nx: _Optional[float] = ..., ny: _Optional[float] = ..., nz: _Optional[float] = ..., d: _Optional[float] = ..., plane_orientation: _Optional[_Union[_vector3_pb2.Vector3, _Mapping]] = ..., plane_points: _Optional[_Iterable[_Union[_vector3_pb2.Vector3, _Mapping]]] = ..., data_source: _Optional[str] = ...) -> None: ...
