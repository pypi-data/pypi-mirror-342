from make87_messages_ros2.rolling.rmf_traffic_msgs.msg import schedule_change_add_item_pb2 as _schedule_change_add_item_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ScheduleChangeAdd(_message.Message):
    __slots__ = ("plan_id", "items")
    PLAN_ID_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    plan_id: int
    items: _containers.RepeatedCompositeFieldContainer[_schedule_change_add_item_pb2.ScheduleChangeAddItem]
    def __init__(self, plan_id: _Optional[int] = ..., items: _Optional[_Iterable[_Union[_schedule_change_add_item_pb2.ScheduleChangeAddItem, _Mapping]]] = ...) -> None: ...
