from make87_messages_ros2.rolling.rc_common_msgs.msg import return_code_pb2 as _return_code_pb2
from make87_messages_ros2.rolling.rc_reason_msgs.msg import load_carrier_model_pb2 as _load_carrier_model_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SetLoadCarrierRequest(_message.Message):
    __slots__ = ("load_carrier",)
    LOAD_CARRIER_FIELD_NUMBER: _ClassVar[int]
    load_carrier: _load_carrier_model_pb2.LoadCarrierModel
    def __init__(self, load_carrier: _Optional[_Union[_load_carrier_model_pb2.LoadCarrierModel, _Mapping]] = ...) -> None: ...

class SetLoadCarrierResponse(_message.Message):
    __slots__ = ("return_code",)
    RETURN_CODE_FIELD_NUMBER: _ClassVar[int]
    return_code: _return_code_pb2.ReturnCode
    def __init__(self, return_code: _Optional[_Union[_return_code_pb2.ReturnCode, _Mapping]] = ...) -> None: ...
