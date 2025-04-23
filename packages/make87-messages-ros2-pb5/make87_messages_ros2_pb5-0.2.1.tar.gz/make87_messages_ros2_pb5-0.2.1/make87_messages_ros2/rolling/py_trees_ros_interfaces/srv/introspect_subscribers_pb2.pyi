from make87_messages_ros2.rolling.py_trees_ros_interfaces.msg import subscriber_details_pb2 as _subscriber_details_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class IntrospectSubscribersRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class IntrospectSubscribersResponse(_message.Message):
    __slots__ = ("subscriber_details",)
    SUBSCRIBER_DETAILS_FIELD_NUMBER: _ClassVar[int]
    subscriber_details: _containers.RepeatedCompositeFieldContainer[_subscriber_details_pb2.SubscriberDetails]
    def __init__(self, subscriber_details: _Optional[_Iterable[_Union[_subscriber_details_pb2.SubscriberDetails, _Mapping]]] = ...) -> None: ...
