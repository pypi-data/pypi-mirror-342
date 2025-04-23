from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.sensor_msgs.msg import point_field_pb2 as _point_field_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CompressedPointCloud2(_message.Message):
    __slots__ = ("header", "ros2_header", "height", "width", "fields", "is_bigendian", "point_step", "row_step", "compressed_data", "is_dense", "format")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    FIELDS_FIELD_NUMBER: _ClassVar[int]
    IS_BIGENDIAN_FIELD_NUMBER: _ClassVar[int]
    POINT_STEP_FIELD_NUMBER: _ClassVar[int]
    ROW_STEP_FIELD_NUMBER: _ClassVar[int]
    COMPRESSED_DATA_FIELD_NUMBER: _ClassVar[int]
    IS_DENSE_FIELD_NUMBER: _ClassVar[int]
    FORMAT_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    height: int
    width: int
    fields: _containers.RepeatedCompositeFieldContainer[_point_field_pb2.PointField]
    is_bigendian: bool
    point_step: int
    row_step: int
    compressed_data: _containers.RepeatedScalarFieldContainer[int]
    is_dense: bool
    format: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., height: _Optional[int] = ..., width: _Optional[int] = ..., fields: _Optional[_Iterable[_Union[_point_field_pb2.PointField, _Mapping]]] = ..., is_bigendian: bool = ..., point_step: _Optional[int] = ..., row_step: _Optional[int] = ..., compressed_data: _Optional[_Iterable[int]] = ..., is_dense: bool = ..., format: _Optional[str] = ...) -> None: ...
