from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import empty_pb2 as _empty_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ClearCostmapAroundRobotRequest(_message.Message):
    __slots__ = ("header", "reset_distance")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    RESET_DISTANCE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    reset_distance: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., reset_distance: _Optional[float] = ...) -> None: ...

class ClearCostmapAroundRobotResponse(_message.Message):
    __slots__ = ("header", "response")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    response: _empty_pb2.Empty
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., response: _Optional[_Union[_empty_pb2.Empty, _Mapping]] = ...) -> None: ...
