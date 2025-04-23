from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geographic_msgs.msg import geo_point_pb2 as _geo_point_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class HilGPS(_message.Message):
    __slots__ = ("header", "ros2_header", "fix_type", "geo", "eph", "epv", "vel", "vn", "ve", "vd", "cog", "satellites_visible")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    FIX_TYPE_FIELD_NUMBER: _ClassVar[int]
    GEO_FIELD_NUMBER: _ClassVar[int]
    EPH_FIELD_NUMBER: _ClassVar[int]
    EPV_FIELD_NUMBER: _ClassVar[int]
    VEL_FIELD_NUMBER: _ClassVar[int]
    VN_FIELD_NUMBER: _ClassVar[int]
    VE_FIELD_NUMBER: _ClassVar[int]
    VD_FIELD_NUMBER: _ClassVar[int]
    COG_FIELD_NUMBER: _ClassVar[int]
    SATELLITES_VISIBLE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    fix_type: int
    geo: _geo_point_pb2.GeoPoint
    eph: int
    epv: int
    vel: int
    vn: int
    ve: int
    vd: int
    cog: int
    satellites_visible: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., fix_type: _Optional[int] = ..., geo: _Optional[_Union[_geo_point_pb2.GeoPoint, _Mapping]] = ..., eph: _Optional[int] = ..., epv: _Optional[int] = ..., vel: _Optional[int] = ..., vn: _Optional[int] = ..., ve: _Optional[int] = ..., vd: _Optional[int] = ..., cog: _Optional[int] = ..., satellites_visible: _Optional[int] = ...) -> None: ...
