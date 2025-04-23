from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DesiredDestination(_message.Message):
    __slots__ = ("header", "msg_counter", "valid", "latitude", "longitude")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    MSG_COUNTER_FIELD_NUMBER: _ClassVar[int]
    VALID_FIELD_NUMBER: _ClassVar[int]
    LATITUDE_FIELD_NUMBER: _ClassVar[int]
    LONGITUDE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    msg_counter: int
    valid: int
    latitude: float
    longitude: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., msg_counter: _Optional[int] = ..., valid: _Optional[int] = ..., latitude: _Optional[float] = ..., longitude: _Optional[float] = ...) -> None: ...
