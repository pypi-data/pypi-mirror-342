from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class StringArrays(_message.Message):
    __slots__ = ["ub_string_static_array_value", "ub_string_ub_array_value", "ub_string_dynamic_array_value", "string_dynamic_array_value", "string_static_array_value", "string_bounded_array_value", "def_string_dynamic_array_value", "def_string_static_array_value", "def_string_bounded_array_value", "def_various_quotes", "def_various_commas"]
    UB_STRING_STATIC_ARRAY_VALUE_FIELD_NUMBER: _ClassVar[int]
    UB_STRING_UB_ARRAY_VALUE_FIELD_NUMBER: _ClassVar[int]
    UB_STRING_DYNAMIC_ARRAY_VALUE_FIELD_NUMBER: _ClassVar[int]
    STRING_DYNAMIC_ARRAY_VALUE_FIELD_NUMBER: _ClassVar[int]
    STRING_STATIC_ARRAY_VALUE_FIELD_NUMBER: _ClassVar[int]
    STRING_BOUNDED_ARRAY_VALUE_FIELD_NUMBER: _ClassVar[int]
    DEF_STRING_DYNAMIC_ARRAY_VALUE_FIELD_NUMBER: _ClassVar[int]
    DEF_STRING_STATIC_ARRAY_VALUE_FIELD_NUMBER: _ClassVar[int]
    DEF_STRING_BOUNDED_ARRAY_VALUE_FIELD_NUMBER: _ClassVar[int]
    DEF_VARIOUS_QUOTES_FIELD_NUMBER: _ClassVar[int]
    DEF_VARIOUS_COMMAS_FIELD_NUMBER: _ClassVar[int]
    ub_string_static_array_value: _containers.RepeatedScalarFieldContainer[str]
    ub_string_ub_array_value: _containers.RepeatedScalarFieldContainer[str]
    ub_string_dynamic_array_value: _containers.RepeatedScalarFieldContainer[str]
    string_dynamic_array_value: _containers.RepeatedScalarFieldContainer[str]
    string_static_array_value: _containers.RepeatedScalarFieldContainer[str]
    string_bounded_array_value: _containers.RepeatedScalarFieldContainer[str]
    def_string_dynamic_array_value: _containers.RepeatedScalarFieldContainer[str]
    def_string_static_array_value: _containers.RepeatedScalarFieldContainer[str]
    def_string_bounded_array_value: _containers.RepeatedScalarFieldContainer[str]
    def_various_quotes: _containers.RepeatedScalarFieldContainer[str]
    def_various_commas: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, ub_string_static_array_value: _Optional[_Iterable[str]] = ..., ub_string_ub_array_value: _Optional[_Iterable[str]] = ..., ub_string_dynamic_array_value: _Optional[_Iterable[str]] = ..., string_dynamic_array_value: _Optional[_Iterable[str]] = ..., string_static_array_value: _Optional[_Iterable[str]] = ..., string_bounded_array_value: _Optional[_Iterable[str]] = ..., def_string_dynamic_array_value: _Optional[_Iterable[str]] = ..., def_string_static_array_value: _Optional[_Iterable[str]] = ..., def_string_bounded_array_value: _Optional[_Iterable[str]] = ..., def_various_quotes: _Optional[_Iterable[str]] = ..., def_various_commas: _Optional[_Iterable[str]] = ...) -> None: ...
