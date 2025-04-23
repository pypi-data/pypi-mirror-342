from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.diagnostic_msgs.msg import key_value_pb2 as _key_value_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CalculateWhiteBalanceRequest(_message.Message):
    __slots__ = ("header",)
    HEADER_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ...) -> None: ...

class CalculateWhiteBalanceResponse(_message.Message):
    __slots__ = ("header", "is_successful", "balance_ratios")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    IS_SUCCESSFUL_FIELD_NUMBER: _ClassVar[int]
    BALANCE_RATIOS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    is_successful: bool
    balance_ratios: _containers.RepeatedCompositeFieldContainer[_key_value_pb2.KeyValue]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., is_successful: bool = ..., balance_ratios: _Optional[_Iterable[_Union[_key_value_pb2.KeyValue, _Mapping]]] = ...) -> None: ...
