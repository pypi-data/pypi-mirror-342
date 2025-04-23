from make87_messages_ros2.rolling.ros_gz_interfaces.msg import entity_factory_pb2 as _entity_factory_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SpawnEntityRequest(_message.Message):
    __slots__ = ("entity_factory",)
    ENTITY_FACTORY_FIELD_NUMBER: _ClassVar[int]
    entity_factory: _entity_factory_pb2.EntityFactory
    def __init__(self, entity_factory: _Optional[_Union[_entity_factory_pb2.EntityFactory, _Mapping]] = ...) -> None: ...

class SpawnEntityResponse(_message.Message):
    __slots__ = ("success",)
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...
