from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ESCTelemetryItem(_message.Message):
    __slots__ = ("header", "temperature", "voltage", "current", "totalcurrent", "rpm", "count")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    VOLTAGE_FIELD_NUMBER: _ClassVar[int]
    CURRENT_FIELD_NUMBER: _ClassVar[int]
    TOTALCURRENT_FIELD_NUMBER: _ClassVar[int]
    RPM_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    temperature: float
    voltage: float
    current: float
    totalcurrent: float
    rpm: int
    count: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., temperature: _Optional[float] = ..., voltage: _Optional[float] = ..., current: _Optional[float] = ..., totalcurrent: _Optional[float] = ..., rpm: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...
