from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class UserInputADAS(_message.Message):
    __slots__ = ("header", "btn_cc_on", "btn_cc_off", "btn_cc_on_off", "btn_cc_set_inc", "btn_cc_set_dec", "btn_cc_res", "btn_cc_cncl", "btn_cc_res_cncl", "btn_acc_gap_inc", "btn_acc_gap_dec", "btn_lka_on", "btn_lka_off", "btn_lka_on_off")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    BTN_CC_ON_FIELD_NUMBER: _ClassVar[int]
    BTN_CC_OFF_FIELD_NUMBER: _ClassVar[int]
    BTN_CC_ON_OFF_FIELD_NUMBER: _ClassVar[int]
    BTN_CC_SET_INC_FIELD_NUMBER: _ClassVar[int]
    BTN_CC_SET_DEC_FIELD_NUMBER: _ClassVar[int]
    BTN_CC_RES_FIELD_NUMBER: _ClassVar[int]
    BTN_CC_CNCL_FIELD_NUMBER: _ClassVar[int]
    BTN_CC_RES_CNCL_FIELD_NUMBER: _ClassVar[int]
    BTN_ACC_GAP_INC_FIELD_NUMBER: _ClassVar[int]
    BTN_ACC_GAP_DEC_FIELD_NUMBER: _ClassVar[int]
    BTN_LKA_ON_FIELD_NUMBER: _ClassVar[int]
    BTN_LKA_OFF_FIELD_NUMBER: _ClassVar[int]
    BTN_LKA_ON_OFF_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    btn_cc_on: bool
    btn_cc_off: bool
    btn_cc_on_off: bool
    btn_cc_set_inc: bool
    btn_cc_set_dec: bool
    btn_cc_res: bool
    btn_cc_cncl: bool
    btn_cc_res_cncl: bool
    btn_acc_gap_inc: bool
    btn_acc_gap_dec: bool
    btn_lka_on: bool
    btn_lka_off: bool
    btn_lka_on_off: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., btn_cc_on: bool = ..., btn_cc_off: bool = ..., btn_cc_on_off: bool = ..., btn_cc_set_inc: bool = ..., btn_cc_set_dec: bool = ..., btn_cc_res: bool = ..., btn_cc_cncl: bool = ..., btn_cc_res_cncl: bool = ..., btn_acc_gap_inc: bool = ..., btn_acc_gap_dec: bool = ..., btn_lka_on: bool = ..., btn_lka_off: bool = ..., btn_lka_on_off: bool = ...) -> None: ...
