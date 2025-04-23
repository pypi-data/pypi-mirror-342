from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.builtin_interfaces.msg import time_pb2 as _time_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ClientControlMode(_message.Message):
    __slots__ = ("header", "stamp", "visual_recording_state", "map_state", "localization_state", "recording_state", "alignment_state", "mask_state", "expandmap_state")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    STAMP_FIELD_NUMBER: _ClassVar[int]
    VISUAL_RECORDING_STATE_FIELD_NUMBER: _ClassVar[int]
    MAP_STATE_FIELD_NUMBER: _ClassVar[int]
    LOCALIZATION_STATE_FIELD_NUMBER: _ClassVar[int]
    RECORDING_STATE_FIELD_NUMBER: _ClassVar[int]
    ALIGNMENT_STATE_FIELD_NUMBER: _ClassVar[int]
    MASK_STATE_FIELD_NUMBER: _ClassVar[int]
    EXPANDMAP_STATE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    stamp: _time_pb2.Time
    visual_recording_state: int
    map_state: int
    localization_state: int
    recording_state: int
    alignment_state: int
    mask_state: int
    expandmap_state: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., stamp: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., visual_recording_state: _Optional[int] = ..., map_state: _Optional[int] = ..., localization_state: _Optional[int] = ..., recording_state: _Optional[int] = ..., alignment_state: _Optional[int] = ..., mask_state: _Optional[int] = ..., expandmap_state: _Optional[int] = ...) -> None: ...
