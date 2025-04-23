from make87_messages_ros2.jazzy.septentrio_gnss_driver.msg import block_header_pb2 as _block_header_pb2
from make87_messages_ros2.jazzy.septentrio_gnss_driver.msg import vector_info_cart_pb2 as _vector_info_cart_pb2
from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BaseVectorCart(_message.Message):
    __slots__ = ("header", "block_header", "n", "sb_length", "vector_info_cart")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    BLOCK_HEADER_FIELD_NUMBER: _ClassVar[int]
    N_FIELD_NUMBER: _ClassVar[int]
    SB_LENGTH_FIELD_NUMBER: _ClassVar[int]
    VECTOR_INFO_CART_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    block_header: _block_header_pb2.BlockHeader
    n: int
    sb_length: int
    vector_info_cart: _containers.RepeatedCompositeFieldContainer[_vector_info_cart_pb2.VectorInfoCart]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., block_header: _Optional[_Union[_block_header_pb2.BlockHeader, _Mapping]] = ..., n: _Optional[int] = ..., sb_length: _Optional[int] = ..., vector_info_cart: _Optional[_Iterable[_Union[_vector_info_cart_pb2.VectorInfoCart, _Mapping]]] = ...) -> None: ...
