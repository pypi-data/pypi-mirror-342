from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SrrDebug5(_message.Message):
    __slots__ = ("header", "can_tx_align_updates")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    CAN_TX_ALIGN_UPDATES_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    can_tx_align_updates: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., can_tx_align_updates: _Optional[int] = ...) -> None: ...
