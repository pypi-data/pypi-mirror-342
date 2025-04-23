from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.qb_device_msgs.msg import resource_data_pb2 as _resource_data_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class State(_message.Message):
    __slots__ = ("header", "actuators", "joints", "is_reliable", "consecutive_failures")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ACTUATORS_FIELD_NUMBER: _ClassVar[int]
    JOINTS_FIELD_NUMBER: _ClassVar[int]
    IS_RELIABLE_FIELD_NUMBER: _ClassVar[int]
    CONSECUTIVE_FAILURES_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    actuators: _containers.RepeatedCompositeFieldContainer[_resource_data_pb2.ResourceData]
    joints: _containers.RepeatedCompositeFieldContainer[_resource_data_pb2.ResourceData]
    is_reliable: bool
    consecutive_failures: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., actuators: _Optional[_Iterable[_Union[_resource_data_pb2.ResourceData, _Mapping]]] = ..., joints: _Optional[_Iterable[_Union[_resource_data_pb2.ResourceData, _Mapping]]] = ..., is_reliable: bool = ..., consecutive_failures: _Optional[int] = ...) -> None: ...
