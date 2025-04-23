from make87_messages_ros2.jazzy.novatel_gps_msgs.msg import novatel_message_header_pb2 as _novatel_message_header_pb2
from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class NovatelCorrectedImuData(_message.Message):
    __slots__ = ("header", "novatel_msg_header", "gps_week_num", "gps_seconds", "pitch_rate", "roll_rate", "yaw_rate", "lateral_acceleration", "longitudinal_acceleration", "vertical_acceleration")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    NOVATEL_MSG_HEADER_FIELD_NUMBER: _ClassVar[int]
    GPS_WEEK_NUM_FIELD_NUMBER: _ClassVar[int]
    GPS_SECONDS_FIELD_NUMBER: _ClassVar[int]
    PITCH_RATE_FIELD_NUMBER: _ClassVar[int]
    ROLL_RATE_FIELD_NUMBER: _ClassVar[int]
    YAW_RATE_FIELD_NUMBER: _ClassVar[int]
    LATERAL_ACCELERATION_FIELD_NUMBER: _ClassVar[int]
    LONGITUDINAL_ACCELERATION_FIELD_NUMBER: _ClassVar[int]
    VERTICAL_ACCELERATION_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    novatel_msg_header: _novatel_message_header_pb2.NovatelMessageHeader
    gps_week_num: int
    gps_seconds: float
    pitch_rate: float
    roll_rate: float
    yaw_rate: float
    lateral_acceleration: float
    longitudinal_acceleration: float
    vertical_acceleration: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., novatel_msg_header: _Optional[_Union[_novatel_message_header_pb2.NovatelMessageHeader, _Mapping]] = ..., gps_week_num: _Optional[int] = ..., gps_seconds: _Optional[float] = ..., pitch_rate: _Optional[float] = ..., roll_rate: _Optional[float] = ..., yaw_rate: _Optional[float] = ..., lateral_acceleration: _Optional[float] = ..., longitudinal_acceleration: _Optional[float] = ..., vertical_acceleration: _Optional[float] = ...) -> None: ...
