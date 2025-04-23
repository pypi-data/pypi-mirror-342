from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.septentrio_gnss_driver.msg import block_header_pb2 as _block_header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ReceiverTime(_message.Message):
    __slots__ = ("header", "ros2_header", "block_header", "utc_year", "utc_month", "utc_day", "utc_hour", "utc_min", "utc_second", "delta_ls", "sync_level")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    BLOCK_HEADER_FIELD_NUMBER: _ClassVar[int]
    UTC_YEAR_FIELD_NUMBER: _ClassVar[int]
    UTC_MONTH_FIELD_NUMBER: _ClassVar[int]
    UTC_DAY_FIELD_NUMBER: _ClassVar[int]
    UTC_HOUR_FIELD_NUMBER: _ClassVar[int]
    UTC_MIN_FIELD_NUMBER: _ClassVar[int]
    UTC_SECOND_FIELD_NUMBER: _ClassVar[int]
    DELTA_LS_FIELD_NUMBER: _ClassVar[int]
    SYNC_LEVEL_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    block_header: _block_header_pb2.BlockHeader
    utc_year: int
    utc_month: int
    utc_day: int
    utc_hour: int
    utc_min: int
    utc_second: int
    delta_ls: int
    sync_level: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., block_header: _Optional[_Union[_block_header_pb2.BlockHeader, _Mapping]] = ..., utc_year: _Optional[int] = ..., utc_month: _Optional[int] = ..., utc_day: _Optional[int] = ..., utc_hour: _Optional[int] = ..., utc_min: _Optional[int] = ..., utc_second: _Optional[int] = ..., delta_ls: _Optional[int] = ..., sync_level: _Optional[int] = ...) -> None: ...
