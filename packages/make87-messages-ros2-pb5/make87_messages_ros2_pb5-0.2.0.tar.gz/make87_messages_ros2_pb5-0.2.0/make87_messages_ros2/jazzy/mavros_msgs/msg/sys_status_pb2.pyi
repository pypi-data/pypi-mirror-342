from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SysStatus(_message.Message):
    __slots__ = ("header", "sensors_present", "sensors_enabled", "sensors_health", "load", "voltage_battery", "current_battery", "battery_remaining", "drop_rate_comm", "errors_comm", "errors_count1", "errors_count2", "errors_count3", "errors_count4")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SENSORS_PRESENT_FIELD_NUMBER: _ClassVar[int]
    SENSORS_ENABLED_FIELD_NUMBER: _ClassVar[int]
    SENSORS_HEALTH_FIELD_NUMBER: _ClassVar[int]
    LOAD_FIELD_NUMBER: _ClassVar[int]
    VOLTAGE_BATTERY_FIELD_NUMBER: _ClassVar[int]
    CURRENT_BATTERY_FIELD_NUMBER: _ClassVar[int]
    BATTERY_REMAINING_FIELD_NUMBER: _ClassVar[int]
    DROP_RATE_COMM_FIELD_NUMBER: _ClassVar[int]
    ERRORS_COMM_FIELD_NUMBER: _ClassVar[int]
    ERRORS_COUNT1_FIELD_NUMBER: _ClassVar[int]
    ERRORS_COUNT2_FIELD_NUMBER: _ClassVar[int]
    ERRORS_COUNT3_FIELD_NUMBER: _ClassVar[int]
    ERRORS_COUNT4_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    sensors_present: int
    sensors_enabled: int
    sensors_health: int
    load: int
    voltage_battery: int
    current_battery: int
    battery_remaining: int
    drop_rate_comm: int
    errors_comm: int
    errors_count1: int
    errors_count2: int
    errors_count3: int
    errors_count4: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., sensors_present: _Optional[int] = ..., sensors_enabled: _Optional[int] = ..., sensors_health: _Optional[int] = ..., load: _Optional[int] = ..., voltage_battery: _Optional[int] = ..., current_battery: _Optional[int] = ..., battery_remaining: _Optional[int] = ..., drop_rate_comm: _Optional[int] = ..., errors_comm: _Optional[int] = ..., errors_count1: _Optional[int] = ..., errors_count2: _Optional[int] = ..., errors_count3: _Optional[int] = ..., errors_count4: _Optional[int] = ...) -> None: ...
