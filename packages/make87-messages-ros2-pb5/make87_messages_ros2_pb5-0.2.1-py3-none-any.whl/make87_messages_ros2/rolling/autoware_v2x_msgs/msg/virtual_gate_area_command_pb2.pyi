from make87_messages_ros2.rolling.builtin_interfaces.msg import time_pb2 as _time_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class VirtualGateAreaCommand(_message.Message):
    __slots__ = ("command", "sequence_id", "area_id", "gate_ids", "expected_time_arrival")
    COMMAND_FIELD_NUMBER: _ClassVar[int]
    SEQUENCE_ID_FIELD_NUMBER: _ClassVar[int]
    AREA_ID_FIELD_NUMBER: _ClassVar[int]
    GATE_IDS_FIELD_NUMBER: _ClassVar[int]
    EXPECTED_TIME_ARRIVAL_FIELD_NUMBER: _ClassVar[int]
    command: int
    sequence_id: int
    area_id: str
    gate_ids: _containers.RepeatedScalarFieldContainer[str]
    expected_time_arrival: _containers.RepeatedCompositeFieldContainer[_time_pb2.Time]
    def __init__(self, command: _Optional[int] = ..., sequence_id: _Optional[int] = ..., area_id: _Optional[str] = ..., gate_ids: _Optional[_Iterable[str]] = ..., expected_time_arrival: _Optional[_Iterable[_Union[_time_pb2.Time, _Mapping]]] = ...) -> None: ...
