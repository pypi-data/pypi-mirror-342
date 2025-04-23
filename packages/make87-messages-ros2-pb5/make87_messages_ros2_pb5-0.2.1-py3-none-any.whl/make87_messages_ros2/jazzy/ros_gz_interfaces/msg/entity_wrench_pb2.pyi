from make87_messages_ros2.jazzy.geometry_msgs.msg import wrench_pb2 as _wrench_pb2
from make87_messages_ros2.jazzy.ros_gz_interfaces.msg import entity_pb2 as _entity_pb2
from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EntityWrench(_message.Message):
    __slots__ = ("header", "entity", "wrench")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ENTITY_FIELD_NUMBER: _ClassVar[int]
    WRENCH_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    entity: _entity_pb2.Entity
    wrench: _wrench_pb2.Wrench
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., entity: _Optional[_Union[_entity_pb2.Entity, _Mapping]] = ..., wrench: _Optional[_Union[_wrench_pb2.Wrench, _Mapping]] = ...) -> None: ...
