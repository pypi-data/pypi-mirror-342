from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.builtin_interfaces.msg import duration_pb2 as _duration_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ChargerRequest(_message.Message):
    __slots__ = ("header", "charger_name", "fleet_name", "robot_name", "start_timeout", "request_id")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    CHARGER_NAME_FIELD_NUMBER: _ClassVar[int]
    FLEET_NAME_FIELD_NUMBER: _ClassVar[int]
    ROBOT_NAME_FIELD_NUMBER: _ClassVar[int]
    START_TIMEOUT_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    charger_name: str
    fleet_name: str
    robot_name: str
    start_timeout: _duration_pb2.Duration
    request_id: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., charger_name: _Optional[str] = ..., fleet_name: _Optional[str] = ..., robot_name: _Optional[str] = ..., start_timeout: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ..., request_id: _Optional[str] = ...) -> None: ...
