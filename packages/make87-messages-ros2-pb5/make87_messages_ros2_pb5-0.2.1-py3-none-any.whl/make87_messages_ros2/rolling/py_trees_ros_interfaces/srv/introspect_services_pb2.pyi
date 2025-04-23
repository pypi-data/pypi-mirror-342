from make87_messages_ros2.rolling.py_trees_ros_interfaces.msg import service_details_pb2 as _service_details_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class IntrospectServicesRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class IntrospectServicesResponse(_message.Message):
    __slots__ = ("service_details",)
    SERVICE_DETAILS_FIELD_NUMBER: _ClassVar[int]
    service_details: _containers.RepeatedCompositeFieldContainer[_service_details_pb2.ServiceDetails]
    def __init__(self, service_details: _Optional[_Iterable[_Union[_service_details_pb2.ServiceDetails, _Mapping]]] = ...) -> None: ...
