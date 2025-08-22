from datetime import datetime, timezone
import enum
from typing import Any, List, Optional
from sqlmodel import JSON, TEXT, Enum, SQLModel, Field
from sqlalchemy import Column, DateTime, func
from pydantic import EmailStr


class PlatformEnum(str, enum.Enum):
    telegram = "telegram"
    email = "email"


class ListTypeEnum(str, enum.Enum):
    whitelist = "whitelist"
    blacklist = "blacklist"


def get_utc_now() -> datetime:
    return datetime.now(timezone.utc)


# >>> Profiles
class ProfileBase(SQLModel):
    name: str
    platform: PlatformEnum = Field(sa_column=Column(Enum(PlatformEnum), nullable=False))
    credentials: Optional[dict] = Field(sa_column=Column(JSON, nullable=True))
    cookies: Optional[dict[str, Any] | list[dict[str, Any]]] = Field(
        default=None, sa_column=Column(JSON, nullable=True)
    )
    proxy: Optional[str] = None


class Profile(ProfileBase, table=True, __tablename__="mpm_profile"):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=func.now)
    updated_at: datetime = Field(
        default_factory=get_utc_now, sa_column_kwargs={"onupdate": func.now()}
    )
    deleted_at: Optional[datetime] = Field(
        default=None, sa_column=Column(DateTime, nullable=True)
    )


class ProfileCreate(ProfileBase):
    pass


class ProfileUpdate(ProfileBase):
    cookies: Optional[dict[str, Any] | list[dict[str, Any]]] = Field(
        default=None, sa_column=Column(JSON, nullable=True)
    )


class ProfilePublic(ProfileBase):
    id: int


# >>> Campaings
class CampaignBase(SQLModel):
    name: str
    description: Optional[str] = Field(default=None, nullable=True)
    cookies: Optional[dict[str, Any] | list[dict[str, Any]]] = Field(
        default=None, sa_column=Column(JSON, nullable=True)
    )


class CampaignCreate(CampaignBase):
    pass


class CampaignUpdate(CampaignBase):
    name: str
    description: Optional[str] = Field(default=None, nullable=True)
    cookies: Optional[dict[str, Any] | list[dict[str, Any]]] = Field(
        default=None, sa_column=Column(JSON, nullable=True)
    )


class Campaign(CampaignBase, table=True, __tablename__="mpm_campaign"):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=func.now)
    updated_at: datetime = Field(
        default_factory=get_utc_now, sa_column_kwargs={"onupdate": func.now()}
    )


# >>> List Entries
class ListEntryBase(SQLModel):
    type: ListTypeEnum = Field(sa_column=Column(Enum(ListTypeEnum), nullable=False))
    value: str = Field(nullable=False)  # e.g. user id, email address
    campaign_id: int| None = Field(default=None, foreign_key="campaign.id")
    profile_id: int| None = Field(default=None, foreign_key="profile.id")


class ListEntryCreate(ListEntryBase):
    pass


class ListEntryUpdate(ListEntryBase):
    status: str = Field(default="draft", nullable=False)
    data: Optional[dict[str, Any]] = Field(
        default=None, sa_column=Column(JSON, nullable=True)
    )


class ListEntry(ListEntryBase, table=True, __tablename__="mpm_list_entry"):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=func.now)
    updated_at: datetime = Field(
        default_factory=get_utc_now, sa_column_kwargs={"onupdate": func.now()}
    )


# >>> Templates
class TemplateBase(SQLModel):
    name: str = Field(index=True)
    subject: Optional[EmailStr] = Field(default=None, nullable=False)  # for email
    body: Optional[str | None] = Field(
        sa_column=Column(TEXT, nullable=True)
    )  # message text with variables


class TemplateCreate(TemplateBase):
    pass


class TemplateUpdate(TemplateBase):
    name: str = Field(index=True)
    subject: Optional[EmailStr] = Field(default=None, nullable=False)  # for email
    body: Optional[str | None] = Field(
        sa_column=Column(TEXT, nullable=True)
    )  # message text with variables


class Template(TemplateBase, table=True, __tablename__="mpm_template"):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=func.now)
    updated_at: datetime = Field(
        default_factory=get_utc_now, sa_column_kwargs={"onupdate": func.now()}
    )


# >>> Logs
class LogEntry(SQLModel, Table=True, __tablename__="mpm_log_entry"):
    id: int | None = Field(default=None, primary_key=True)
    profile_id: int
    action: str  # e.g. "send_message", "invite", etc.
    status: str  # e.g. "success", "error", etc.
    detail: Optional[str] = Field(
        default=None, sa_column=Column(TEXT, nullable=True)
    )  # error message or extra info
    created_at: datetime = Field(default_factory=get_utc_now)
