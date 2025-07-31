from pydantic import BaseModel, Field
from typing import Optional
import enum


class PlatformEnum(str, enum.Enum):
    telegram = "telegram"
    email = "email"


class ListTypeEnum(str, enum.Enum):
    whitelist = "whitelist"
    blacklist = "blacklist"


# >>> Profiles
class ProfileBase(BaseModel):
    name: str
    platform: PlatformEnum
    credentials: dict
    proxy: Optional[str] = None


class ProfileCreate(ProfileBase):
    pass


class Profile(ProfileBase):
    id: int
    created_at: Optional[str]

    class Config:
        orm_mode = True


# >>> Templates
class TemplateBase(BaseModel):
    name: str
    subject: Optional[str] = None
    body: str


class TemplateCreate(TemplateBase):
    pass


class Template(TemplateBase):
    id: int
    created_at: Optional[str]

    class Config:
        orm_mode = True


# >>> List Entries
class ListEntryBase(BaseModel):
    profile_id: int
    type: ListTypeEnum
    value: str


class ListEntryCreate(ListEntryBase):
    pass


class ListEntry(ListEntryBase):
    id: int

    class Config:
        orm_mode = True


# >>> Logs
class LogEntry(BaseModel):
    id: int
    profile_id: int
    action: str
    status: str
    detail: Optional[str]
    timestamp: Optional[str]

    class Config:
        orm_mode = True
