from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.builtin_interfaces.msg import time_pb2 as _time_pb2
from make87_messages_ros2.humble.ibeo_msgs.msg import ibeo_data_header_pb2 as _ibeo_data_header_pb2
from make87_messages_ros2.humble.ibeo_msgs.msg import scan_point2205_pb2 as _scan_point2205_pb2
from make87_messages_ros2.humble.ibeo_msgs.msg import scanner_info2205_pb2 as _scanner_info2205_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ScanData2205(_message.Message):
    __slots__ = ("header", "ros2_header", "ibeo_header", "scan_start_time", "scan_end_time_offset", "fused_scan", "mirror_side", "coordinate_system", "scan_number", "scan_points", "number_of_scanner_infos", "scanner_info_list", "scan_point_list")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    IBEO_HEADER_FIELD_NUMBER: _ClassVar[int]
    SCAN_START_TIME_FIELD_NUMBER: _ClassVar[int]
    SCAN_END_TIME_OFFSET_FIELD_NUMBER: _ClassVar[int]
    FUSED_SCAN_FIELD_NUMBER: _ClassVar[int]
    MIRROR_SIDE_FIELD_NUMBER: _ClassVar[int]
    COORDINATE_SYSTEM_FIELD_NUMBER: _ClassVar[int]
    SCAN_NUMBER_FIELD_NUMBER: _ClassVar[int]
    SCAN_POINTS_FIELD_NUMBER: _ClassVar[int]
    NUMBER_OF_SCANNER_INFOS_FIELD_NUMBER: _ClassVar[int]
    SCANNER_INFO_LIST_FIELD_NUMBER: _ClassVar[int]
    SCAN_POINT_LIST_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    ibeo_header: _ibeo_data_header_pb2.IbeoDataHeader
    scan_start_time: _time_pb2.Time
    scan_end_time_offset: int
    fused_scan: bool
    mirror_side: int
    coordinate_system: int
    scan_number: int
    scan_points: int
    number_of_scanner_infos: int
    scanner_info_list: _containers.RepeatedCompositeFieldContainer[_scanner_info2205_pb2.ScannerInfo2205]
    scan_point_list: _containers.RepeatedCompositeFieldContainer[_scan_point2205_pb2.ScanPoint2205]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., ibeo_header: _Optional[_Union[_ibeo_data_header_pb2.IbeoDataHeader, _Mapping]] = ..., scan_start_time: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., scan_end_time_offset: _Optional[int] = ..., fused_scan: bool = ..., mirror_side: _Optional[int] = ..., coordinate_system: _Optional[int] = ..., scan_number: _Optional[int] = ..., scan_points: _Optional[int] = ..., number_of_scanner_infos: _Optional[int] = ..., scanner_info_list: _Optional[_Iterable[_Union[_scanner_info2205_pb2.ScannerInfo2205, _Mapping]]] = ..., scan_point_list: _Optional[_Iterable[_Union[_scan_point2205_pb2.ScanPoint2205, _Mapping]]] = ...) -> None: ...
