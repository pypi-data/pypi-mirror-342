from make87_messages_ros2.rolling.autoware_map_msgs.msg import point_cloud_map_cell_meta_data_pb2 as _point_cloud_map_cell_meta_data_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PointCloudMapCellMetaDataWithID(_message.Message):
    __slots__ = ["cell_id", "metadata"]
    CELL_ID_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    cell_id: str
    metadata: _point_cloud_map_cell_meta_data_pb2.PointCloudMapCellMetaData
    def __init__(self, cell_id: _Optional[str] = ..., metadata: _Optional[_Union[_point_cloud_map_cell_meta_data_pb2.PointCloudMapCellMetaData, _Mapping]] = ...) -> None: ...
