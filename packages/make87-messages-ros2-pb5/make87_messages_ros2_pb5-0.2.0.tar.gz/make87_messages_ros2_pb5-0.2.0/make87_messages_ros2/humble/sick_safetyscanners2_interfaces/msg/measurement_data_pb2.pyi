from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.sick_safetyscanners2_interfaces.msg import scan_point_pb2 as _scan_point_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MeasurementData(_message.Message):
    __slots__ = ("header", "number_of_beams", "scan_points")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    NUMBER_OF_BEAMS_FIELD_NUMBER: _ClassVar[int]
    SCAN_POINTS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    number_of_beams: int
    scan_points: _containers.RepeatedCompositeFieldContainer[_scan_point_pb2.ScanPoint]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., number_of_beams: _Optional[int] = ..., scan_points: _Optional[_Iterable[_Union[_scan_point_pb2.ScanPoint, _Mapping]]] = ...) -> None: ...
