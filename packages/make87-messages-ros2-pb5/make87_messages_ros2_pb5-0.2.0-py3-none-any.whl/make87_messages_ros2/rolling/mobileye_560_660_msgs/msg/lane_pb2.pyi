from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Lane(_message.Message):
    __slots__ = ("header", "lane_curvature", "lane_heading", "construction_area", "pitch_angle", "yaw_angle", "right_ldw_availability", "left_ldw_availability")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    LANE_CURVATURE_FIELD_NUMBER: _ClassVar[int]
    LANE_HEADING_FIELD_NUMBER: _ClassVar[int]
    CONSTRUCTION_AREA_FIELD_NUMBER: _ClassVar[int]
    PITCH_ANGLE_FIELD_NUMBER: _ClassVar[int]
    YAW_ANGLE_FIELD_NUMBER: _ClassVar[int]
    RIGHT_LDW_AVAILABILITY_FIELD_NUMBER: _ClassVar[int]
    LEFT_LDW_AVAILABILITY_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    lane_curvature: float
    lane_heading: float
    construction_area: bool
    pitch_angle: float
    yaw_angle: float
    right_ldw_availability: bool
    left_ldw_availability: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., lane_curvature: _Optional[float] = ..., lane_heading: _Optional[float] = ..., construction_area: bool = ..., pitch_angle: _Optional[float] = ..., yaw_angle: _Optional[float] = ..., right_ldw_availability: bool = ..., left_ldw_availability: bool = ...) -> None: ...
