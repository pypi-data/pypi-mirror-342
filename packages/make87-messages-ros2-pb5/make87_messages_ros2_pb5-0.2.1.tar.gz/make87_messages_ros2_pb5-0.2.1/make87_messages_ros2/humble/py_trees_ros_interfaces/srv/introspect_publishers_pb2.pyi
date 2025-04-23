from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.py_trees_ros_interfaces.msg import publisher_details_pb2 as _publisher_details_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class IntrospectPublishersRequest(_message.Message):
    __slots__ = ("header",)
    HEADER_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ...) -> None: ...

class IntrospectPublishersResponse(_message.Message):
    __slots__ = ("header", "publisher_details")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    PUBLISHER_DETAILS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    publisher_details: _containers.RepeatedCompositeFieldContainer[_publisher_details_pb2.PublisherDetails]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., publisher_details: _Optional[_Iterable[_Union[_publisher_details_pb2.PublisherDetails, _Mapping]]] = ...) -> None: ...
