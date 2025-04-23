from make87_messages_ros2.rolling.autoware_v2x_msgs.msg import virtual_gate_area_command_pb2 as _virtual_gate_area_command_pb2
from make87_messages_ros2.rolling.builtin_interfaces.msg import time_pb2 as _time_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class VirtualGateCommand(_message.Message):
    __slots__ = ("stamp", "areas")
    STAMP_FIELD_NUMBER: _ClassVar[int]
    AREAS_FIELD_NUMBER: _ClassVar[int]
    stamp: _time_pb2.Time
    areas: _containers.RepeatedCompositeFieldContainer[_virtual_gate_area_command_pb2.VirtualGateAreaCommand]
    def __init__(self, stamp: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., areas: _Optional[_Iterable[_Union[_virtual_gate_area_command_pb2.VirtualGateAreaCommand, _Mapping]]] = ...) -> None: ...
