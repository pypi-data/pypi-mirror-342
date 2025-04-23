from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.marti_common_msgs.msg import service_header_pb2 as _service_header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TestTopicServiceRequest(_message.Message):
    __slots__ = ("header", "srv_header", "request_value")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SRV_HEADER_FIELD_NUMBER: _ClassVar[int]
    REQUEST_VALUE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    srv_header: _service_header_pb2.ServiceHeader
    request_value: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., srv_header: _Optional[_Union[_service_header_pb2.ServiceHeader, _Mapping]] = ..., request_value: _Optional[int] = ...) -> None: ...
