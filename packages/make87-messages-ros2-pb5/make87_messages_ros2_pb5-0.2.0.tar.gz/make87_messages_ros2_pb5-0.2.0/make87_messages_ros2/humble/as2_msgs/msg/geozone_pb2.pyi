from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import polygon_pb2 as _polygon_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Geozone(_message.Message):
    __slots__ = ("header", "id", "alert", "type", "data_type", "polygon", "z_up", "z_down")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    ALERT_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    DATA_TYPE_FIELD_NUMBER: _ClassVar[int]
    POLYGON_FIELD_NUMBER: _ClassVar[int]
    Z_UP_FIELD_NUMBER: _ClassVar[int]
    Z_DOWN_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    id: int
    alert: int
    type: str
    data_type: str
    polygon: _polygon_pb2.Polygon
    z_up: float
    z_down: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., id: _Optional[int] = ..., alert: _Optional[int] = ..., type: _Optional[str] = ..., data_type: _Optional[str] = ..., polygon: _Optional[_Union[_polygon_pb2.Polygon, _Mapping]] = ..., z_up: _Optional[float] = ..., z_down: _Optional[float] = ...) -> None: ...
