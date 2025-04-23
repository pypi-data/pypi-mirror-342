from make87_messages_ros2.jazzy.geographic_msgs.msg import key_value_pb2 as _key_value_pb2
from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from make87_messages_ros2.jazzy.unique_identifier_msgs.msg import uuid_pb2 as _uuid_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RoutePath(_message.Message):
    __slots__ = ("header", "network", "segments", "props")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    NETWORK_FIELD_NUMBER: _ClassVar[int]
    SEGMENTS_FIELD_NUMBER: _ClassVar[int]
    PROPS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    network: _uuid_pb2.UUID
    segments: _containers.RepeatedCompositeFieldContainer[_uuid_pb2.UUID]
    props: _containers.RepeatedCompositeFieldContainer[_key_value_pb2.KeyValue]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., network: _Optional[_Union[_uuid_pb2.UUID, _Mapping]] = ..., segments: _Optional[_Iterable[_Union[_uuid_pb2.UUID, _Mapping]]] = ..., props: _Optional[_Iterable[_Union[_key_value_pb2.KeyValue, _Mapping]]] = ...) -> None: ...
