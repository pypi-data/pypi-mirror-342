from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.cartographer_ros_msgs.msg import status_response_pb2 as _status_response_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class WriteStateRequest(_message.Message):
    __slots__ = ("header", "filename", "include_unfinished_submaps")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_UNFINISHED_SUBMAPS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    filename: str
    include_unfinished_submaps: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., filename: _Optional[str] = ..., include_unfinished_submaps: bool = ...) -> None: ...

class WriteStateResponse(_message.Message):
    __slots__ = ("header", "status")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    status: _status_response_pb2.StatusResponse
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., status: _Optional[_Union[_status_response_pb2.StatusResponse, _Mapping]] = ...) -> None: ...
