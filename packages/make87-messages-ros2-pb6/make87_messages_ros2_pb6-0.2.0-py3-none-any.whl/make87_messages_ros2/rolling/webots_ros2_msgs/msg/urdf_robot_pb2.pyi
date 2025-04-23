from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class UrdfRobot(_message.Message):
    __slots__ = ("name", "urdf_path", "robot_description", "relative_path_prefix", "translation", "rotation", "normal", "box_collision", "init_pos")
    NAME_FIELD_NUMBER: _ClassVar[int]
    URDF_PATH_FIELD_NUMBER: _ClassVar[int]
    ROBOT_DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    RELATIVE_PATH_PREFIX_FIELD_NUMBER: _ClassVar[int]
    TRANSLATION_FIELD_NUMBER: _ClassVar[int]
    ROTATION_FIELD_NUMBER: _ClassVar[int]
    NORMAL_FIELD_NUMBER: _ClassVar[int]
    BOX_COLLISION_FIELD_NUMBER: _ClassVar[int]
    INIT_POS_FIELD_NUMBER: _ClassVar[int]
    name: str
    urdf_path: str
    robot_description: str
    relative_path_prefix: str
    translation: str
    rotation: str
    normal: bool
    box_collision: bool
    init_pos: str
    def __init__(self, name: _Optional[str] = ..., urdf_path: _Optional[str] = ..., robot_description: _Optional[str] = ..., relative_path_prefix: _Optional[str] = ..., translation: _Optional[str] = ..., rotation: _Optional[str] = ..., normal: bool = ..., box_collision: bool = ..., init_pos: _Optional[str] = ...) -> None: ...
