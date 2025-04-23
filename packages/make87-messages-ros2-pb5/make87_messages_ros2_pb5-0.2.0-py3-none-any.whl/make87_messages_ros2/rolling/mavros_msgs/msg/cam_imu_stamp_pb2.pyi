from make87_messages_ros2.rolling.builtin_interfaces.msg import time_pb2 as _time_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CamIMUStamp(_message.Message):
    __slots__ = ("frame_stamp", "frame_seq_id")
    FRAME_STAMP_FIELD_NUMBER: _ClassVar[int]
    FRAME_SEQ_ID_FIELD_NUMBER: _ClassVar[int]
    frame_stamp: _time_pb2.Time
    frame_seq_id: int
    def __init__(self, frame_stamp: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., frame_seq_id: _Optional[int] = ...) -> None: ...
