from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.sensor_msgs.msg import point_cloud2_pb2 as _point_cloud2_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetPointMapROIRequest(_message.Message):
    __slots__ = ("header", "x", "y", "z", "r", "l_x", "l_y", "l_z")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    Z_FIELD_NUMBER: _ClassVar[int]
    R_FIELD_NUMBER: _ClassVar[int]
    L_X_FIELD_NUMBER: _ClassVar[int]
    L_Y_FIELD_NUMBER: _ClassVar[int]
    L_Z_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    x: float
    y: float
    z: float
    r: float
    l_x: float
    l_y: float
    l_z: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., x: _Optional[float] = ..., y: _Optional[float] = ..., z: _Optional[float] = ..., r: _Optional[float] = ..., l_x: _Optional[float] = ..., l_y: _Optional[float] = ..., l_z: _Optional[float] = ...) -> None: ...

class GetPointMapROIResponse(_message.Message):
    __slots__ = ("header", "sub_map")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUB_MAP_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    sub_map: _point_cloud2_pb2.PointCloud2
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., sub_map: _Optional[_Union[_point_cloud2_pb2.PointCloud2, _Mapping]] = ...) -> None: ...
