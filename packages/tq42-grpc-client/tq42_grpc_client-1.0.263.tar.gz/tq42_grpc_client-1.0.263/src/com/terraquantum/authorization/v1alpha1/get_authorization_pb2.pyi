from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetAuthorizationRequest(_message.Message):
    __slots__ = ("project_id", "organization_id", "principal_mask")
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    PRINCIPAL_MASK_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    organization_id: str
    principal_mask: str
    def __init__(self, project_id: _Optional[str] = ..., organization_id: _Optional[str] = ..., principal_mask: _Optional[str] = ...) -> None: ...

class GetAuthorizationResponse(_message.Message):
    __slots__ = ("principal_authorizations", "project_id", "organization_id")
    class PrincipalAuthorization(_message.Message):
        __slots__ = ("principal_id", "roles")
        PRINCIPAL_ID_FIELD_NUMBER: _ClassVar[int]
        ROLES_FIELD_NUMBER: _ClassVar[int]
        principal_id: str
        roles: _containers.RepeatedScalarFieldContainer[str]
        def __init__(self, principal_id: _Optional[str] = ..., roles: _Optional[_Iterable[str]] = ...) -> None: ...
    PRINCIPAL_AUTHORIZATIONS_FIELD_NUMBER: _ClassVar[int]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    principal_authorizations: _containers.RepeatedCompositeFieldContainer[GetAuthorizationResponse.PrincipalAuthorization]
    project_id: str
    organization_id: str
    def __init__(self, principal_authorizations: _Optional[_Iterable[_Union[GetAuthorizationResponse.PrincipalAuthorization, _Mapping]]] = ..., project_id: _Optional[str] = ..., organization_id: _Optional[str] = ...) -> None: ...
