from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SbgStatusCom(_message.Message):
    __slots__ = ("header", "port_a", "port_b", "port_c", "port_d", "port_e", "port_a_rx", "port_a_tx", "port_b_rx", "port_b_tx", "port_c_rx", "port_c_tx", "port_d_rx", "port_d_tx", "port_e_rx", "port_e_tx", "eth_0", "eth_1", "eth_2", "eth_3", "eth_4", "eth_0_rx", "eth_0_tx", "eth_1_rx", "eth_1_tx", "eth_2_rx", "eth_2_tx", "eth_3_rx", "eth_3_tx", "eth_4_rx", "eth_4_tx", "can_rx", "can_tx", "can_status")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    PORT_A_FIELD_NUMBER: _ClassVar[int]
    PORT_B_FIELD_NUMBER: _ClassVar[int]
    PORT_C_FIELD_NUMBER: _ClassVar[int]
    PORT_D_FIELD_NUMBER: _ClassVar[int]
    PORT_E_FIELD_NUMBER: _ClassVar[int]
    PORT_A_RX_FIELD_NUMBER: _ClassVar[int]
    PORT_A_TX_FIELD_NUMBER: _ClassVar[int]
    PORT_B_RX_FIELD_NUMBER: _ClassVar[int]
    PORT_B_TX_FIELD_NUMBER: _ClassVar[int]
    PORT_C_RX_FIELD_NUMBER: _ClassVar[int]
    PORT_C_TX_FIELD_NUMBER: _ClassVar[int]
    PORT_D_RX_FIELD_NUMBER: _ClassVar[int]
    PORT_D_TX_FIELD_NUMBER: _ClassVar[int]
    PORT_E_RX_FIELD_NUMBER: _ClassVar[int]
    PORT_E_TX_FIELD_NUMBER: _ClassVar[int]
    ETH_0_FIELD_NUMBER: _ClassVar[int]
    ETH_1_FIELD_NUMBER: _ClassVar[int]
    ETH_2_FIELD_NUMBER: _ClassVar[int]
    ETH_3_FIELD_NUMBER: _ClassVar[int]
    ETH_4_FIELD_NUMBER: _ClassVar[int]
    ETH_0_RX_FIELD_NUMBER: _ClassVar[int]
    ETH_0_TX_FIELD_NUMBER: _ClassVar[int]
    ETH_1_RX_FIELD_NUMBER: _ClassVar[int]
    ETH_1_TX_FIELD_NUMBER: _ClassVar[int]
    ETH_2_RX_FIELD_NUMBER: _ClassVar[int]
    ETH_2_TX_FIELD_NUMBER: _ClassVar[int]
    ETH_3_RX_FIELD_NUMBER: _ClassVar[int]
    ETH_3_TX_FIELD_NUMBER: _ClassVar[int]
    ETH_4_RX_FIELD_NUMBER: _ClassVar[int]
    ETH_4_TX_FIELD_NUMBER: _ClassVar[int]
    CAN_RX_FIELD_NUMBER: _ClassVar[int]
    CAN_TX_FIELD_NUMBER: _ClassVar[int]
    CAN_STATUS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    port_a: bool
    port_b: bool
    port_c: bool
    port_d: bool
    port_e: bool
    port_a_rx: bool
    port_a_tx: bool
    port_b_rx: bool
    port_b_tx: bool
    port_c_rx: bool
    port_c_tx: bool
    port_d_rx: bool
    port_d_tx: bool
    port_e_rx: bool
    port_e_tx: bool
    eth_0: bool
    eth_1: bool
    eth_2: bool
    eth_3: bool
    eth_4: bool
    eth_0_rx: bool
    eth_0_tx: bool
    eth_1_rx: bool
    eth_1_tx: bool
    eth_2_rx: bool
    eth_2_tx: bool
    eth_3_rx: bool
    eth_3_tx: bool
    eth_4_rx: bool
    eth_4_tx: bool
    can_rx: bool
    can_tx: bool
    can_status: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., port_a: bool = ..., port_b: bool = ..., port_c: bool = ..., port_d: bool = ..., port_e: bool = ..., port_a_rx: bool = ..., port_a_tx: bool = ..., port_b_rx: bool = ..., port_b_tx: bool = ..., port_c_rx: bool = ..., port_c_tx: bool = ..., port_d_rx: bool = ..., port_d_tx: bool = ..., port_e_rx: bool = ..., port_e_tx: bool = ..., eth_0: bool = ..., eth_1: bool = ..., eth_2: bool = ..., eth_3: bool = ..., eth_4: bool = ..., eth_0_rx: bool = ..., eth_0_tx: bool = ..., eth_1_rx: bool = ..., eth_1_tx: bool = ..., eth_2_rx: bool = ..., eth_2_tx: bool = ..., eth_3_rx: bool = ..., eth_3_tx: bool = ..., eth_4_rx: bool = ..., eth_4_tx: bool = ..., can_rx: bool = ..., can_tx: bool = ..., can_status: _Optional[int] = ...) -> None: ...
