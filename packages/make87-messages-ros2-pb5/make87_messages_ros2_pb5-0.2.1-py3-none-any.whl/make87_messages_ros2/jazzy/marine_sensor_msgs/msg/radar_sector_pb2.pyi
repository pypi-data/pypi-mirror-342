from make87_messages_ros2.jazzy.builtin_interfaces.msg import duration_pb2 as _duration_pb2
from make87_messages_ros2.jazzy.marine_sensor_msgs.msg import radar_echo_pb2 as _radar_echo_pb2
from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RadarSector(_message.Message):
    __slots__ = ("header", "angle_start", "angle_increment", "time_increment", "scan_time", "range_min", "range_max", "intensities")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ANGLE_START_FIELD_NUMBER: _ClassVar[int]
    ANGLE_INCREMENT_FIELD_NUMBER: _ClassVar[int]
    TIME_INCREMENT_FIELD_NUMBER: _ClassVar[int]
    SCAN_TIME_FIELD_NUMBER: _ClassVar[int]
    RANGE_MIN_FIELD_NUMBER: _ClassVar[int]
    RANGE_MAX_FIELD_NUMBER: _ClassVar[int]
    INTENSITIES_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    angle_start: float
    angle_increment: float
    time_increment: _duration_pb2.Duration
    scan_time: _duration_pb2.Duration
    range_min: float
    range_max: float
    intensities: _containers.RepeatedCompositeFieldContainer[_radar_echo_pb2.RadarEcho]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., angle_start: _Optional[float] = ..., angle_increment: _Optional[float] = ..., time_increment: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ..., scan_time: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ..., range_min: _Optional[float] = ..., range_max: _Optional[float] = ..., intensities: _Optional[_Iterable[_Union[_radar_echo_pb2.RadarEcho, _Mapping]]] = ...) -> None: ...
