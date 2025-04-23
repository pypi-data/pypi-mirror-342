from make87_messages_ros2.jazzy.plansys2_msgs.msg import derived_pb2 as _derived_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetDomainDerivedPredicateDetailsRequest(_message.Message):
    __slots__ = ("predicate",)
    PREDICATE_FIELD_NUMBER: _ClassVar[int]
    predicate: str
    def __init__(self, predicate: _Optional[str] = ...) -> None: ...

class GetDomainDerivedPredicateDetailsResponse(_message.Message):
    __slots__ = ("predicates", "success", "error_info")
    PREDICATES_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_INFO_FIELD_NUMBER: _ClassVar[int]
    predicates: _containers.RepeatedCompositeFieldContainer[_derived_pb2.Derived]
    success: bool
    error_info: str
    def __init__(self, predicates: _Optional[_Iterable[_Union[_derived_pb2.Derived, _Mapping]]] = ..., success: bool = ..., error_info: _Optional[str] = ...) -> None: ...
