from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BatteryTraction(_message.Message):
    __slots__ = ("header", "state_of_charge", "voltage", "current", "temperature", "status")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    STATE_OF_CHARGE_FIELD_NUMBER: _ClassVar[int]
    VOLTAGE_FIELD_NUMBER: _ClassVar[int]
    CURRENT_FIELD_NUMBER: _ClassVar[int]
    TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    state_of_charge: float
    voltage: float
    current: float
    temperature: float
    status: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., state_of_charge: _Optional[float] = ..., voltage: _Optional[float] = ..., current: _Optional[float] = ..., temperature: _Optional[float] = ..., status: _Optional[int] = ...) -> None: ...
