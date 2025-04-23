from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from make87_messages_ros2.rolling.ublox_ubx_msgs.msg import comms_port_info_pb2 as _comms_port_info_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class UBXMonComms(_message.Message):
    __slots__ = ("header", "version", "n_ports", "tx_errors", "reserved0", "prot_ids", "ports")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    N_PORTS_FIELD_NUMBER: _ClassVar[int]
    TX_ERRORS_FIELD_NUMBER: _ClassVar[int]
    RESERVED0_FIELD_NUMBER: _ClassVar[int]
    PROT_IDS_FIELD_NUMBER: _ClassVar[int]
    PORTS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    version: int
    n_ports: int
    tx_errors: int
    reserved0: int
    prot_ids: _containers.RepeatedScalarFieldContainer[int]
    ports: _containers.RepeatedCompositeFieldContainer[_comms_port_info_pb2.CommsPortInfo]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., version: _Optional[int] = ..., n_ports: _Optional[int] = ..., tx_errors: _Optional[int] = ..., reserved0: _Optional[int] = ..., prot_ids: _Optional[_Iterable[int]] = ..., ports: _Optional[_Iterable[_Union[_comms_port_info_pb2.CommsPortInfo, _Mapping]]] = ...) -> None: ...
