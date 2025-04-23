from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.novatel_gps_msgs.msg import novatel_receiver_status_pb2 as _novatel_receiver_status_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class NovatelMessageHeader(_message.Message):
    __slots__ = ("header", "message_name", "port", "sequence_num", "percent_idle_time", "gps_time_status", "gps_week_num", "gps_seconds", "receiver_status", "receiver_software_version")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_NAME_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    SEQUENCE_NUM_FIELD_NUMBER: _ClassVar[int]
    PERCENT_IDLE_TIME_FIELD_NUMBER: _ClassVar[int]
    GPS_TIME_STATUS_FIELD_NUMBER: _ClassVar[int]
    GPS_WEEK_NUM_FIELD_NUMBER: _ClassVar[int]
    GPS_SECONDS_FIELD_NUMBER: _ClassVar[int]
    RECEIVER_STATUS_FIELD_NUMBER: _ClassVar[int]
    RECEIVER_SOFTWARE_VERSION_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    message_name: str
    port: str
    sequence_num: int
    percent_idle_time: float
    gps_time_status: str
    gps_week_num: int
    gps_seconds: float
    receiver_status: _novatel_receiver_status_pb2.NovatelReceiverStatus
    receiver_software_version: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., message_name: _Optional[str] = ..., port: _Optional[str] = ..., sequence_num: _Optional[int] = ..., percent_idle_time: _Optional[float] = ..., gps_time_status: _Optional[str] = ..., gps_week_num: _Optional[int] = ..., gps_seconds: _Optional[float] = ..., receiver_status: _Optional[_Union[_novatel_receiver_status_pb2.NovatelReceiverStatus, _Mapping]] = ..., receiver_software_version: _Optional[int] = ...) -> None: ...
