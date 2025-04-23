from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.diagnostic_msgs.msg import key_value_pb2 as _key_value_pb2
from make87_messages_ros2.humble.py_trees_ros_interfaces.msg import activity_item_pb2 as _activity_item_pb2
from make87_messages_ros2.humble.py_trees_ros_interfaces.msg import behaviour_pb2 as _behaviour_pb2
from make87_messages_ros2.humble.py_trees_ros_interfaces.msg import statistics_pb2 as _statistics_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BehaviourTree(_message.Message):
    __slots__ = ("header", "behaviours", "changed", "blackboard_on_visited_path", "blackboard_activity", "statistics")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    BEHAVIOURS_FIELD_NUMBER: _ClassVar[int]
    CHANGED_FIELD_NUMBER: _ClassVar[int]
    BLACKBOARD_ON_VISITED_PATH_FIELD_NUMBER: _ClassVar[int]
    BLACKBOARD_ACTIVITY_FIELD_NUMBER: _ClassVar[int]
    STATISTICS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    behaviours: _containers.RepeatedCompositeFieldContainer[_behaviour_pb2.Behaviour]
    changed: bool
    blackboard_on_visited_path: _containers.RepeatedCompositeFieldContainer[_key_value_pb2.KeyValue]
    blackboard_activity: _containers.RepeatedCompositeFieldContainer[_activity_item_pb2.ActivityItem]
    statistics: _statistics_pb2.Statistics
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., behaviours: _Optional[_Iterable[_Union[_behaviour_pb2.Behaviour, _Mapping]]] = ..., changed: bool = ..., blackboard_on_visited_path: _Optional[_Iterable[_Union[_key_value_pb2.KeyValue, _Mapping]]] = ..., blackboard_activity: _Optional[_Iterable[_Union[_activity_item_pb2.ActivityItem, _Mapping]]] = ..., statistics: _Optional[_Union[_statistics_pb2.Statistics, _Mapping]] = ...) -> None: ...
