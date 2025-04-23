from make87_messages_ros2.jazzy.nav2_msgs.msg import costmap_pb2 as _costmap_pb2
from make87_messages_ros2.jazzy.nav2_msgs.msg import costmap_meta_data_pb2 as _costmap_meta_data_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetCostmapRequest(_message.Message):
    __slots__ = ["specs"]
    SPECS_FIELD_NUMBER: _ClassVar[int]
    specs: _costmap_meta_data_pb2.CostmapMetaData
    def __init__(self, specs: _Optional[_Union[_costmap_meta_data_pb2.CostmapMetaData, _Mapping]] = ...) -> None: ...

class GetCostmapResponse(_message.Message):
    __slots__ = ["map"]
    MAP_FIELD_NUMBER: _ClassVar[int]
    map: _costmap_pb2.Costmap
    def __init__(self, map: _Optional[_Union[_costmap_pb2.Costmap, _Mapping]] = ...) -> None: ...
