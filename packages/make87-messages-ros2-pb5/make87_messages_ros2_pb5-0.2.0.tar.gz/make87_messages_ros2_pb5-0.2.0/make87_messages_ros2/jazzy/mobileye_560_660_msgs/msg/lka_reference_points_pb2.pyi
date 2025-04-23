from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LkaReferencePoints(_message.Message):
    __slots__ = ("header", "ref_point_1_position", "ref_point_1_distance", "ref_point_1_validity", "ref_point_2_position", "ref_point_2_distance", "ref_point_2_validity")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    REF_POINT_1_POSITION_FIELD_NUMBER: _ClassVar[int]
    REF_POINT_1_DISTANCE_FIELD_NUMBER: _ClassVar[int]
    REF_POINT_1_VALIDITY_FIELD_NUMBER: _ClassVar[int]
    REF_POINT_2_POSITION_FIELD_NUMBER: _ClassVar[int]
    REF_POINT_2_DISTANCE_FIELD_NUMBER: _ClassVar[int]
    REF_POINT_2_VALIDITY_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ref_point_1_position: float
    ref_point_1_distance: float
    ref_point_1_validity: bool
    ref_point_2_position: float
    ref_point_2_distance: float
    ref_point_2_validity: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ref_point_1_position: _Optional[float] = ..., ref_point_1_distance: _Optional[float] = ..., ref_point_1_validity: bool = ..., ref_point_2_position: _Optional[float] = ..., ref_point_2_distance: _Optional[float] = ..., ref_point_2_validity: bool = ...) -> None: ...
