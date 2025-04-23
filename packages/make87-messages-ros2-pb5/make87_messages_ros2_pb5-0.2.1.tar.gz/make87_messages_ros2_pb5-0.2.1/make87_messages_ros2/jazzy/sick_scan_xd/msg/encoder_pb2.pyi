from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Encoder(_message.Message):
    __slots__ = ("header", "enc_position", "enc_speed")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ENC_POSITION_FIELD_NUMBER: _ClassVar[int]
    ENC_SPEED_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    enc_position: int
    enc_speed: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., enc_position: _Optional[int] = ..., enc_speed: _Optional[int] = ...) -> None: ...
