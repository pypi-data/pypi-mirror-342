from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.rmf_traffic_msgs.msg import schedule_change_add_item_pb2 as _schedule_change_add_item_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ScheduleChangeAdd(_message.Message):
    __slots__ = ("header", "plan_id", "items")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    PLAN_ID_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    plan_id: int
    items: _containers.RepeatedCompositeFieldContainer[_schedule_change_add_item_pb2.ScheduleChangeAddItem]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., plan_id: _Optional[int] = ..., items: _Optional[_Iterable[_Union[_schedule_change_add_item_pb2.ScheduleChangeAddItem, _Mapping]]] = ...) -> None: ...
