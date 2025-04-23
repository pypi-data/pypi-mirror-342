from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.builtin_interfaces.msg import time_pb2 as _time_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class IbeoDataHeader(_message.Message):
    __slots__ = ("header", "previous_message_size", "message_size", "device_id", "data_type_id", "stamp")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    PREVIOUS_MESSAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    DEVICE_ID_FIELD_NUMBER: _ClassVar[int]
    DATA_TYPE_ID_FIELD_NUMBER: _ClassVar[int]
    STAMP_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    previous_message_size: int
    message_size: int
    device_id: int
    data_type_id: int
    stamp: _time_pb2.Time
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., previous_message_size: _Optional[int] = ..., message_size: _Optional[int] = ..., device_id: _Optional[int] = ..., data_type_id: _Optional[int] = ..., stamp: _Optional[_Union[_time_pb2.Time, _Mapping]] = ...) -> None: ...
