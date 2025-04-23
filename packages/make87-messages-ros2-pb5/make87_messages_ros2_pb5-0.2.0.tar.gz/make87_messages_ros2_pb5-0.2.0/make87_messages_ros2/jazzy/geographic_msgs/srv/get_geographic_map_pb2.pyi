from make87_messages_ros2.jazzy.geographic_msgs.msg import bounding_box_pb2 as _bounding_box_pb2
from make87_messages_ros2.jazzy.geographic_msgs.msg import geographic_map_pb2 as _geographic_map_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetGeographicMapRequest(_message.Message):
    __slots__ = ("url", "bounds")
    URL_FIELD_NUMBER: _ClassVar[int]
    BOUNDS_FIELD_NUMBER: _ClassVar[int]
    url: str
    bounds: _bounding_box_pb2.BoundingBox
    def __init__(self, url: _Optional[str] = ..., bounds: _Optional[_Union[_bounding_box_pb2.BoundingBox, _Mapping]] = ...) -> None: ...

class GetGeographicMapResponse(_message.Message):
    __slots__ = ("success", "status", "map")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MAP_FIELD_NUMBER: _ClassVar[int]
    success: bool
    status: str
    map: _geographic_map_pb2.GeographicMap
    def __init__(self, success: bool = ..., status: _Optional[str] = ..., map: _Optional[_Union[_geographic_map_pb2.GeographicMap, _Mapping]] = ...) -> None: ...
