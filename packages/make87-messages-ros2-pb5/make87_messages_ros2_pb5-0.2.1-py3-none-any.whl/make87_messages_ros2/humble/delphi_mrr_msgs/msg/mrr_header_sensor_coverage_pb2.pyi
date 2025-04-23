from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MrrHeaderSensorCoverage(_message.Message):
    __slots__ = ("header", "ros2_header", "can_sensor_fov_hor", "can_doppler_coverage", "can_range_coverage")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    CAN_SENSOR_FOV_HOR_FIELD_NUMBER: _ClassVar[int]
    CAN_DOPPLER_COVERAGE_FIELD_NUMBER: _ClassVar[int]
    CAN_RANGE_COVERAGE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    can_sensor_fov_hor: int
    can_doppler_coverage: int
    can_range_coverage: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., can_sensor_fov_hor: _Optional[int] = ..., can_doppler_coverage: _Optional[int] = ..., can_range_coverage: _Optional[int] = ...) -> None: ...
