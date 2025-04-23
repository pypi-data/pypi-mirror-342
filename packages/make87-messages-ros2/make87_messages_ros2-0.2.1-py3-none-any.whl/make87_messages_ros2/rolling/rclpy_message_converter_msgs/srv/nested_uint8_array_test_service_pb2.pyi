from make87_messages_ros2.rolling.rclpy_message_converter_msgs.msg import nested_uint8_array_test_message_pb2 as _nested_uint8_array_test_message_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class NestedUint8ArrayTestServiceRequest(_message.Message):
    __slots__ = ["input"]
    INPUT_FIELD_NUMBER: _ClassVar[int]
    input: _nested_uint8_array_test_message_pb2.NestedUint8ArrayTestMessage
    def __init__(self, input: _Optional[_Union[_nested_uint8_array_test_message_pb2.NestedUint8ArrayTestMessage, _Mapping]] = ...) -> None: ...

class NestedUint8ArrayTestServiceResponse(_message.Message):
    __slots__ = ["output"]
    OUTPUT_FIELD_NUMBER: _ClassVar[int]
    output: _nested_uint8_array_test_message_pb2.NestedUint8ArrayTestMessage
    def __init__(self, output: _Optional[_Union[_nested_uint8_array_test_message_pb2.NestedUint8ArrayTestMessage, _Mapping]] = ...) -> None: ...
