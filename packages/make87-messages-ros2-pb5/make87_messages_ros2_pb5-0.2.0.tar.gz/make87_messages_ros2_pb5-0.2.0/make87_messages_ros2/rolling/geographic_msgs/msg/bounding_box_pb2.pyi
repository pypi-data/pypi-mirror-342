from make87_messages_ros2.rolling.geographic_msgs.msg import geo_point_pb2 as _geo_point_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BoundingBox(_message.Message):
    __slots__ = ("min_pt", "max_pt")
    MIN_PT_FIELD_NUMBER: _ClassVar[int]
    MAX_PT_FIELD_NUMBER: _ClassVar[int]
    min_pt: _geo_point_pb2.GeoPoint
    max_pt: _geo_point_pb2.GeoPoint
    def __init__(self, min_pt: _Optional[_Union[_geo_point_pb2.GeoPoint, _Mapping]] = ..., max_pt: _Optional[_Union[_geo_point_pb2.GeoPoint, _Mapping]] = ...) -> None: ...
