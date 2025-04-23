from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GPSStatus(_message.Message):
    __slots__ = ("header", "ros2_header", "satellites_used", "satellite_used_prn", "satellites_visible", "satellite_visible_prn", "satellite_visible_z", "satellite_visible_azimuth", "satellite_visible_snr", "status", "motion_source", "orientation_source", "position_source")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    SATELLITES_USED_FIELD_NUMBER: _ClassVar[int]
    SATELLITE_USED_PRN_FIELD_NUMBER: _ClassVar[int]
    SATELLITES_VISIBLE_FIELD_NUMBER: _ClassVar[int]
    SATELLITE_VISIBLE_PRN_FIELD_NUMBER: _ClassVar[int]
    SATELLITE_VISIBLE_Z_FIELD_NUMBER: _ClassVar[int]
    SATELLITE_VISIBLE_AZIMUTH_FIELD_NUMBER: _ClassVar[int]
    SATELLITE_VISIBLE_SNR_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MOTION_SOURCE_FIELD_NUMBER: _ClassVar[int]
    ORIENTATION_SOURCE_FIELD_NUMBER: _ClassVar[int]
    POSITION_SOURCE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    satellites_used: int
    satellite_used_prn: _containers.RepeatedScalarFieldContainer[int]
    satellites_visible: int
    satellite_visible_prn: _containers.RepeatedScalarFieldContainer[int]
    satellite_visible_z: _containers.RepeatedScalarFieldContainer[int]
    satellite_visible_azimuth: _containers.RepeatedScalarFieldContainer[int]
    satellite_visible_snr: _containers.RepeatedScalarFieldContainer[int]
    status: int
    motion_source: int
    orientation_source: int
    position_source: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., satellites_used: _Optional[int] = ..., satellite_used_prn: _Optional[_Iterable[int]] = ..., satellites_visible: _Optional[int] = ..., satellite_visible_prn: _Optional[_Iterable[int]] = ..., satellite_visible_z: _Optional[_Iterable[int]] = ..., satellite_visible_azimuth: _Optional[_Iterable[int]] = ..., satellite_visible_snr: _Optional[_Iterable[int]] = ..., status: _Optional[int] = ..., motion_source: _Optional[int] = ..., orientation_source: _Optional[int] = ..., position_source: _Optional[int] = ...) -> None: ...
