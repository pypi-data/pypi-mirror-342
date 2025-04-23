from make87_messages_ros2.rolling.tuw_object_map_msgs.msg import geo_json_geometry_pb2 as _geo_json_geometry_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GeoJSONFeature(_message.Message):
    __slots__ = ("type", "geometry")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    GEOMETRY_FIELD_NUMBER: _ClassVar[int]
    type: str
    geometry: _geo_json_geometry_pb2.GeoJSONGeometry
    def __init__(self, type: _Optional[str] = ..., geometry: _Optional[_Union[_geo_json_geometry_pb2.GeoJSONGeometry, _Mapping]] = ...) -> None: ...
