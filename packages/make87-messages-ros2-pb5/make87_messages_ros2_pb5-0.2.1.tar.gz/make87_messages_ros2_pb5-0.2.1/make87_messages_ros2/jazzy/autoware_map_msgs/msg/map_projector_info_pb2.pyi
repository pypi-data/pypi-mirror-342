from make87_messages_ros2.jazzy.geographic_msgs.msg import geo_point_pb2 as _geo_point_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MapProjectorInfo(_message.Message):
    __slots__ = ("projector_type", "vertical_datum", "mgrs_grid", "map_origin")
    PROJECTOR_TYPE_FIELD_NUMBER: _ClassVar[int]
    VERTICAL_DATUM_FIELD_NUMBER: _ClassVar[int]
    MGRS_GRID_FIELD_NUMBER: _ClassVar[int]
    MAP_ORIGIN_FIELD_NUMBER: _ClassVar[int]
    projector_type: str
    vertical_datum: str
    mgrs_grid: str
    map_origin: _geo_point_pb2.GeoPoint
    def __init__(self, projector_type: _Optional[str] = ..., vertical_datum: _Optional[str] = ..., mgrs_grid: _Optional[str] = ..., map_origin: _Optional[_Union[_geo_point_pb2.GeoPoint, _Mapping]] = ...) -> None: ...
