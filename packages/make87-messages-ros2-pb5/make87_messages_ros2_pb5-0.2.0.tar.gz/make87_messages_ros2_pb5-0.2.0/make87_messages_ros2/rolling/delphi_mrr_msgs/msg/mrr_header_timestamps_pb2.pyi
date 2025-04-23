from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MrrHeaderTimestamps(_message.Message):
    __slots__ = ("header", "can_det_time_since_meas", "can_sensor_time_stamp")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    CAN_DET_TIME_SINCE_MEAS_FIELD_NUMBER: _ClassVar[int]
    CAN_SENSOR_TIME_STAMP_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    can_det_time_since_meas: float
    can_sensor_time_stamp: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., can_det_time_since_meas: _Optional[float] = ..., can_sensor_time_stamp: _Optional[float] = ...) -> None: ...
