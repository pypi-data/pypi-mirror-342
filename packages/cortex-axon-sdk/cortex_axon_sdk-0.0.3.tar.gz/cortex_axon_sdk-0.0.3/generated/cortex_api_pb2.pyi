from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional
DESCRIPTOR: _descriptor.FileDescriptor

class CallRequest(_message.Message):
    __slots__ = ('method', 'path', 'content_type', 'body')
    METHOD_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    CONTENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    BODY_FIELD_NUMBER: _ClassVar[int]
    method: str
    path: str
    content_type: str
    body: str

    def __init__(self, method: _Optional[str]=..., path: _Optional[str]=..., content_type: _Optional[str]=..., body: _Optional[str]=...) -> None:
        ...

class CallResponse(_message.Message):
    __slots__ = ('status_code', 'status', 'headers', 'body')

    class HeadersEntry(_message.Message):
        __slots__ = ('key', 'value')
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str

        def __init__(self, key: _Optional[str]=..., value: _Optional[str]=...) -> None:
            ...
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    HEADERS_FIELD_NUMBER: _ClassVar[int]
    BODY_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    status: str
    headers: _containers.ScalarMap[str, str]
    body: str

    def __init__(self, status_code: _Optional[int]=..., status: _Optional[str]=..., headers: _Optional[_Mapping[str, str]]=..., body: _Optional[str]=...) -> None:
        ...