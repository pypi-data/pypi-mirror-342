from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.sensor_msgs.msg import laser_scan_pb2 as _laser_scan_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ExtendedLaserScan(_message.Message):
    __slots__ = ("header", "laser_scan", "reflektor_status", "reflektor_median", "intrusion")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    LASER_SCAN_FIELD_NUMBER: _ClassVar[int]
    REFLEKTOR_STATUS_FIELD_NUMBER: _ClassVar[int]
    REFLEKTOR_MEDIAN_FIELD_NUMBER: _ClassVar[int]
    INTRUSION_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    laser_scan: _laser_scan_pb2.LaserScan
    reflektor_status: _containers.RepeatedScalarFieldContainer[bool]
    reflektor_median: _containers.RepeatedScalarFieldContainer[bool]
    intrusion: _containers.RepeatedScalarFieldContainer[bool]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., laser_scan: _Optional[_Union[_laser_scan_pb2.LaserScan, _Mapping]] = ..., reflektor_status: _Optional[_Iterable[bool]] = ..., reflektor_median: _Optional[_Iterable[bool]] = ..., intrusion: _Optional[_Iterable[bool]] = ...) -> None: ...
