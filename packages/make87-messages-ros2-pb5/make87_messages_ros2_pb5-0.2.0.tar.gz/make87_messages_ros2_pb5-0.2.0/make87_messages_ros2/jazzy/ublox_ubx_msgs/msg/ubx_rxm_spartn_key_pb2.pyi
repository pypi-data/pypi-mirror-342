from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from make87_messages_ros2.jazzy.ublox_ubx_msgs.msg import spartn_key_info_pb2 as _spartn_key_info_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class UBXRxmSpartnKey(_message.Message):
    __slots__ = ("header", "version", "num_keys", "reserved0", "key_info", "key_payload")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    NUM_KEYS_FIELD_NUMBER: _ClassVar[int]
    RESERVED0_FIELD_NUMBER: _ClassVar[int]
    KEY_INFO_FIELD_NUMBER: _ClassVar[int]
    KEY_PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    version: int
    num_keys: int
    reserved0: _containers.RepeatedScalarFieldContainer[int]
    key_info: _containers.RepeatedCompositeFieldContainer[_spartn_key_info_pb2.SpartnKeyInfo]
    key_payload: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., version: _Optional[int] = ..., num_keys: _Optional[int] = ..., reserved0: _Optional[_Iterable[int]] = ..., key_info: _Optional[_Iterable[_Union[_spartn_key_info_pb2.SpartnKeyInfo, _Mapping]]] = ..., key_payload: _Optional[_Iterable[int]] = ...) -> None: ...
