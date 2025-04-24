from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class UserProfileProto(_message.Message):
    __slots__ = ("first_name", "last_name", "company", "picture")
    FIRST_NAME_FIELD_NUMBER: _ClassVar[int]
    LAST_NAME_FIELD_NUMBER: _ClassVar[int]
    COMPANY_FIELD_NUMBER: _ClassVar[int]
    PICTURE_FIELD_NUMBER: _ClassVar[int]
    first_name: str
    last_name: str
    company: str
    picture: str
    def __init__(self, first_name: _Optional[str] = ..., last_name: _Optional[str] = ..., company: _Optional[str] = ..., picture: _Optional[str] = ...) -> None: ...

class UserSettingsProto(_message.Message):
    __slots__ = ("newsletter_sign_up", "multi_factor_authentication", "wizard_finished")
    NEWSLETTER_SIGN_UP_FIELD_NUMBER: _ClassVar[int]
    MULTI_FACTOR_AUTHENTICATION_FIELD_NUMBER: _ClassVar[int]
    WIZARD_FINISHED_FIELD_NUMBER: _ClassVar[int]
    newsletter_sign_up: bool
    multi_factor_authentication: bool
    wizard_finished: bool
    def __init__(self, newsletter_sign_up: bool = ..., multi_factor_authentication: bool = ..., wizard_finished: bool = ...) -> None: ...

class UserProto(_message.Message):
    __slots__ = ("id", "email", "profile", "created_at", "settings")
    ID_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    PROFILE_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_FIELD_NUMBER: _ClassVar[int]
    id: str
    email: str
    profile: UserProfileProto
    created_at: _timestamp_pb2.Timestamp
    settings: UserSettingsProto
    def __init__(self, id: _Optional[str] = ..., email: _Optional[str] = ..., profile: _Optional[_Union[UserProfileProto, _Mapping]] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., settings: _Optional[_Union[UserSettingsProto, _Mapping]] = ...) -> None: ...
