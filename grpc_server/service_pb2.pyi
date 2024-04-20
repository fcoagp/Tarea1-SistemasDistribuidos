from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class NameRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class NameReply(_message.Message):
    __slots__ = ("id", "nconst", "primaryName", "birthYear", "deathYear", "primaryProfession", "knownForTitles")
    ID_FIELD_NUMBER: _ClassVar[int]
    NCONST_FIELD_NUMBER: _ClassVar[int]
    PRIMARYNAME_FIELD_NUMBER: _ClassVar[int]
    BIRTHYEAR_FIELD_NUMBER: _ClassVar[int]
    DEATHYEAR_FIELD_NUMBER: _ClassVar[int]
    PRIMARYPROFESSION_FIELD_NUMBER: _ClassVar[int]
    KNOWNFORTITLES_FIELD_NUMBER: _ClassVar[int]
    id: int
    nconst: str
    primaryName: str
    birthYear: str
    deathYear: str
    primaryProfession: str
    knownForTitles: str
    def __init__(self, id: _Optional[int] = ..., nconst: _Optional[str] = ..., primaryName: _Optional[str] = ..., birthYear: _Optional[str] = ..., deathYear: _Optional[str] = ..., primaryProfession: _Optional[str] = ..., knownForTitles: _Optional[str] = ...) -> None: ...
